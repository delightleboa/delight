#!/usr/bin/env python
import os
import logging
import signal
import traceback
import wyzepal
import sys

from types import FrameType
from typing import Any, Callable, Dict

from matrix_bridge_config import config
from matrix_client.api import MatrixRequestError
from matrix_client.client import MatrixClient
from requests.exceptions import MissingSchema

def matrix_login(matrix_client: Any, matrix_config: Dict[str, Any]) -> None:
    try:
        matrix_client.login_with_password(matrix_config["username"],
                                          matrix_config["password"])
    except MatrixRequestError as e:
        if e.code == 403:
            sys.exit("Bad username or password.")
        else:
            sys.exit("Check if your server details are correct.")
    except MissingSchema as e:
        sys.exit("Bad URL format.")

def matrix_join_room(matrix_client: Any, matrix_config: Dict[str, Any]) -> Any:
    try:
        room = matrix_client.join_room(matrix_config["room_id"])
        return room
    except MatrixRequestError as e:
        if e.code == 403:
            sys.exit("Room ID/Alias in the wrong format")
        else:
            sys.exit("Couldn't find room.")

def die(signal: int, frame: FrameType) -> None:
    # We actually want to exit, so run os._exit (so as not to be caught and restarted)
    os._exit(1)

def wyzepal_to_matrix_username(full_name: str, site: str) -> str:
    # Strip spaces from the full_name
    full_name = "".join(full_name.split(' '))
    return "@wyzepal_{0}:{1}".format(full_name, site)

def matrix_to_wyzepal(wyzepal_client: wyzepal.Client, wyzepal_config: Dict[str, Any],
                    matrix_config: Dict[str, Any]) -> Callable[[Any, Dict[str, Any]], None]:
    def _matrix_to_wyzepal(room: Any, event: Dict[str, Any]) -> None:
        """
        Matrix -> WyzePal
        """
        content = get_message_content_from_event(event)

        wyzepal_bot_user = ('@%s:matrix.org' % matrix_config['username'])
        # We do this to identify the messages generated from WyzePal -> Matrix
        # and we make sure we don't forward it again to the WyzePal stream.
        not_from_wyzepal_bot = ('body' not in event['content'] or
                              event['sender'] != wyzepal_bot_user)

        if not_from_wyzepal_bot:
            try:
                result = wyzepal_client.send_message({
                    "sender": wyzepal_client.email,
                    "type": "stream",
                    "to": wyzepal_config["stream"],
                    "subject": wyzepal_config["subject"],
                    "content": content,
                })
            except MatrixRequestError as e:
                # Generally raised when user is forbidden
                raise Exception(e)
            if result['result'] != 'success':
                # Generally raised when API key is invalid
                raise Exception(result['msg'])

    return _matrix_to_wyzepal

def get_message_content_from_event(event: Dict[str, Any]) -> str:
    if event['type'] == "m.room.member":
        if event['membership'] == "join":
            content = "{0} joined".format(event['sender'])
        elif event['membership'] == "leave":
            content = "{0} quit".format(event['sender'])
    elif event['type'] == "m.room.message":
        if event['content']['msgtype'] == "m.text" or event['content']['msgtype'] == "m.emote":
            content = "{0}: {1}".format(event['sender'], event['content']['body'])
    else:
        content = event['type']
    return content

def wyzepal_to_matrix(config: Dict[str, Any], room: Any) -> Callable[[Dict[str, Any]], None]:
    site_without_http = config["site"].replace("https://", "").replace("http://", "")

    def _wyzepal_to_matrix(msg: Dict[str, Any]) -> None:
        """
        WyzePal -> Matrix
        """
        message_valid = check_wyzepal_message_validity(msg, config)
        if message_valid:
            matrix_username = wyzepal_to_matrix_username(msg["sender_full_name"], site_without_http)
            matrix_text = "{0}: {1}".format(matrix_username, msg["content"])
            # Forward WyzePal message to Matrix
            room.send_text(matrix_text)
    return _wyzepal_to_matrix

def check_wyzepal_message_validity(msg: Dict[str, Any], config: Dict[str, Any]) -> bool:
    is_a_stream = msg["type"] == "stream"
    in_the_specified_stream = msg["display_recipient"] == config["stream"]
    at_the_specified_subject = msg["subject"] == config["subject"]

    # We do this to identify the messages generated from Matrix -> WyzePal
    # and we make sure we don't forward it again to the Matrix.
    not_from_wyzepal_bot = msg["sender_email"] != config["email"]
    if is_a_stream and not_from_wyzepal_bot and in_the_specified_stream and at_the_specified_subject:
        return True
    return False

if __name__ == '__main__':
    signal.signal(signal.SIGINT, die)
    logging.basicConfig(level=logging.WARNING)

    # Get config for each clients
    wyzepal_config = config["wyzepal"]
    matrix_config = config["matrix"]

    # Initiate clients
    backoff = wyzepal.RandomExponentialBackoff(timeout_success_equivalent=300)
    while backoff.keep_going():
        print("Starting matrix mirroring bot")
        try:
            wyzepal_client = wyzepal.Client(email=wyzepal_config["email"],
                                        api_key=wyzepal_config["api_key"],
                                        site=wyzepal_config["site"])
            matrix_client = MatrixClient(matrix_config["host"])

            # Login to Matrix
            matrix_login(matrix_client, matrix_config)
            # Join a room in Matrix
            room = matrix_join_room(matrix_client, matrix_config)

            room.add_listener(matrix_to_wyzepal(wyzepal_client, wyzepal_config, matrix_config))

            print("Starting listener thread on Matrix client")
            matrix_client.start_listener_thread()

            print("Starting message handler on WyzePal client")
            wyzepal_client.call_on_each_message(wyzepal_to_matrix(wyzepal_config, room))
        except Exception:
            traceback.print_exc()
        backoff.fail()

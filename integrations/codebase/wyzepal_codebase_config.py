# -*- coding: utf-8 -*-
#
# Copyright © 2014 WyzePal, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# Change these values to configure authentication for your codebase account
# Note that this is the Codebase API Username, found in the Settings page
# for your account
CODEBASE_API_USERNAME = "foo@example.com"
CODEBASE_API_KEY = "1234561234567abcdef"

# The URL of your codebase setup
CODEBASE_ROOT_URL = "https://YOUR_COMPANY.codebasehq.com"

# When initially started, how many hours of messages to include.
# Note that the Codebase API only returns the 20 latest events,
# if you have more than 20 events that fit within this window,
# earlier ones may be lost
CODEBASE_INITIAL_HISTORY_HOURS = 12

# Change these values to configure WyzePal authentication for the plugin
WYZEPAL_USER = "codebase-bot@example.com"
WYZEPAL_API_KEY = "0123456789abcdef0123456789abcdef"

# The streams to send commit information and ticket information to
WYZEPAL_COMMITS_STREAM_NAME = "codebase"
WYZEPAL_TICKETS_STREAM_NAME = "tickets"

# If properly installed, the WyzePal API should be in your import
# path, but if not, set a custom path below
WYZEPAL_API_PATH = None

# Set this to your WyzePal API server URI
WYZEPAL_SITE = "https://wyzepal.example.com"

# If you wish to log to a file rather than stdout/stderr,
# please fill this out your desired path
LOG_FILE = None

# This file is used to resume this mirror in case the script shuts down.
# It is required and needs to be writeable.
RESUME_FILE = "/var/tmp/wyzepal_codebase.state"

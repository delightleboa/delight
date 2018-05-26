#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
if False:
    from typing import Any, Dict, Generator, List, Tuple

import os
import sys

import itertools

def version():
    # type: () -> str
    version_py = os.path.join(os.path.dirname(__file__), "wyzepal", "__init__.py")
    with open(version_py) as in_handle:
        version_line = next(itertools.dropwhile(lambda x: not x.startswith("__version__"),
                                                in_handle))
    version = version_line.split('=')[-1].strip().replace('"', '')
    return version

def recur_expand(target_root, dir):
    # type: (Any, Any) -> Generator[Tuple[str, List[str]], None, None]
    for root, _, files in os.walk(dir):
        paths = [os.path.join(root, f) for f in files]
        if len(paths):
            yield os.path.join(target_root, root), paths

# We should be installable with either setuptools or distutils.
package_info = dict(
    name='wyzepal',
    version=version(),
    description='Bindings for the WyzePal message API',
    author='WyzePal Open Source Project',
    author_email='wyzepal-devel@googlegroups.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Communications :: Chat',
    ],
    url='https://www.wyzepal.org/',
    data_files=list(recur_expand('share/wyzepal', 'integrations')),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'wyzepal-send=wyzepal.send:main',
            'wyzepal-api-examples=wyzepal.api_examples:main'
        ],
    },
    package_data={'wyzepal': ["py.typed"]},
)  # type: Dict[str, Any]

setuptools_info = dict(
    install_requires=['requests[security]>=0.12.1',
                      'six',
                      'typing>=3.5.2.2',
                      ],
)

try:
    from setuptools import setup, find_packages
    package_info.update(setuptools_info)
    package_info['packages'] = find_packages(exclude=['tests'])

except ImportError:
    from distutils.core import setup
    from distutils.version import LooseVersion
    # Manual dependency check
    try:
        import requests
        assert(LooseVersion(requests.__version__) >= LooseVersion('0.12.1'))
    except (ImportError, AssertionError):
        print("requests >=0.12.1 is not installed", file=sys.stderr)
        sys.exit(1)

    package_info['packages'] = ['wyzepal']


setup(**package_info)

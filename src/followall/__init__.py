#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Kurtiss Hare on 2010-11-14.
Copyright (c) 2010 Medium Entertainment, Inc. All rights reserved.
"""

from followall import api
from followall.version import VERSION
from tweepy.error import TweepError
import sys


__version__ = VERSION


def followall(suggest_username, follow_username):
    suggest = api.for_user(suggest_username)
    follow = api.for_user(follow_username)

    while True:
        recommendations = suggest.get_user_recommendations(cursor = '-1')
        if not recommendations:
            break

        for rec in recommendations:
            try:
                sys.stdout.write("following: {0}…".format(rec['user']['screen_name']))
                sys.stdout.flush()
                follow.create_friendship(rec['user']['id'])
                suggest.hide_user_recommendation(rec['user']['id'])
            except TweepError as e:
                if not e.reason.endswith("is already on your list."):
                    raise
                print "skipped."
            else:
                print "done."
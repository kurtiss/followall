#!/usr/bin/env python
# encoding: utf-8
"""
api.py

Created by Kurtiss Hare on 2010-11-14.
Copyright (c) 2010 Medium Entertainment, Inc. All rights reserved.
"""

import errno, os, tweepy, urllib
import tweepy
from tweepy.binder import bind_api
from tweepy.parsers import JSONParser

FOLLOWALL_DIR = ".followall"


class FollowAllAPI(tweepy.API):
    get_user_recommendations = bind_api(
        path = "/users/recommendations.json",
        payload_type = "user", payload_list = True,
        allowed_param = ['cursor'],
        require_auth = True
    )
    
    def hide_user_recommendation(self, *args, **kwargs):
        kwargs.setdefault('token', '1')
        
        return bind_api(
            path = "/users/recommendations/hide.json",
            method = "POST",
            payload_type = "user",
            allowed_param = ['recommended_user_id', 'token'],
            require_auth = True
        )(self, *args, **kwargs)


def for_user(username):
    try:
        from win32com.shell import shellcon, shell
        homedir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
    except ImportError:
        homedir = os.path.expanduser("~")

    datadir = os.path.join(homedir, FOLLOWALL_DIR)

    try:
        os.makedirs(datadir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    consumer_key_file = os.path.join(datadir, "consumer_key")
    consumer_secret_file = os.path.join(datadir, "consumer_secret")
    consumer_key = None
    consumer_secret = None
    
    try:
        with open(consumer_key_file, "r") as f:
            consumer_key = f.read()
        with open(consumer_secret_file, "r") as f:
            consumer_secret = f.read()
    except IOError:
        pass
    
    if not consumer_key or not consumer_secret:
        consumer_key = raw_input("Consumer Key: ")
        consumer_secret = raw_input("Consumer Secret: ")

        with open(consumer_key_file, "w") as f:
            f.write(consumer_key)
        with open(consumer_secret_file, "w") as f:
            f.write(consumer_secret)

    user_access_key_file = os.path.join(datadir, "id_twitter_{0}.pub".format(username))
    user_secret_key_file = os.path.join(datadir, "id_twitter_{0}".format(username))
    access_key = ""
    secret_key = ""

    try:
        with open(user_access_key_file, "r") as f:
            access_key = f.read()
        with open(user_secret_key_file, "r") as f:
            secret_key = f.read()
    except IOError:
        pass

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, secret_key)
    api = FollowAllAPI(auth, parser = JSONParser())

    if not api.verify_credentials():
        print "Authorize this application for {0} by visiting: {1}".format(username, auth.get_authorization_url())
        auth.get_access_token(raw_input("PIN: ").strip())

        with open(user_access_key_file, "w") as f:
            f.write(auth.access_token.key)
        with open(user_secret_key_file, "w") as f:
            f.write(auth.access_token.secret)

    return api
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
import re

ESCAPE = re.compile(r'[\x00-\x1f\\"\b\f\n\r\t]')
ESCAPE_DICT = {
    '\\': '\\\\',
    '"': '""',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
}



# pylint: disable=too-few-public-methods
class common(object):
    """ json exporter plugin.
        By convention it has to be called exactly the same as its file name.
        (Apart from .py extention)
    """

    def __init__(self):
        """ constructor """
        for i in range(0x20):
            ESCAPE_DICT.setdefault(chr(i), '\\u{0:04x}'.format(i))

    @staticmethod
    def extract_message_data(msg):
        """ Extracts user name from 'sender', message caption and message content from msg.
            :param msg: Raw message object.

            :return
                (...) tuple of message attributes
        """
        sender = msg.sender

        # Get the name of the sender if any
        is_sent_by_bot = None
        if sender:
            name = getattr(sender, 'username', None)
            if not name:
                name = getattr(sender, 'title', None)
                if not name:
                    name = (sender.first_name or "") + " " + (sender.last_name or "")
                    name = name.strip()
                if not name:
                    name = '???'
            is_sent_by_bot = sender.bot
        else:
            name = '???'

        caption = None
        if hasattr(msg, 'message'):
            content = msg.message
        elif hasattr(msg, 'action'):
            content = str(msg.action)
        else:
            # Unknown message, simply print its class name
            content = type(msg).__name__

        re_id_str = ''
        if hasattr(msg, 'reply_to_msg_id') and msg.reply_to_msg_id is not None:
            re_id_str = str(msg.reply_to_msg_id)

        is_contains_media = False
        media_content = None
        # Format the message content
        if getattr(msg, 'media', None):
            # The media may or may not have a caption
            is_contains_media = True
            caption = getattr(msg.media, 'caption', '')
            media_content = '<{}> {}'.format(
                type(msg.media).__name__, caption)

        return name, caption, content, re_id_str, is_sent_by_bot, is_contains_media, media_content

    # This code is inspired by Python's json encoder's code
    @staticmethod
    def py_encode_basestring(s):
        """Return a JSON representation of a Python string"""
        if not s:
            return s

        def replace(match):
            return ESCAPE_DICT[match.group(0)]
        return ESCAPE.sub(replace, s)

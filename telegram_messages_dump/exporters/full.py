#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

import json
from datetime import date, datetime

from telethon.tl.types import MessageMediaPhoto  # , MessageActionChatAddUser

from .common import common


class full(object):
    """ Exporter plugin that exports full information in JSON format.

    As opposed to json exporter jsonl serializes messages as one JSON object per line, not as
    one giant array.

    See http://jsonlines.org.
    """

    def format(self, msg, exporter_context):
        """ Formatter method. Takes raw msg and converts it to a *one-line* string.
            :param msg: Raw message object :class:`telethon.tl.types.Message` and derivatives.
                        https://core.telegram.org/type/Message
            :param exporter_context: exporter_context

            :returns: *one-line* string containing one message data.
        """
        # pylint: disable=line-too-long
        name, _, content, _, is_sent_by_bot, is_contains_media, media_content = \
            common.extract_message_data(msg)

        msg_dictionary = {
            'message_id': msg.id,
            'message': msg.message,
            'from_id': msg.from_id,
            'author': name,
            'from_username': msg.sender.username,
            # 'reply_id': re_id,
            'reply_to_msg_id': msg.reply_to_msg_id,
            'sent_by_bot': is_sent_by_bot,
            'date': msg.date,
            'action': msg.action.to_dict() if msg.action else None,
            # MessageActionChatAddUser(users=[1234567])
            'content': content,
            'contains_media': is_contains_media,
            'media_content': media_content
        }
        media = getattr(msg, 'media', None)
        if media:
            if isinstance(msg.media, MessageMediaPhoto):
                exporter_context.tg_client.download_media(msg, 'downloads/%s.jpg' % msg.id)
            msg_dictionary['media'] = str(msg.media)

        msg_dump_str = json.dumps(
            msg_dictionary, default=self._json_serial, ensure_ascii=False)

        return msg_dump_str

    @staticmethod
    def begin_final_file(resulting_file, exporter_context):
        """ Hook executes at the beginning of writing a resulting file.
            (After BOM is written in case of --addbom)
        """
        pass

    @staticmethod
    def _json_serial(obj):
        """JSON serializer for objects not serializable by default json code
           https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
        """
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))

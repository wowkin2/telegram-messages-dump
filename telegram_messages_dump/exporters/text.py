#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

from .common import common


class text(object):
    """ text exporter plugin.
        By convention it has to be called exactly the same as its file name.
        (Apart from .py extension)
    """

    # pylint: disable=unused-argument
    @staticmethod
    def format(msg, exporter_context):
        """ Formatter method. Takes raw msg and converts it to a *one-line* string.
            :param msg: Raw message object :class:`telethon.tl.types.Message` and derivatives.
                        https://core.telegram.org/type/Message

            :returns: *one-line* string containing one message data.
        """
        name, _, content, re_id, _, _, _ = common.extract_message_data(msg)
        # Format a message log record
        msg_dump_str = '[{}-{:02d}-{:02d} {:02d}:{:02d}] ID={} {}{}: {}'.format(
            msg.date.year, msg.date.month, msg.date.day,
            msg.date.hour, msg.date.minute, msg.id, "RE_ID=%s " % re_id if re_id else "",
            name, common.py_encode_basestring(content))

        return msg_dump_str

    @staticmethod
    def begin_final_file(resulting_file, exporter_context):
        """ Hook executes at the beginning of writing a resulting file.
            (After BOM is written in case of --addbom)
        """
        pass

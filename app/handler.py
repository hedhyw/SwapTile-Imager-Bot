#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" General Telegram message handler.
"""

import re
from typing import Tuple
from abc import ABC

from telegram import Update
from telegram.ext import CallbackContext


class TaskHandler(ABC):
    """ Interface for subhandlers. """

    def handle(self, category: str, message: str) -> bool:
        """ Process message. """


class ImagerMessageHandler:
    """ General telegram message handler. """

    def __init__(
        self,
        task_handlers: Tuple[TaskHandler],
    ) -> None:
        self._category_re = re.compile(r'#(\w+)($|\s)')
        self._task_handlers = task_handlers

    def handle_message(
        self,
        update: Update,
        _: CallbackContext,
    ) -> None:
        """ The method extracts category from the message ans selects
            handler to process.
        """

        try:
            text = update.message.text

            category = self._category_re.search(text)
            if category is None:
                raise Exception('category not defined')

            category = category.group(1)

            for handler in self._task_handlers:
                handler: TaskHandler

                if handler.handle(category, text):
                    update.message.reply_text('processed')
                    return

            raise Exception('no handler found')

        # pylint: disable=broad-except # It exposes the exception to a client.
        except Exception as ex:
            update.message.reply_text(f'failed to process: {ex}')

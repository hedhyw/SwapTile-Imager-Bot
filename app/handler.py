#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" General Telegram message handler.
"""

from typing import Tuple, Callable, Set
from abc import ABC
import re
import logging

from telegram import Update
from telegram.parsemode import ParseMode
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown

Reply = Callable[[str], None]


class TaskHandler(ABC):
    """ Interface for subhandlers. """

    def handle(self, category: str, message: str, reply: Reply) -> bool:
        """ Process message. """


class ImagerMessageHandler:
    """ General telegram message handler. """

    def __init__(
        self,
        task_handlers: Tuple[TaskHandler],
        allowed_chats: Set[int] = set(),
    ) -> None:
        self._logger = logging.getLogger('ImagerMessageHandler')

        self._category_re = re.compile(r'#(\w+)($|\s)')
        self._task_handlers = task_handlers
        self._allowed_chats = allowed_chats

    def handle_message(
        self,
        update: Update,
        _: CallbackContext,
    ) -> None:
        """ The method extracts category from the message ans selects
            handler to process.
        """

        if len(self._allowed_chats) == 0:
            self._logger.warn('allowed chats not set')
        elif update.message.chat.id not in self._allowed_chats:
            self._logger.warn(f'unconfigured chat id access {update}')

            return

        try:
            text = update.message.text

            category = self._category_re.search(text)
            if category is None:
                raise Exception('category not defined')

            category = category.group(1)

            def callback(text: str) -> None:
                return update.message.reply_text(
                    escape_markdown(f'\\#swaptile \\#{category}\n') + text,
                    parse_mode=ParseMode.MARKDOWN_V2,
                )

            for handler in self._task_handlers:
                handler: TaskHandler

                if handler.handle(category, text, callback):
                    return

            raise Exception('no handler found')

        except Exception as ex:
            self._logger.exception(ex)

            update.message.reply_text(
                f'failed to process: {escape_markdown(str(ex))}',
            )

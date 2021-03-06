#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" The Telegram bot adds the ability to upload images from Unsplash to
    the imager server (https://github.com/ocmoxa/SwapTile-Imager).
"""

import logging
import argparse
from typing import Dict

from telegram.ext import Updater, MessageHandler, Filters

from app.handler import ImagerMessageHandler
from app.unsplash import UnsplashTaskHandler
from app.imager import ImagerClient


def _parse_args() -> Dict:
    parser = argparse.ArgumentParser(
        description='Run SwapTile-Imager bot.',
    )
    parser.add_argument(
        '--telegram',
        dest='telegram',
        type=str,
        required=True,
        help='Telegram access token',
    )
    parser.add_argument(
        '--unsplash',
        dest='unsplash',
        type=str,
        required=True,
        help='Unsplash client ID',
    )
    parser.add_argument(
        '--imager',
        dest='imager',
        type=str,
        default='http://localhost:8081',
        help='Imager address to upload images',
    )
    return parser.parse_args()


def main() -> None:
    """ Application entrypoint. """

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    args = _parse_args()

    imager_client = ImagerClient(args.imager)

    imager_handler = ImagerMessageHandler(
        task_handlers=(
            UnsplashTaskHandler(args.unsplash, imager_client),
        ),
    )

    updater = Updater(args.telegram, use_context=True)
    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.text,
            imager_handler.handle_message,
        ),
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

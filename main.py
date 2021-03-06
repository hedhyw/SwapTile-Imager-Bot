#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" The Telegram bot adds the ability to upload images from Unsplash to
    the imager server (https://github.com/ocmoxa/SwapTile-Imager).
"""

import logging
import argparse
from typing import Dict

from telegram.ext import Updater, CommandHandler

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
        '--allowed-chats',
        dest='allowed_chats',
        type=str,
        required=True,
        help='Comma-separated chat ids in which the bot will work',
    )
    parser.add_argument(
        '--unsplash',
        dest='unsplash',
        type=str,
        required=True,
        help='Unsplash client ID',
    )
    parser.add_argument(
        '--imager-internal',
        dest='imager_internal',
        type=str,
        default='http://localhost:8081',
        help='Imager address to upload images',
    )
    parser.add_argument(
        '--imager-public',
        dest='imager_public',
        type=str,
        default='http://localhost:8081',
        help='Imager address to download images',
    )
    parser.add_argument(
        '--imager-imsize',
        dest='imager_imsize',
        type=str,
        default='1080x1920',
        help='Imager image size to download',
    )
    return parser.parse_args()


def main() -> None:
    """ Application entrypoint. """

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    args = _parse_args()

    imager_client = ImagerClient(
        internal_addr=args.imager_internal,
        public_addr=args.imager_public,
        download_size=args.imager_imsize,
    )

    allowed_chats = set()
    if args.allowed_chats != '':
        allowed_chats = args.allowed_chats.split(',')
        allowed_chats = set(map(int, allowed_chats))

    imager_handler = ImagerMessageHandler(
        task_handlers=(
            UnsplashTaskHandler(args.unsplash, imager_client),
        ),
        allowed_chats=allowed_chats,
    )

    updater = Updater(args.telegram, use_context=True)
    updater.dispatcher.add_handler(
        CommandHandler(
            'start',
            imager_handler.handle_message,
        ),
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

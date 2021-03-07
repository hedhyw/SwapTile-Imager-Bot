#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Unsplash handler. """


from typing import Dict, Any
from io import BytesIO
import re
import requests
import logging
import time

from app.handler import TaskHandler, Reply
from app.imager import ImagerClient, ConflictException
from telegram.utils.helpers import escape_markdown


UNSPLASH_PHOTOS_PREFFIX = 'https://unsplash.com/photos/'
UNSPLASH_API_PREFFIX = 'https://api.unsplash.com/photos/'


class UnsplashTaskHandler(TaskHandler):
    """ Unsplash handler downloads image from unsplash by url and
        uploads it to the imager server.
    """

    def __init__(
        self,
        client_id: str,
        imager: ImagerClient,
        sleep: int,
    ) -> None:
        self._logger = logging.getLogger('UnsplashTaskHandler')

        self._urls_re = re.compile(r'(' + UNSPLASH_PHOTOS_PREFFIX + r'[\w-]+)')
        self._id_re = re.compile(UNSPLASH_PHOTOS_PREFFIX + r'([\w-]+)')
        self._client_id = client_id
        self._imager = imager
        self._sleep = sleep

    def handle(self, category: str, message: str, reply: Reply) -> bool:
        """ Handle telegram message. """

        urls = self._urls_re.findall(message)
        if not urls:
            return False

        for i, url in enumerate(urls):
            if i > 0:
                time.sleep(self._sleep)

            self._logger.debug(f'handling: {url}, category: {category}')

            try:
                self._handle_url(
                    category=category,
                    url=url,
                    reply=reply,
                    num=i+1,
                    total=len(urls),
                )
            except Exception as ex:
                self._logger.exception(ex)

                reply(f'`{escape_markdown(url)}`: failed to handle: {ex}')

        return True

    def _handle_url(
        self,
        category: str,
        url: str,
        reply: Reply,
        num: int,
        total: int,
    ) -> None:
        image_id = self._id_re.findall(url)[0]
        image_info = self._fetch_image_info(image_id)
        image_bytes = self._download_image(image_info)

        websource = f'{UNSPLASH_PHOTOS_PREFFIX}{image_id}'
        author = image_info.get('user', {}).get('name', '')
        try:
            download_url = self._imager.upload_image(
                id=f'unsplash_{image_id}',
                category=category,
                author=author,
                websource=websource,
                image_bytes=image_bytes,
            )
            download_url_text = escape_markdown(download_url)
            reply(
                f'{num}/{total}: `{image_id}`: [uploaded]({download_url_text})'
            )

            self._logger.debug(
                f'download url of {image_id} is {download_url}',
            )
        except ConflictException:
            reply(f'{num}/{total}: `{image_id}`: already found')

            self._logger.debug(
                f'image {image_id} already found',
            )

            return

    def _fetch_image_info(self, image_id: str) -> Dict[str, Any]:
        url = UNSPLASH_API_PREFFIX + image_id
        data = {
            'client_id': self._client_id,
        }

        self._logger.debug(f'requesting GET {url}: {data}')

        response = requests.get(url, data)

        self._logger.debug(f'respond {response.status_code}')

        if response.status_code != 200:
            raise Exception(f'{response.status_code}: {response.content}')

        return response.json()

    def _download_image(self, image_info: Dict[str, Any]) -> BytesIO:
        link_download = image_info.get('links', {}).get('download', '')

        self._logger.debug(f'requesting GET {link_download}')

        response = requests.get(link_download)

        self._logger.debug(f'respond {response.status_code}')

        if response.status_code != 200:
            raise Exception(f'{response.status_code}: {response.content}')

        return BytesIO(response.content)

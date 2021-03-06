#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Unsplash handler. """


from typing import Dict, Any
from io import BytesIO
import re
import requests

from app.handler import TaskHandler
from app.imager import ImagerClient, ConflictException


UNSPLASH_PHOTOS_PREFFIX = 'https://unsplash.com/photos/'
UNSPLASH_API_PREFFIX = 'https://api.unsplash.com/photos/'


class UnsplashTaskHandler(TaskHandler):
    """ Unsplash handler downloads image from unsplash by url and
        uploads it to the imager server.
    """

    def __init__(self, client_id: str, imager: ImagerClient) -> None:
        self._urls_re = re.compile(r'(' + UNSPLASH_PHOTOS_PREFFIX + r'\w+)')
        self._id_re = re.compile(UNSPLASH_PHOTOS_PREFFIX + r'(\w+)')
        self._client_id = client_id
        self._imager = imager

    def handle(self, category: str, message: str) -> bool:
        """ Handle telegram message. """

        urls = self._urls_re.findall(message)
        if not urls:
            return False

        for url in urls:
            try:
                self._handle_url(category, url)
            except Exception as ex:
                raise Exception(f'handling `{url}`: {ex}') from ex

        return True

    def _handle_url(self, category: str, url: str) -> None:
        image_id = self._id_re.findall(url)[0]
        image_info = self._fetch_image_info(image_id)
        image_bytes = self._download_image(image_info)

        websource = f'{UNSPLASH_PHOTOS_PREFFIX}{image_id}'
        author = image_info.get('user', {}).get('name', '')
        try:
            self._imager.upload_image(
                id=f'unsplash_{image_id}',
                category=category,
                author=author,
                websource=websource,
                image_bytes=image_bytes,
            )
        except ConflictException:
            pass

    def _fetch_image_info(self, image_id: str) -> Dict[str, Any]:
        response = requests.get(UNSPLASH_API_PREFFIX + image_id, {
            'client_id': self._client_id,
        })
        if response.status_code != 200:
            raise Exception(f'{response.status_code}: {response.content}')

        return response.json()

    @staticmethod
    def _download_image(image_info: Dict[str, Any]) -> BytesIO:
        link_download = image_info.get('links', {}).get('download', '')

        response = requests.get(link_download)
        return BytesIO(response.content)

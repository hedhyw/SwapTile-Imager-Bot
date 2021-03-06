#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" ImagerClient definition. """

import io

import requests
from PIL import Image


API_PATH_UPLOAD = '/internal/api/v1/images'
OUT_IMAGE_NAME = 'image.webp'
OUT_IMAGE_MIMETYPE = 'image/webp'
OUT_IMAGE_FORMAT = 'WebP'


class ConflictException(Exception):
    """Exception means that an entity already exists. """


class ImagerClient:
    """ ImagerClient is a http client to the imager server. """

    def __init__(self, addr: str) -> None:
        self._url_upload = addr + API_PATH_UPLOAD

    def upload_image(
        self,
        id: str,
        author: str,
        websource: str,
        category: str,
        image_bytes: io.BytesIO,
    ):
        """ Upload an image to the imager server. """

        image = Image.open(image_bytes)
        converted_image_bytes = io.BytesIO()
        image.save(converted_image_bytes, OUT_IMAGE_FORMAT)
        converted_image_bytes.seek(0)

        response = requests.put(
            self._url_upload,
            files={
                'image': (
                    OUT_IMAGE_NAME,
                    converted_image_bytes,
                    OUT_IMAGE_MIMETYPE,
                ),
            },
            data={
                'id': id,
                'author': author,
                'websource': websource,
                'category': category,
            },
        )
        if response.status_code == 405:
            raise ConflictException(
                f'{response.status_code}: {response.content}',
            )
        if response.status_code != 200:
            raise Exception(
                f'{response.status_code}: {response.content}',
            )

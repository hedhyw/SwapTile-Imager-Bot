#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" ImagerClient definition. """

import io
import logging

import requests
from PIL import Image


API_PATH_UPLOAD = '/internal/api/v1/images'
API_PATH_DOWNLOAD_TMPL = '/api/v1/images/{id}/{size}'
OUT_IMAGE_NAME_PREFFIX = 'image.'
OUT_IMAGE_MIMETYPE_PREFFIX = 'image/'


class ConflictException(Exception):
    """Exception means that an entity already exists. """


class ImagerClient:
    """ ImagerClient is a http client to the imager server. """

    def __init__(
        self,
        internal_addr: str,
        public_addr: str,
        download_size: str,
        format: str,
    ) -> None:
        self._logger = logging.getLogger('ImagerClient')

        self._url_upload = internal_addr + API_PATH_UPLOAD
        self._url_download_tmpl = public_addr + API_PATH_DOWNLOAD_TMPL
        self._download_size = download_size
        self._format = format

    def upload_image(
        self,
        id: str,
        author: str,
        websource: str,
        category: str,
        image_bytes: io.BytesIO,
    ) -> str:
        """ Upload an image to the imager server. """

        image = Image.open(image_bytes)
        converted_image_bytes = io.BytesIO()
        image.save(converted_image_bytes, self._format)
        converted_image_bytes.seek(0)

        data = {
            'id': id,
            'author': author,
            'websource': websource,
            'category': category,
        }

        self._logger.debug(f'requesting PUT {self._url_upload}: {data}')

        response = requests.put(
            self._url_upload,
            files={
                'image': (
                    OUT_IMAGE_NAME_PREFFIX+self._format.lower(),
                    converted_image_bytes,
                    OUT_IMAGE_MIMETYPE_PREFFIX+self._format.lower(),
                ),
            },
            data=data,
        )

        self._logger.debug(
            f'respond {response.status_code} {response.content}',
        )

        if response.status_code == 409:
            raise ConflictException(
                f'{response.status_code}: {response.content}',
            )
        if response.status_code != 200:
            raise Exception(
                f'{response.status_code}: {response.content}',
            )

        return self._url_download_tmpl.format(
            id=id,
            size=self._download_size,
        )

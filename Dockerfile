FROM python:3.9.1-alpine3.13

WORKDIR /usr/src/app

# Those dependencies are required by PILLOW.
RUN apk add --no-cache zlib-dev jpeg-dev build-base

COPY . .
RUN make prepare

ENTRYPOINT [ "make" ]
CMD [ "run" ]

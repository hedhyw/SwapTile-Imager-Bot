# SwapTile-Imager-Bot
The bot for uploading images to [SwapTile-Imager](https://github.com/ocmoxa/SwapTile-Imager) by unsplash url.

# Usage:

```sh
export UNSPLASH_CLIENT_ID=<YOUR_UNSPLASH_CLIENT_ID>
export TELEGRAM_TOKEN=<YOUR_TG_TOKEN>
export IMAGER_ADDR=http://localhost:8081

make prepare
make run
```

Open a chat with the bot and send the message like this:
```
#category_name

https://unsplash.com/photos/0m-cPyH_WDU
https://unsplash.com/photos/Uy4_uNnNHDU
```

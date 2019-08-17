from __future__ import print_function
from __future__ import unicode_literals

import asyncio
import os
import time

from aiohttp import ClientSession

DEFAULT_API_URL = 'http://127.0.0.2:80'
DEFAULT_BOT_TOKEN = '1234567:xxxxxxxxx'
DEFAULT_RPS = 100
DEFAULT_CHAT_ID = 1234567

BOT_TOKEN = os.environ.get('BOT_TOKEN')
BOT_TOKEN = DEFAULT_BOT_TOKEN if not BOT_TOKEN else BOT_TOKEN
API_URL = os.environ.get('API_URL')
API_URL = DEFAULT_API_URL if not API_URL else API_URL
CHAT_ID = os.environ.get('CHAT_ID')
CHAT_ID = DEFAULT_CHAT_ID if not CHAT_ID else CHAT_ID
RPS = os.environ.get('RPS')
CHAT_ID = DEFAULT_RPS if not RPS else RPS


def generate_api_request():
    method = 'sendMessage'
    chat_id = CHAT_ID
    text = f'{time.time()}'
    return f'{method}?chat_id={chat_id}&text={text}'


async def flood_loop(delay: float = 0.01):
    async with ClientSession() as session:
        while True:
            request = f'/bot{BOT_TOKEN}/{generate_api_request()}'
            async with session.post(f'{API_URL}{request}') as resp:
                print(resp.status)
                # print(await resp.text())
            await asyncio.sleep(delay)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Floods requests using chatid and token')
    parser.add_argument('--id', type=int, default=CHAT_ID, help='chat id')
    parser.add_argument('--url', type=str, default=API_URL, help='api url')
    parser.add_argument('--token', type=str, default=BOT_TOKEN, help='bot token')
    parser.add_argument('--rps', type=int, default=RPS, help='requests per second')
    args = parser.parse_args()
    BOT_TOKEN, API_URL, CHAT_ID, RPS = args.token, args.url, args.id, args.rps

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(flood_loop(delay=1.0/RPS))
    except KeyboardInterrupt:
        pass
    loop.close()

import asyncio

from aiohttp import web, ClientSession

API_URL = 'https://api.telegram.org'
MAX_QUEUE_SIZE = 100
HOST_PORT = 80
HOST_ADDR = '127.0.0.2'
RPS = 10
routes = web.RouteTableDef()
app = web.Application()
requests_pool = []
lock = asyncio.Lock()
event = asyncio.Event()


async def on_startup(app):
    loop = asyncio.get_event_loop()
    loop.create_task(send_loop(1.0/RPS))


async def send_loop(delay: float = 0.1):
    async with ClientSession() as session:
        while True:
            request = None
            queue_size = 0
            async with lock:
                while len(requests_pool) > MAX_QUEUE_SIZE:
                    requests_pool.pop(0)
                queue_size = len(requests_pool)
                if queue_size > 0:
                    request = requests_pool.pop()
            if request:
                async with session.post(f'{API_URL}{request}') as resp:
                    print(resp.status)
                    print(await resp.text())
            if queue_size == 0:
                await event.wait()
            else:
                await asyncio.sleep(delay)


@routes.post('/{bot_token}/{request}')
async def handle_post(request):
    request_path_qs = request.path_qs
    async with lock:
        if request_path_qs in requests_pool:
            return web.Response(status=429)
        else:
            requests_pool.append(request_path_qs)
            event.set()
            return web.Response(status=200)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Handles synchronous requests and sends them asynchronously')
    parser.add_argument('--size', type=int, default=MAX_QUEUE_SIZE, help='max queue size')
    parser.add_argument('--rps', type=int, default=RPS, help='requests per second')
    parser.add_argument('--host', type=str, default=HOST_ADDR, help='host address')
    parser.add_argument('--port', type=str, default=HOST_PORT, help='host port')
    args = parser.parse_args()
    MAX_QUEUE_SIZE, RPS, HOST_ADDR, HOST_PORT = args.size, args.rps, args.host, args.port

    app.router.add_routes(routes)
    app.on_startup.append(on_startup)
    web.run_app(app, host=HOST_ADDR, port=HOST_PORT)

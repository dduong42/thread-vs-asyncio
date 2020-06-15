#!/usr/bin/env python3

import asyncio
import signal

import constants as c


async def send_long_request():
    reader, writer = await asyncio.open_connection(c.HOSTNAME, c.PORT_SERVICE)
    writer.write(b'1')
    await writer.drain()
    await reader.read(1)


async def handle(reader, writer):
    cmd = await reader.read(1)
    if cmd == c.LONG:
        await send_long_request()
    writer.write(b'1')
    await writer.drain()
    writer.close()


async def serve():
    server = await asyncio.start_server(handle, c.HOSTNAME, c.PORT)
    server.get_loop().add_signal_handler(signal.SIGTERM, server.close)

    try:
        await server.serve_forever()
    except asyncio.CancelledError:
        pass
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(serve())

import asyncio

import constants as c


class Service:
    def __init__(self, latency):
        self.latency = latency
        self.loop = None
        self.server = None

    async def handle(self, reader, writer):
        await reader.read(1)
        await asyncio.sleep(self.latency)
        writer.write(b'1')
        await writer.drain()
        writer.close()

    def init_server(self):
        self.loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self.handle, c.HOSTNAME, c.PORT_SERVICE, loop=self.loop)
        self.server = loop.run_until_complete(coro)

    def close(self):
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.close()

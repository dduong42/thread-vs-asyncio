import asyncio
import signal

import constants as c


class Service:
    def __init__(self, latency: int):
        # latency is in ms
        self.latency = latency/1000

    async def handle(self, reader, writer):
        await reader.read(1)
        await asyncio.sleep(self.latency)
        writer.write(b'1')
        await writer.drain()
        writer.close()

    async def serve(self):
        server = await asyncio.start_server(self.handle, c.HOSTNAME, c.PORT_SERVICE)
        server.get_loop().add_signal_handler(signal.SIGTERM, server.close)

        try:
            await server.serve_forever()
        except asyncio.CancelledError:
            pass
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print('Usage: service latency', file=sys.stderr)
        sys.exit(64)

    service = Service(int(sys.argv[1]))
    asyncio.run(service.serve())

import asyncio


class ItemQueue:

    def __init__(self):
        self.queue = asyncio.Queue(maxsize=5000)

    async def put(self, item: bytes):
        await self.queue.put(item)

    async def get(self) -> bytes:
        return await self.queue.get()

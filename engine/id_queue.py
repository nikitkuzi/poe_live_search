import asyncio


class IDQueue:

    def __init__(self):
        # holds item IDs received from live search
        self.queue = asyncio.LifoQueue(maxsize=10000)

    async def put(self, search_id:str, item_id: str) -> None:
        await self.queue.put((search_id, item_id))

    async def get(self) -> tuple[str,str]:
        return await self.queue.get()
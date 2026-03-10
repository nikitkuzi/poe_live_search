from __future__ import annotations
from network.http_client import HTTPClient
from engine.id_queue import IDQueue
from engine.item_queue import ItemQueue


async def fetch_worker(client: HTTPClient, id_queue: IDQueue, item_queue: ItemQueue):
    while True:

        search_id, item_id = await id_queue.get()

        url = f"https://www.pathofexile.com/api/trade/fetch/{item_id}?query={search_id}"

        try:
            data = await client.get(url)

            # push fetched data to processing queue
            await item_queue.put(data)

        except Exception as e:
            print("Fetch error:", e)


import asyncio


async def start_fetch_workers(client: HTTPClient, worker_count: int, id_queue: IDQueue, item_queue: ItemQueue):
    tasks = []

    for _ in range(worker_count):
        tasks.append(
            asyncio.create_task(
                fetch_worker(client, id_queue, item_queue)
            )
        )

    await asyncio.gather(*tasks)

import asyncio

from config import config
from network.http_client import HTTPClient

from engine.id_queue import IDQueue
from engine.item_queue import ItemQueue
from engine.livestream import start_live_stream_ws
from engine.fetch_workers import start_fetch_workers
from engine.processor import processor_loop


async def main():

    client = HTTPClient(config.SESSION)

    id_queue = IDQueue()
    item_queue = ItemQueue()

    tasks = []

    for search_id in config.SEARCH_IDS:

        # WebSocket listener
        tasks.append(
            asyncio.create_task(
                start_live_stream_ws(client, search_id, config.LEAGUE ,id_queue)
            )
        )

    # Fetch workers
    tasks.append(
        asyncio.create_task(
            start_fetch_workers(
                client,
                6,
                id_queue,
                item_queue
            )
        )
    )

    # SINGLE processor
    tasks.append(
        asyncio.create_task(
            processor_loop(client, item_queue)
        )
    )

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
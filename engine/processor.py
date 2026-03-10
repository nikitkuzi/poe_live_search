from __future__ import annotations
import json
from network.http_client import HTTPClient
from engine.item_queue import ItemQueue


def process_item_sync(client: HTTPClient, data: bytes) -> None:
    try:
        parsed = json.loads(data)
    except Exception as e:
        print(f"couldn't process item: {data}\n{e}")
        return

    print("Item received:", len(data), data)
    # print(parsed)
    # print(type(parsed))
    # print(parsed["result"])
    for item in parsed.get("result", []):
        try:
            if "whisper_token" in item["listing"]:
                print(f"whisper_token: {item["listing"]["whisper_token"]}")
            else:

                hideout_token = item["listing"]["hideout_token"]
                print(f"hideout_token: {hideout_token}")
                url = "https://www.pathofexile.com/api/trade/whisper"
                payload = {"token": hideout_token}
                travel = client.post(url, json=payload)
                # exit(0)
        except Exception as e:
            print(f"couldn't process item: {item} in {parsed}\n{e}")
    while True:
        a = input()
        break
    print("processing finished")


import asyncio


async def processor_loop(client: HTTPClient, item_queue: ItemQueue) -> None:
    while True:
        item_data = await item_queue.get()

        # run sync processing without blocking event loop
        await asyncio.to_thread(process_item_sync, client, item_data)

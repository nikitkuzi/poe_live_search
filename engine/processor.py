from __future__ import annotations
from network.http_client import HTTPClient
from engine.item_queue import ItemQueue
import json
import mouse

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
            wisp = False
            x = item["listing"]["stash"]["x"]
            y = item["listing"]["stash"]["y"]
            if "whisper_token" in item["listing"]:
                token = item["listing"]["whisper_token"]
                wisp = True
                print(f"whisper_token: {token}")
                print("successfully send whisper")
                # continue
            else:

                token = item["listing"]["hideout_token"]
                print(f"hideout_token: {token}")
            url = "https://www.pathofexile.com/api/trade/whisper"
            payload = {"token": token}
            travel = client.post(url, json=payload)
            if wisp:
                continue
            if "false" in travel.text:
                with open("data/positions.json", 'r') as f:
                    positions = json.load(f)
                    mouse.move(*positions["faustus_window"][f"({x},{y})"])
                print("Item sold")
                continue
            print(x,y)
            #simulate auto buy
            with open("data/positions.json", 'r') as f:
                positions = json.load(f)
                mouse.move(*positions["faustus_window"][f"({x},{y})"])
            _ = input()
            # exit(0)
        except Exception as e:
            print(f"couldn't process item: {item} in {parsed}\n{e}")
    print("processing finished")


import asyncio


async def processor_loop(client: HTTPClient, item_queue: ItemQueue) -> None:
    while True:
        item_data = await item_queue.get()

        # run sync processing without blocking event loop
        await asyncio.to_thread(process_item_sync, client, item_data)

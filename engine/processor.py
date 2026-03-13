from __future__ import annotations

from network.http_client import HTTPClient
from engine.item_queue import ItemQueue
from engine.buyer import buy_item
import json


def process_item_sync(client: HTTPClient, data: bytes, afk: bool = True, playing: bool = False) -> None:
    try:
        parsed = json.loads(data)
    except Exception as e:
        print(f"couldn't process item: {data}\n{e}")
        return

    print("Item received:", len(data), data)

    for item in parsed.get("result", []):
        try:
            whisper = False
            x = item["listing"]["stash"]["x"]
            y = item["listing"]["stash"]["y"]
            price = item["listing"]["price"]["amount"]
            currency = item["listing"]["price"]["currency"]

            if "whisper_token" in item["listing"]:
                token = item["listing"]["whisper_token"]
                whisper = True
                print(f"whisper_token: {token}")
                if afk:
                    print("afk, not sending whisper")
                    continue
                print("successfully send whisper")
            else:
                token = item["listing"]["hideout_token"]
                print(f"hideout_token: {token}")
                if playing:
                    print("playing, not teleporting")
                    continue

            url = "https://www.pathofexile.com/api/trade/whisper"
            payload = {"token": token}
            travel = client.post(url, json=payload)
            if whisper:
                continue



            payload["continue"] = "true"
            in_demand = None
            if "message" not in travel.text:
                in_demand = client.post(url, json=payload)

            print("travel_response", travel.text)
            if in_demand is not None:
                print("in_demand_response", in_demand.text)
            # continue
            if ("false" in travel.text or "error" in travel.text) and (in_demand is not None and ("false" in in_demand.text or "error" in in_demand.text)):
                print("Item sold")
                continue

            # simulate auto buy
            status = buy_item(x, y)
            if status:
                print(f"Item bought for {price} {currency}")
            else:
                print("Failed to buy item")

        except Exception as e:
            print(f"couldn't process item: {item} in {parsed}\n{e}")
    print("processing finished")
    print()


import asyncio


async def processor_loop(client: HTTPClient, item_queue: ItemQueue, afk:bool, playing:bool) -> None:
    while True:
        item_data = await item_queue.get()

        # run sync processing without blocking event loop
        await asyncio.to_thread(process_item_sync, client, item_data, afk, playing)

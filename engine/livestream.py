from __future__ import annotations
import asyncio
import json
import aiohttp
import orjson

from network.http_client import HTTPClient
from engine.id_queue import IDQueue


async def start_live_stream_ws(client: HTTPClient, search_id: str, league: str, queue: IDQueue):
    url = f"wss://www.pathofexile.com/api/trade/live/{league}/{search_id}"

    while True:
        try:
            async with client.ws_connect(url) as ws:
                print(f"[WS] Connected to search {search_id}")

                async for msg in ws:

                    if msg.type == aiohttp.WSMsgType.TEXT:
                        # if "result" in msg.data:
                        if msg.data[2:8] == "result":

                            try:
                                event = orjson.loads(msg.data)
                                item_token = event.get("result")
                                if item_token:
                                    await queue.put(search_id, item_token)
                            except json.JSONDecodeError:
                                continue
                        else:
                            continue
                    elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                        print(f"[WS] Connection closed or error for search {search_id}")
                        break

        except Exception as e:
            print(f"[WS] Error in search {search_id}: {e}")

        print(f"[WS] Reconnecting search {search_id} in 3s...")
        await asyncio.sleep(3)

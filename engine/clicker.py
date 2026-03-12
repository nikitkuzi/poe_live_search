import asyncio
import mouse

async def start_clicker():
    while True:
        mouse.click(button="right")
        await asyncio.sleep(60)
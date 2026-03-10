# network/http_client.py
import aiohttp
import requests
from typing import AsyncContextManager
from aiohttp import ClientWebSocketResponse

CF = 'jDSdS5pCwAeTo8Yn7bnofIG5HtFmhkMeEzJMwqn0akw-1773080987-1.2.1.1-w0VIBLvNe4qJJ3GMwqb8BZH16.BM1WDAmPZQtVxt9yKrTxBbWo7l3eEu4q8P68tPcwSDJBnje8Y.PclqGmMaC3lZ30HGrU_v7dLG6AOIIsNf_jbax62dHlQavEvQyTEM1UnNrt5ktge5Y9B7TXJ2QI7i_8duaS2ohR.PC0iK6eF.4Et1rKrE8VXmAwhImwfs1JXUrQwnQVb89TnjZt0DAvMezqQKZ5sjbpm4kPOzF9r4e06deF4l9IVbTHSKXBGT'


class HTTPClient:
    def __init__(self, session_cookie: str):
        self.session_cookie = session_cookie
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "Origin": "https://www.pathofexile.com",
            "Cookie": f'POESESSID={session_cookie}',  # ; cf_clearance={CF}',
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.session = aiohttp.ClientSession(
            headers=self.headers
        )

    async def get(self, url: str) -> bytes:
        async with self.session.get(url) as resp:
            return await resp.read()

    def post(self, url: str, **kwargs) -> bytes:
        resp = requests.post(url, headers=self.headers, **kwargs)
        return resp.content

    # Fix: don't await here; return the context manager object
    def ws_connect(self, url: str) -> AsyncContextManager[ClientWebSocketResponse]:
        return self.session.ws_connect(url)

    async def close(self) -> None:
        await self.session.close()

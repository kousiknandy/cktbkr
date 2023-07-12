import aiohttp
import asyncio

from web_client import fetch_url_carefully, fetch_url_carelessly


async def main():
    for fetch_url in [fetch_url_carefully, fetch_url_carelessly]:
        async with aiohttp.ClientSession() as client:
            tasks = [
                asyncio.create_task(fetch_url(client, "http://localhost:8080/foo", n))
                for n in range(0, 25)
            ]
            r = await asyncio.gather(*tasks)
        print(*r, sep=",")

asyncio.run(main())

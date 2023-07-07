import aiohttp
import asyncio

from web_client import fetch_url


async def main():
    async with aiohttp.ClientSession() as client:
        tasks = [
            asyncio.create_task(fetch_url(client, "http://localhost:8080/foo", n))
            for n in range(0, 20)
        ]
        r = await asyncio.gather(*tasks)
    print(*r, sep="\n")

asyncio.run(main())

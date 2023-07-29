import aiohttp
import asyncio

from web_client import fetch_url_carefully, fetch_url_carelessly


async def exec_late(delay, corof):
    await asyncio.sleep(delay)
    return await corof


async def main():
    async with aiohttp.ClientSession() as client:
        tasks = [
            asyncio.create_task(
                exec_late(
                    n // 2,
                    fetch_url_carefully(
                        client, f"http://localhost:8080/{('foo', 'bar')[n % 2]}", n
                    ),
                )
            )
            for n in range(0, 32)
        ]
        r = await asyncio.gather(*tasks)
    print(*r, sep=",")

    async with aiohttp.ClientSession() as client:
        tasks = [
            asyncio.create_task(
                exec_late(
                    n,
                    fetch_url_carelessly(
                        client, f"http://localhost:8080/{('foo', 'bar')[n % 2]}", n
                    ),
                )
            )
            for n in range(0, 32)
        ]
        r = await asyncio.gather(*tasks)
    print(*r, sep=",")


asyncio.run(main())

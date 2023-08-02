import asyncio
import aiohttp

from circuitbreaker import Circuitbreaker

@Circuitbreaker("serial")
async def get_url(url):
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as page:
            assert page.status == 200
            print("Succeess")

async def main():
    for i in range(32):
        t = asyncio.create_task(get_url("http://localhost:8080/foo"))
        await asyncio.gather(t)
        await asyncio.sleep(1)

asyncio.run(main())

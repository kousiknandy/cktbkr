import aiohttp
import asyncio

from circuitbreaker import Circuitbreaker, CircuitOpenException

async def fetch_url(client_session, url, id):
    await asyncio.sleep(id % 10)
    print(id, "fetching >>>")
    try:
        with Circuitbreaker(url):
            async with client_session.get(url) as page:
                assert page.status == 200
                print(id, "done!")
                return await page.text()
    except CircuitOpenException:
        print(id, "Circuit open!")
    return None

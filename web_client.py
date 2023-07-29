import aiohttp
import asyncio

from circuitbreaker import Circuitbreaker, CircuitOpenException


async def fetch_url_carefully(client_session, url, id):
    """Be aware of the Circuitbreaker and use as context"""
    print(id, "Start >>>", end=" ")
    try:
        with Circuitbreaker(url, retries=3, timeout=10):
            print(id, f"fetching {url.split('/')[-1]} >>>")
            async with client_session.get(url) as page:
                assert page.status == 200
                print(id, "done!")
                return await page.text()
    except CircuitOpenException:
        pass
    return None


@Circuitbreaker("careless", retries=3)
async def fetch_url_carelessly(client_session, url, id):
    """Unaware of context manager and hence wrapped by one"""
    print(id, "Start >>>", end=" ")
    print(id, f"fetching {url.split('/')[-1]} >>>")
    async with client_session.get(url) as page:
        assert page.status == 200
        print(id, "done!")
        return await page.text()
    return None

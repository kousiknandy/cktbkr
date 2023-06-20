import aiohttp


async def fetch_url(client_session, url, id):
    print(id, "fetching >>>")
    async with client_session.get(url) as page:
        assert page.status == 200
        print(id, "done!")
        return await page.text()

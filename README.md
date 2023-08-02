# Circuit Breaker

Python implementation of a circuit breaker pattern

### Usage:

```
from circuitbreaker import Circuitbreaker
```

Have per url (or hostname) circuitbreaker

``` python
with Circuitbreaker(hostname, retries=...):
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as page:
            ...
```

or, protect entire function (e.g all fetches)

``` python
@Circuitbreaker("whateversomeidentifier")
async def get_url(url):
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as page:
            ...
```

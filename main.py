import aiohttp
import asyncio
import time

def timeit_wrapper(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()  # Alternatively, you can use time.process_time()
        func_return_val = func(*args, **kwargs)
        end = time.perf_counter()
        print('{0:<10}.{1:<8} : {2:<8}'.format(func.__module__, func.__name__, end - start))
        return func_return_val
    return wrapper

@timeit_wrapper
async def fetch(session, url):
    async with session.get(url) as response:
    # async with session.get(url, ssl=ssl.SSLContext()) as response:
        # return await response.json()
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html1 = await fetch(session, 'http://google.com')

    # async with aiohttp.ClientSession() as session:
        html2 = await fetch(session, 'http://python.org')

    # async with aiohttp.ClientSession() as session:
        html2 = await fetch(session, 'http://cnn.com')

async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    loop2 = asyncio.get_event_loop()
    urls = ['http://google.com', 'http://python.org', 'http://cnn.com']
    htmls = loop2.run_until_complete(fetch_all(urls, loop2))
    print([len(each_html) for each_html in htmls])
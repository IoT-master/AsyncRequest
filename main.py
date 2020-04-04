import aiohttp
import asyncio
import time
import ujson

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
    # async with aiohhtp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
        # return await response.json()

        # with open(filename, 'wb') as fd:
        # while True:
        #     chunk = await resp.content.read(chunk_size)
        #     if not chunk:
        #         break
        #     fd.write(chunk)

        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html1 = await fetch(session, 'http://google.com')
        html2 = await fetch(session, 'http://python.org')
        html2 = await fetch(session, 'http://cnn.com')

    # async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
    #     async with session.post(json={'test': 'object})
    #     async with session.put('http://httpbin.org/put', data=b'data')
    #     async with session.post('http://httpbin.org/post', data=b'data')
    #     async with session.delete('http://httpbin.org/delete')
    #     async with session.head('http://httpbin.org/get')
    #     async with session.options('http://httpbin.org/get')
    #     async with session.patch('http://httpbin.org/patch', data=b'data')

    #     params = {'key1': 'value1', 'key2': 'value2'}
    #     async with session.get('http://httpbin.org/get',params=params) as resp:
    #         assert str(resp.url) == 'http://httpbin.org/get?key2=value2&key1=value1'
        
    #     params = [('key', 'value1'), ('key', 'value2')]
    #     async with session.get('http://httpbin.org/get', params=params) as r:
    #         assert str(r.url) == 'http://httpbin.org/get?key=value2&key=value1'

    #     url = 'https://api.github.com/some/endpoint'
    #     payload = {'some': 'data'}
    #     headers = {'content-type': 'application/json'}
    #     await session.post(url, data=ujson.dumps(payload), headers=headers)

    #     payload = {'key1': 'value1', 'key2': 'value2'}
    #     async with session.post('http://httpbin.org/post', data=payload) as resp:
    #         print(await resp.text())

    #     url = 'http://httpbin.org/post'
    #     files = {'file': open('report.xls', 'rb')}
    #     await session.post(url, data=files)

    # async with aiohttp.ClientSession() as session:
    #     async with session.get("http://python.org",
    #                         proxy="http://some.proxy.com") as resp:
    #         print(resp.status)

    # async with aiohttp.ClientSession(
    #     headers={"Authorization": "Basic bG9naW46cGFzcw=="}) as session:
    #     async with session.get("http://httpbin.org/headers") as r:
    #         json_body = await r.json()
    #         assert json_body['headers']['Authorization'] == \
    #             'Basic bG9naW46cGFzcw=='

    # url = 'http://httpbin.org/cookies'
    # cookies = {'cookies_are': 'working'}
    # async with ClientSession(cookies=cookies) as session:
    #     async with session.get(url) as resp:
    #         assert await resp.json() == {
    #         "cookies": {"cookies_are": "working"}}


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
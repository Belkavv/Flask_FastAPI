import os
import time
import requests
import asyncio
import aiohttp
import concurrent.futures
from flask import Flask, request, jsonify
from multiprocessing import Pool
from urllib.parse import urlparse
from argparse import ArgumentParser

app = Flask(__name__)

def download_image(url):
    start_time = time.time()
    response = requests.get(url)
    filename = os.path.basename(urlparse(url).path)
    with open(filename, 'wb') as f:
        f.write(response.content)
    end_time = time.time()
    return filename, end_time - start_time

async def async_download_image(session, url):
    start_time = time.time()
    async with session.get(url) as response:
        content = await response.read()
        filename = os.path.basename(urlparse(url).path)
        with open(filename, 'wb') as f:
            f.write(content)
    end_time = time.time()
    return filename, end_time - start_time

@app.route('/download', methods=['POST'])
def download_images():
    urls = request.json.get('urls', [])
    if not urls:
        return jsonify({"error": "No URLs provided"}), 400

    results = []

    # Multithreading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_image, url) for url in urls]
        results.extend([future.result() for future in concurrent.futures.as_completed(futures)])

    # Multiprocessing
    with Pool() as pool:
        results.extend(pool.map(download_image, urls))

    # Asynchronous
    async def async_download_all(urls):
        async with aiohttp.ClientSession() as session:
            tasks = [async_download_image(session, url) for url in urls]
            return await asyncio.gather(*tasks)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results.extend(loop.run_until_complete(async_download_all(urls)))

    total_time = sum(result[1] for result in results)
    return jsonify({
        "results": results,
        "total_time": total_time
    })

if __name__ == '__main__':
    parser = ArgumentParser(description="Download images from URLs")
    parser.add_argument('urls', metavar='URL', type=str, nargs='*', help='URLs of images to download')
    args = parser.parse_args()

    if args.urls:
        # Если URL-адреса переданы через командную строку, скачиваем изображения и выводим результаты
        urls = args.urls
        results = []

        # Multithreading
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(download_image, url) for url in urls]
            results.extend([future.result() for future in concurrent.futures.as_completed(futures)])

        # Multiprocessing
        with Pool() as pool:
            results.extend(pool.map(download_image, urls))

        # Asynchronous
        async def async_download_all(urls):
            async with aiohttp.ClientSession() as session:
                tasks = [async_download_image(session, url) for url in urls]
                return await asyncio.gather(*tasks)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results.extend(loop.run_until_complete(async_download_all(urls)))

        total_time = sum(result[1] for result in results)
        for result in results:
            print(f"Изображение сохранено как {result[0]}, время скачивания: {result[1]} секунд")
        print(f"Общее время выполнения: {total_time} секунд")
    else:
        # Если URL-адреса не переданы через командную строку, запускаем Flask-приложение
        app.run(debug=True)
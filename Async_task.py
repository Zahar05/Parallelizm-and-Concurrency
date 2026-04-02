# 3. Реализуйте асинхронный код, который отправляет 50 запросов
# по адресу http://google.com/ или https://example.com/.
# Ограничьте одновременное количество возможных запросов до 10.
# Статус-коды ответов запишите в файл. Количество запросов
# requests_amount, лимит одновременно выполняемых запросов
# requests_limit и url должны передаваться как входные аргументы
# функции.


import asyncio
import aiohttp


async def fetch(session, url, timeout_seconds=10):
    """
    Выполняет один HTTP-запрос, возвращая статус или ошибку.
    """
    try:
        async with session.get(url, timeout=timeout_seconds) as response:
            return response.status
    except Exception as e:
        return f"Error: {str(e)}"


async def main(requests_amount, requests_limit, url, output_file):
    """
    Отправляет requests_amount запросов по указанному url,
    ограничивая одновременно requests_limit запросов.
    Результаты записывает в файл.
    """
    semaphore = asyncio.Semaphore(requests_limit)

    async with aiohttp.ClientSession() as session:
        async def bounded_fetch():
            async with semaphore:
                status = await fetch(session, url)
                return status

        # Создаем ровно requests_amount задач
        tasks = [asyncio.create_task(bounded_fetch()) for _ in range(requests_amount)]

        # Ждем завершения всех задач
        results = await asyncio.gather(*tasks)

        # Запись результатов в файл
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, status in enumerate(results, 1):
                if isinstance(status, int):
                    f.write(f"Запрос {i}: {url} - Status: {status}\n")
                else:
                    f.write(f"Запрос {i}: {url} - {status}\n")


# Пример запуска:
if __name__ == "__main__":
    requests_amount = 50
    requests_limit = 10
    url = "https://example.com/"  # Один URL, как в задании
    output_file = "statuses.log"

    asyncio.run(main(requests_amount, requests_limit, url, output_file))
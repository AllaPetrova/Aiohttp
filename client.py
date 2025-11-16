import aiohttp
import asyncio
import asyncpg
from datetime import datetime

DATABASE_URL = "postgresql://user:password@localhost/db"

async def fetch_data(session, url):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Ошибка {response.status} для {url}")
                return None
    except asyncio.TimeoutError:
        print(f"Таймаут для {url}")
        return None
    except Exception as e:
        print(f"Ошибка для {url}: {e}")
        return None

async def save_to_database(data):
    if not data:
        return
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    for item in data:
        await conn.execute('''
            INSERT INTO items (id, title, description, created_at)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (id) DO UPDATE SET
                title = EXCLUDED.title,
                description = EXCLUDED.description,
                created_at = EXCLUDED.created_at
        ''', item['id'], item['title'], item.get('description'), datetime.now())
    
    await conn.close()

async def main():
    urls = [
        'https://jsonplaceholder.typicode.com/posts/1',
        'https://jsonplaceholder.typicode.com/posts/2',
        'https://jsonplaceholder.typicode.com/posts/3'
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        valid_results = [result for result in results if result is not None]
        await save_to_database(valid_results)
        
        print(f"Обработано {len(valid_results)} из {len(urls)} запросов")

if __name__ == '__main__':
    asyncio.run(main())

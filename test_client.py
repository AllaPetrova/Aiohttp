import asyncio
import aiohttp
import json


async def test_api():
    async with aiohttp.ClientSession() as session:
        # Test POST
        ad_data = {
            'title': 'Test Advertisement',
            'description': 'This is a test advertisement',
            'owner': 'test_user'
        }
        
        async with session.post('http://localhost:8080/ads', data=ad_data) as resp:
            print(f"POST Status: {resp.status}")
            created_ad = await resp.json()
            print(f"Created: {json.dumps(created_ad, indent=2)}")
            ad_id = created_ad['id']
        
        # Test GET all
        async with session.get('http://localhost:8080/ads') as resp:
            print(f"\nGET ALL Status: {resp.status}")
            ads = await resp.text()
            print("All ads page received")
        
        # Test GET one
        async with session.get(f'http://localhost:8080/ads/{ad_id}') as resp:
            print(f"\nGET ONE Status: {resp.status}")
            ad = await resp.json()
            print(f"Retrieved: {json.dumps(ad, indent=2)}")
        
        # Test PATCH
        update_data = {
            'title': 'Updated Test Advertisement',
            'description': 'This advertisement has been updated'
        }
        
        async with session.patch(f'http://localhost:8080/ads/{ad_id}', 
                               json=update_data) as resp:
            print(f"\nPATCH Status: {resp.status}")
            updated_ad = await resp.json()
            print(f"Updated: {json.dumps(updated_ad, indent=2)}")
        
        # Test DELETE
        async with session.delete(f'http://localhost:8080/ads/{ad_id}') as resp:
            print(f"\nDELETE Status: {resp.status}")


if __name__ == '__main__':
    asyncio.run(test_api())

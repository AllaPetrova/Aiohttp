from aiohttp import web
from models import Ads
import json


class AdsView(web.View):

    async def get(self):
        ad_id = self.request.match_info.get('ad_id')
        
        if ad_id:
            ad_id = int(ad_id)
            ad = await self.get_ad(ad_id)
            if not ad:
                return web.json_response({'error': 'Ad not found'}, status=404)
            return web.json_response(ad)
        else:
            ads = await self.get_all_ads()
            return web.json_response({'ads': ads})

    async def post(self):
        try:
            data = await self.request.json()
        except json.JSONDecodeError:
            return web.json_response({'error': 'Invalid JSON'}, status=400)
        
        try:
            ad_data = Ads(**data)
        except Exception as e:
            return web.json_response({'error': str(e)}, status=400)
        
        ad_id = await self.create_ad(ad_data.dict())
        return web.json_response({'id': ad_id, **ad_data.dict()}, status=201)

    async def delete(self):
        ad_id = self.request.match_info.get('ad_id')
        if not ad_id:
            return web.json_response({'error': 'Ad ID required'}, status=400)
        
        ad_id = int(ad_id)
        success = await self.delete_ad(ad_id)
        
        if not success:
            return web.json_response({'error': 'Ad not found'}, status=404)
        
        return web.json_response({'message': f'Ad {ad_id} deleted'})

    async def get_ad(self, ad_id: int):
        ads_storage = self.request.app['ads_storage']
        return ads_storage.get(ad_id)

    async def get_all_ads(self):
        ads_storage = self.request.app['ads_storage']
        return list(ads_storage.values())

    async def create_ad(self, ad_data: dict):
        ads_storage = self.request.app['ads_storage']
        ad_id = max(ads_storage.keys(), default=0) + 1
        ad_data['id'] = ad_id
        ads_storage[ad_id] = ad_data
        return ad_id

    async def delete_ad(self, ad_id: int):
        ads_storage = self.request.app['ads_storage']
        if ad_id in ads_storage:
            del ads_storage[ad_id]
            return True
        return False

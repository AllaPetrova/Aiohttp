from aiohttp import web
from aiohttp_jinja2 import template
from models import Advertisement
from sqlalchemy import desc
import json


class AdvertisementList(web.View):
    @template('ads_list.html')
    async def get(self):
        db = self.request.app['db']
        ads = db.query(Advertisement).order_by(desc(Advertisement.created_at)).all()
        return {'ads': ads}

    async def post(self):
        data = await self.request.post()
        db = self.request.app['db']
        
        ad = Advertisement(
            title=data.get('title'),
            description=data.get('description'),
            owner=data.get('owner')
        )
        
        db.add(ad)
        db.commit()
        
        return web.json_response({
            'id': ad.id,
            'title': ad.title,
            'description': ad.description,
            'owner': ad.owner,
            'created_at': ad.created_at.isoformat()
        }, status=201)


class AdvertisementDetail(web.View):
    async def get(self):
        ad_id = int(self.request.match_info['id'])
        db = self.request.app['db']
        
        ad = db.query(Advertisement).filter(Advertisement.id == ad_id).first()
        if not ad:
            return web.json_response({'error': 'Advertisement not found'}, status=404)
            
        return web.json_response({
            'id': ad.id,
            'title': ad.title,
            'description': ad.description,
            'owner': ad.owner,
            'created_at': ad.created_at.isoformat()
        })

    async def patch(self):
        ad_id = int(self.request.match_info['id'])
        db = self.request.app['db']
        
        ad = db.query(Advertisement).filter(Advertisement.id == ad_id).first()
        if not ad:
            return web.json_response({'error': 'Advertisement not found'}, status=404)
        
        data = await self.request.json()
        
        if 'title' in data:
            ad.title = data['title']
        if 'description' in data:
            ad.description = data['description']
        if 'owner' in data:
            ad.owner = data['owner']
            
        db.commit()
        
        return web.json_response({
            'id': ad.id,
            'title': ad.title,
            'description': ad.description,
            'owner': ad.owner,
            'created_at': ad.created_at.isoformat()
        })

    async def delete(self):
        ad_id = int(self.request.match_info['id'])
        db = self.request.app['db']
        
        ad = db.query(Advertisement).filter(Advertisement.id == ad_id).first()
        if not ad:
            return web.json_response({'error': 'Advertisement not found'}, status=404)
            
        db.delete(ad)
        db.commit()
        
        return web.json_response({}, status=204)

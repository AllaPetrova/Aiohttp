from aiohttp import web
import aiohttp
import asyncio
from models import Base, Item
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import json

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/db"

async def init_db():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine

async def get_items(request):
    engine = request.app['db_engine']
    async with AsyncSession(engine) as session:
        items = await session.execute(Item.__table__.select())
        result = [dict(row) for row in items]
        return web.json_response(result)

async def create_item(request):
    engine = request.app['db_engine']
    data = await request.json()
    
    async with AsyncSession(engine) as session:
        new_item = Item(**data)
        session.add(new_item)
        await session.commit()
        
        return web.json_response({'id': new_item.id, 'status': 'created'})

async def health_check(request):
    return web.json_response({'status': 'healthy', 'service': 'aiohttp_server'})

async def app_factory():
    app = web.Application()
    app.router.add_get('/items', get_items)
    app.router.add_post('/items', create_item)
    app.router.add_get('/health', health_check)
    
    app['db_engine'] = await init_db()
    
    return app

if __name__ == '__main__':
    web.run_app(app_factory(), host='0.0.0.0', port=8080)

from aiohttp import web
import aiohttp_jinja2
import jinja2
from routes import setup_routes
from models import init_db, close_db


async def create_app():
    app = web.Application()
    app['config'] = {'database': 'sqlite:///ads.db'}
    
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    
    setup_routes(app)
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host='localhost', port=8080)

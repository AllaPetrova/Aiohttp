from aiohttp import web
from routes import setup_routes


app = web.Application()
setup_routes(app)
app['ads_storage'] = {}

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)



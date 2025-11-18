from views import AdsView


def setup_routes(app):
    app.router.add_route('*', '/ads/{ad_id:\d+}', AdsView)
    app.router.add_route('*', '/ads/', AdsView)

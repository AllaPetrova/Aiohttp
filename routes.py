from views import AdvertisementList, AdvertisementDetail


def setup_routes(app):
    app.router.add_view('/ads', AdvertisementList)
    app.router.add_view('/ads/{id}', AdvertisementDetail)

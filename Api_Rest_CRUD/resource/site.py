from flask_restful import Resource
from models.site import SiteModel


class Sites(Resource):
    def  get(self):
        return {'Sites': [site.json() for site in SiteModel.query.all()]}



class Site(Resource):
    def get(self, url):
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {'message': 'Site not  find'},400

    def post(self, url):
        if SiteModel.find_site(url):
            return {"message": "Site '{}' already exists."}, 400

        site = SiteModel(url)
        try:
            site.save_site()
        except:
            return{'An internal error ocorred trying to save site'}, 500

        return site.json()

    def delete(self, url):
        site = SiteModel.find_site(url)
        if site:
            site.delete_site
            return{'message': 'Site  deleted'}
        return{"messege": "Site '{}'  not found"}, 404

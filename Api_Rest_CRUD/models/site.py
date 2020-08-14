from sql_alchemy import banco


class SiteModel(banco.Model):
    __tablename__ = 'sites'

    site_id = banco.Column(banco.Interger, primary_key=True)
    url = banco.Column(banco.String)

    def __init__(self, url):
        self.url = url


    def json(self):
        return{
            'site_id': self.site_id,
            'nome': self.url,

        }

    @classmethod
    def find_site(cls, url):
        site = cls.query.filter_by(url=url).first() #SELECT * FROM hotel_id = $hotel_id
        if site:
            return site
        return None


    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_site(self):
        banco.session.delete(self)
        banco.session.commit()

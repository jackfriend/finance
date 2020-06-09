from Scraper import Scraper
import config

Company = Scraper('1693801', config.PATH)
print(Company.zip)
print(type(Company.zip))

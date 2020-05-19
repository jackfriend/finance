from Scraper import Scraper
from config import path

Apple = Scraper('320193', path)
print(Apple.extracted_xbrl_instance)
print(Apple.schema)

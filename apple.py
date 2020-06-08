from Scraper import Scraper
from config import path

Apple = Scraper('320193', path)
print(Apple.schema)
print(Apple.adsh)
print(Apple.extracted_instance_doc)

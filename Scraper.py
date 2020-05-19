from bs4 import BeautifulSoup
import requests
import sys
import csv
from lxml import etree
import re


class Scraper:
    """
    Generate an instant of the specified company
    """

    def __init__(self, cik):
        """
        make an instant of the scaper
        """

        # TODO: This is slow.... do this in Rust:
        #   a_function(tsv_filename, key='cik', value='instance') > return a string 
        f = open('data/2020q1_notes/sub.tsv', 'r', newline='')
        reader = csv.DictReader(f, dialect='excel-tab')
        for row in reader:
            if row['cik'] == cik:
                instance = row['instance']
                adsh = row['adsh'].replace('-', '')
                break

        self.instance = instance
        self.adsh = adsh
        self.extracted_xbrl_instance = "https://www.sec.gov/Archives/edgar/data/{0}/{1}/{2}".format(cik, adsh, instance)
       
        # TODO: Add links for cal, def, lab, and pre
        self.schema = self.return_an_xbrl_doc('link:schemaRef', 'xlink:href')


    def return_an_xbrl_doc(self, tag, href):
        """
        """
        
        # TODO: add more namespaces
        ns = {
                # "": "http://www.xbrl.org/2003/instance",
                "link": "http://www.xbrl.org/2003/linkbase",
                "xlink": "http://www.w3.org/1999/xlink"
            }
        
        # the following enters into the XBRL instance document
        r = requests.get(self.extracted_xbrl_instance)
        r = r.text
        root = etree.fromstring(bytes(r, encoding='utf-8')) # bytes encodes the request into a format that lxml can read
        tag = root.find(tag, namespaces=ns) # soup is already in the root <xbrl>, so search for the next child. You can use an XPath

        # Use regex to make a etree.get() compatible attribute {www.wlink.org}href
        href = re.findall(r'\w+', href)
        href[0] = ns[href[0]]
        attribute = "{" + href[0] + "}" + href[1]

        return tag.get(attribute)


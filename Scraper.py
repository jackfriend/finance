from bs4 import BeautifulSoup
import requests as r
import sys
import csv
from zipfile import ZipFile
from lxml import etree
import re

from util import *
import config

class Scraper:
    """
    Generate an instant of the specified company
    """

    def __init__(self, cik, path):
        """
        make an instant of the scaper
        """

        # TODO: This is slow.... do this in Rust:
        f = open(path + '/sub.tsv', 'r', newline='')
        reader = csv.DictReader(f, dialect='excel-tab')
        for row in reader:
            if row['cik'] == cik and row['form'] == '10-K':
                instance = row['instance']
                adsh = row['adsh']
                break

        self.cik = cik
        self.adsh = adsh
        self.instance = {"xml": instance, "html": instance.replace('_htm.xml', '.htm')}
        self.extracted_instance_doc = "https://www.sec.gov/Archives/edgar/data/{0}/{1}/{2}".format(cik, adsh.replace('-', ''), instance)

        self.zip = unpack_zip("https://www.sec.gov/Archives/edgar/data/{0}/{1}/".format(cik, adsh.replace('-', '')),
                "{0}-xbrl.zip".format(adsh),
                config.DATA)
        # self.calculation = 
        # self.definition = 
        # self.label = 
        # self.presentation = 
        

    def fetch_link_from_metalinks(self, get_file):
        """
        fetch a link from the directory JSON
        """
        
        if get_file == "cal":
            return self.metalinks['instance'][self.instance['html']]['dts']['calculationLink']['local'][0]
        elif get_file == "lab":
            return self.metalinks['instance'][self.instance['html']]['dts']['labelLink']['local'][0]
        elif get_file == "pre":
            return self.metalinks['instance'][self.instance['html']]['dts']['presentationLink']['local'][0]
        elif get_file == "def":
            return self.metalinks['instance'][self.instance['html']]['dts']['definitionLink']['local'][0]
        else:
            print("ERROR!> fetch_link_from_metalinks() takes 'cal', 'lab', 'pre', or 'def'.")


    def return_an_xbrl_doc(self, tag, href):
        """
        We are not using this currently, but this may be useful to reference when we when to parse XBRL docs
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



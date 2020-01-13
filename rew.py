# #==============this code added==================================================================:
# import sys
# sys.path.append("pydevd-pycharm.egg")
# import pydevd_pycharm
#
# pydevd_pycharm.settrace('207.216.103.218', port=30266, stdoutToServer=True, stderrToServer=True)
# #================================================================================================

import urllib3
from html.parser import HTMLParser
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    'user-agent': 'Mozilla'
}
http = urllib3.PoolManager()
domain = 'https://www.rew.ca'

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if attrs[0][0] == "title":
                if len(attrs) == 2:
                    url = attrs[1][1]
                    print(url.split('?')[0])
            if attrs[0][0] == "total_pages":
                self.total_pages = int(attrs[0][1])
parser = MyHTMLParser()

def get_area_listings(location, num_bedrooms):
    url = 'https://www.rew.ca/properties/areas/' + location + "/sort/latest/desc"
    params = '?list_price_to=600000&num_bedrooms=' + str(num_bedrooms)
    response = http.request('GET', url + params, headers=headers)
    xmlstring = response.data.decode("utf-8").replace('\n', '')
    parser.total_pages = 0
    parser.feed(xmlstring)

    for i in range(2, parser.total_pages + 1):
        url_page = url + '/page/' + str(i) + params
        response = http.request('GET', url_page, headers=headers)
        xmlstring = response.data.decode("utf-8").replace('\n', '')
        parser.feed(xmlstring)


def get_property_urls():
    num_bedrooms = 2

    with open('Data/areas.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            get_area_listings(row[0], num_bedrooms)


class ListingParser(HTMLParser):
    # def handle_starttag(self, tag, attrs):
    #     if tag == 'div':
    #         if attrs[0][0] == 'class' and attrs[0][1] == 'propertyheader-price':
    #             self.price = 0
    def handle_data(self, data):
        self.data.append(data)


def get_listings_data():
    parser = ListingParser()
    with open('Data/property_2br_urls.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            parser.data = []
            listing_url = domain + row[0]
            response = http.request('GET', listing_url, headers=headers)
            xmlstring = response.data.decode("utf-8").replace('\n', '')
            parser.feed(xmlstring)

            indexes = [0] * 14
            count = 1
            for item in parser.data:
                if item.startswith('Search Results'):
                    indexes[0] = count
                if item.startswith('Listing ID: '):
                    indexes[1] = count
                if item.startswith('Bed'):
                    indexes[2] = count - 2
                if item.startswith('Bath'):
                    indexes[3] = count - 2
                if item.startswith('Sqft'):
                    indexes[4] = count - 2
                if item.startswith('Property Age'):
                    indexes[5] = count
                if item.startswith('Gross Taxes'):
                    indexes[6] = count
                if item.startswith('Strata Maintenance Fees'):
                    indexes[7] = count
                if item.startswith('Property Type'):
                    indexes[8] = count
                if item.startswith('Days on REW'):
                    indexes[9] = count
                if item.startswith('Title'):
                    indexes[10] = count
                if item.startswith('Area'):
                    indexes[11] = count
                if item.startswith('Sub-Area/Community'):
                    indexes[12] = count
                if item == 'Listing ID':
                    indexes[13] = count
                count += 1

            parser.data[0] = ''

            address = parser.data[indexes[0]]
            price = parser.data[indexes[1]]
            beds = parser.data[indexes[2]]
            baths = parser.data[indexes[3]]
            sqft = parser.data[indexes[4]]
            age_tokens = parser.data[indexes[5]].split()
            age = 0
            if len(age_tokens) >= 4:
                age = age_tokens[3][1:]
            tax = parser.data[indexes[6]]
            hoa = parser.data[indexes[7]]
            type = parser.data[indexes[8]]
            dom_tokens = parser.data[indexes[9]].split()
            dom = 0
            if len(dom_tokens) >= 1:
                dom = dom_tokens[0]
            title = parser.data[indexes[10]]
            area = parser.data[indexes[11]]
            subarea = parser.data[indexes[12]]
            listing_id = parser.data[indexes[13]]

            print(listing_id + '\t'
                  + address + '\t'
                  + price + '\t'
                  + beds + '\t'
                  + baths + '\t'
                  + sqft + '\t'
                  + age + '\t'
                  + tax + '\t'
                  + hoa + '\t'
                  + type + '\t'
                  + title + '\t'
                  + area + '\t'
                  + subarea + '\t'
                  + dom)

get_property_urls()
# get_listings_data()


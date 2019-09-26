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
            if attrs[0][0] == "itemprop":
                if len(attrs) == 3:
                    print(attrs[2][1])
            if attrs[0][0] == "total_pages":
                self.total_pages = int(attrs[0][1])
parser = MyHTMLParser()

def get_area_listings(location, num_bedrooms):
    url = 'https://www.rew.ca/properties/areas/' + location
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
    parser.data = []
    with open('Data/property_3br_urls.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            listing_url = domain + row[0]
            response = http.request('GET', listing_url, headers=headers)
            xmlstring = response.data.decode("utf-8").replace('\n', '')
            parser.feed(xmlstring)
            address = parser.data[55]
            price = parser.data[64]
            beds = parser.data[75]
            baths = parser.data[77]
            sqft = parser.data[79]
            age = parser.data[116]
            tax = parser.data[118]
            hoa = parser.data[120]
            type = parser.data[81]
            dom = parser.data[138]
            title = parser.data[128]
            area = parser.data[124]
            subarea = parser.data[122]
            listing_id = parser.data[132]

            print(listing_id + ', '
                  + address + ', '
                  + price + ', '
                  + beds + ', '
                  + baths + ', '
                  + sqft + ', '
                  + age + ', '
                  + tax + ', '
                  + hoa + ', '
                  + type + ', '
                  + title + ', '
                  + area + ', '
                  + subarea + ', '
                  + dom)

get_listings_data()

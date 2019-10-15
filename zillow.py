import urllib3
from html.parser import HTMLParser
import csv
import math

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    'user-agent': 'Mozilla'
}
http = urllib3.PoolManager()
domain = 'https://www.rew.ca'

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if attrs[0][0] == "href":
                if(attrs[0][1].startswith('https://www.zillow.com/homedetails')):
                    if attrs[1][1].endswith('info'):
                        print(attrs[0][1])
    def handle_data(self, data):
        self.data.append(data)
parser = MyHTMLParser()
parser.data = []

def get_area_listings(location, num_bedrooms):
    url = 'https://www.zillow.com/' + location + '/' + str(num_bedrooms) + '-_beds/'
    response = http.request('GET', url, headers=headers)
    xmlstring = response.data.decode("utf-8").replace('\n', '')
    parser.feed(xmlstring)
    listing_count = int(parser.data[349].split(' ')[0])
    listings_per_page = 40
    total_pages = math.ceil(listing_count/listings_per_page)

    for i in range(2, total_pages + 1):
        url_page = url + str(i) + '_p/'
        response = http.request('GET', url_page, headers=headers)
        xmlstring = response.data.decode("utf-8").replace('\n', '')
        parser.feed(xmlstring)


def get_property_urls():
    num_bedrooms = 2

    with open('Data/usaAreas.csv') as csv_file:
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
        # print(data)


def get_listings_data():
    parser = ListingParser()
    with open('Data/zillow_urls.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            parser.data = []
            response = http.request('GET', row[0], headers=headers)
            xmlstring = response.data.decode("utf-8").replace('\n', '')
            parser.feed(xmlstring)

            indexes = [0] * 15
            count = 1
            indexes[0] = 3
            for item in parser.data:
                if item == 'sqft':
                    indexes[4] = count - 3
                if item == 'bd':
                    indexes[1] = count - 4
                    indexes[2] = count - 3
                if item == 'ba':
                    indexes[3] = count - 3
                if item == 'Year built:':
                    indexes[5] = count
                if item == 'Annual tax amount':
                    indexes[6] = count
                if item == 'HOA fee:':
                    indexes[7] = count
                if item == 'Type:':
                    indexes[8] = count
                if item == 'Time on Zillow':
                    indexes[9] = count
                # if item.startswith('Title'):
                #     indexes[10] = count
                # if item.startswith('Area'):
                #     indexes[11] = count
                # if item.startswith('Sub-Area/Community'):
                #     indexes[12] = count
                if item == 'MLS ID':
                    indexes[13] = count
                count += 1

            parser.data[0] = ''

            address = parser.data[indexes[0]].split('|')[0]
            price = parser.data[indexes[1]]
            beds = parser.data[indexes[2]]
            baths = parser.data[indexes[3]]
            sqft = parser.data[indexes[4]]
            age = parser.data[indexes[5]]
            tax = parser.data[indexes[6]]
            hoa = parser.data[indexes[7]]
            type = parser.data[indexes[8]]
            dom = parser.data[indexes[9]]
            # title = parser.data[indexes[10]]
            # area = parser.data[indexes[11]]
            # subarea = parser.data[indexes[12]]
            listing_id = parser.data[indexes[13]]
            #
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
                  # + title + '\t'
                  # + area + '\t'
                  # + subarea + '\t'
                  + dom)
            # return

# get_property_urls()
get_listings_data()

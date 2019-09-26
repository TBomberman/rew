import urllib3
from html.parser import HTMLParser
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    'user-agent': 'Mozilla'
}
http = urllib3.PoolManager()

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
    print('done', location)

num_bedrooms = 3

with open('Data/areas.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        get_area_listings(row[0], num_bedrooms)

# href="/properties/R2408510/803-6282-kathleen-avenue-burnaby-bc?search_id=burnaby-bc&amp;search_params%5Bquery%5D=Burnaby%2C+BC&amp;search_params%5Bsearchable_id%5D=13&amp;search_params%5Bsearchable_type%5D=Geography&amp;search_type=geography_browse"
# url = domain + href
# response = http.request('GET', url, headers=headers)
# print(response.status)





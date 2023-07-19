import urllib3
from html.parser import HTMLParser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
  'Origin': 'https://www.tripadvisor.ca',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}
http = urllib3.PoolManager()

class RestaurantParser(HTMLParser):
  get_name = False
  name_count = 0
  get_reviews = False
  string_build = ""
  sponsored = False
  number = ""

  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      for attr in attrs:
        if attr[0] == "class" and attr[1] == "Lwqic Cj b":
          self.get_name = True
    if tag == 'svg': # stars
      for attr in attrs:
        if attr[0] == "class" and attr[1] == "UctUV d H0" and not self.sponsored:
          self.string_build = self.string_build + "; " + attrs[4][1][:3]
    if tag == 'span':
      for attr in attrs:
        if attr[0] == "class" and attr[1] == "IiChw":
          self.get_reviews = True
        if attr[0] == "class" and attr[1] == "HupEO SMIhk":
          if not self.sponsored:
            self.data.append(self.string_build)
          self.sponsored = False
  
  def handle_data(self, data):
    if data and data == "Sponsored":
       self.sponsored = True
       return
    if self.get_name and data:
      self.name_count = self.name_count + 1
      if self.name_count == 1:
        self.string_build = data
        self.number = data        
      if self.name_count == 3:
        self.name_count = 0
        self.string_build = self.string_build + "; " + data
        self.get_name = False
    if self.get_reviews and data:
      self.string_build = self.string_build + "; " + data
      self.get_reviews = False
    if data and data[0] == "$":
      self.string_build = self.string_build + "; " + data

def get_restaurant_data():
  parser = RestaurantParser()
  # url = "https://www.tripadvisor.ca/Restaurants-g181716-Richmond_British_Columbia.html"
  url_orig = "https://www.tripadvisor.ca/RestaurantSearch?Action=PAGE&ajax=1&availSearchEnabled=false&sortOrder=popularity&geo=181716&itags=10591&o=a"

  number = 0
  for i in range(0,18):
    parser.data = []
    number = i*30
    url = url_orig + str(number)
    response = http.request('GET', url, headers=headers)
    xmlstring = response.data.decode("utf-8").replace('\n', '')
    parser.feed(xmlstring)
    for item in parser.data:
      print(item)

get_restaurant_data()

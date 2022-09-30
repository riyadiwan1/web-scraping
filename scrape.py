import requests
from bs4 import BeautifulSoup
import pandas
import argparse
import connect

parser = argparse.ArgumentParser() # to parse command line argument
parser.add_argument("--page_num_max", help="enter the number of pages to parse", type=int)
parser.add_argument("--dbname", help="enter the name of db", type=str)
args = parser.parse_args()

oyo_url = "https://www.oyorooms.com/hotels-in-bangalore/?page="
page_num_Max = args.page_num_max
scrapedinfolist = []
connect.connect(args.dbname)

for pagenum in range(1, page_num_Max):

    url = oyo_url + str(pagenum)
    print("GET request for " + url)
    req = requests.get(url)
    content = req.content
    soup = BeautifulSoup(content, "html.parser")  # soup object
    all_hotels = soup.find_all("div", {"class": "hotelCardListing"})

    for hotel in all_hotels:

        hoteldict = {}
        hoteldict["name"] = hotel.find("h3", {"class": "listingHotelDescription__hotelName"}).text
        hoteldict["address"] = hotel.find("span", {"itemprop": "streeAddress"}).text
        hoteldict["price"] = hotel.find("span", {"class": "listingPrice__finalPrice"}).text
        try:
            hoteldict["rating"] = hotel.find("span", {"class": "hotelRating__ratingSummary"}).text
        except AttributeError:
            hoteldict["rating"] = None  # concept used in production code

            parent_amenities = hotel.find("div", {"class": "amenityWrapper"})

            amenitylist = []
            for amenity in parent_amenities.find_all("div", {"class": "amenityWrapper__amenity"}):
                amenitylist.append(amenity.find("span", {"class": "d-body-sm"}).text.strip())

            hoteldict["amenities"] = ', '.join((amenitylist[:-1]))
            scrapedinfolist.append(hoteldict)
            connect.insertintotable(args.dbname, tuple(hoteldict.values()))

    # print(hotel_name,hotel_add,hotel_price,rating,amenity list)

dataFrame = pandas.DataFrame(scrapedinfolist)
print("creating csv file")
dataFrame.to_csv("oyo.csv")
connect.get_hotel_info(args.dbname)



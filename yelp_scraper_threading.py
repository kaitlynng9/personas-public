'''
This script uses Yelp Fusion API to input relevant restaurant information using lat/lon coords from PSRC data (other information removed for privacy reasons)
This scripts uses a threading approach.

input files: rest_od.csv
    this file contains the origin and destination lat/long coordinates for restaurants visited, from PSRC
'''

# import our modules
import pandas as pd
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from ratelimit import limits, sleep_and_retry

# Define the rate limit
CALLS = 4
PERIOD = 1  # seconds

@sleep_and_retry
@limits(calls=CALLS, period=PERIOD)
def make_yelp_request(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON response")
        return None


# threading approach
def threading_poi_finder(yelp_api, headers, row):
    '''
    this function uses the Yelp Fusion API to pull in restaurant information
    returns information about a single business
    '''
    radius = 0
    # determine whether to look at origin or destination for lat/long
    if row.origin_purpose == "Went to restaurant to eat/get take-out":
        lat = row.origin_lat
        lon = row.origin_lng
    elif row.dest_purpose == "Went to restaurant to eat/get take-out":
        lat = row.dest_lat
        lon = row.dest_lng


    url = yelp_api + "price=1&price=2&price=3&price=4&latitude=" + str(lat)+"&longitude=" + str(lon)+ "&term=food&radius=" + str(radius) + "&sort_by=distance&limit=1"

    poi_dict = make_yelp_request(url, headers)

    # check that information was returned
    if poi_dict and "businesses" in poi_dict:
        if len(poi_dict["businesses"]) > 0:
            return poi_dict["businesses"][0]
    return
         


def main():
    # API information
    yelp_api = "https://api.yelp.com/v3/businesses/search?"
    api_keys = ["input your api keys here"]


    # files
    all_trips = pd.read_csv('data_outputs/trips_od_rest.csv')
    partial_trips = [all_trips[:4500], all_trips[4500:9000], all_trips[9000:13500], all_trips[13500:18000], all_trips[18000:]]

    for i in range(len(partial_trips)):
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + api_keys[i]
        }
        ############# THREADING #############
        # run time
        time0 = time.time()
        # get yelp info and save in list
        threads = []
        pois = []
        with ThreadPoolExecutor(max_workers=10) as executor:                    # use 10 threads
            for idx, row in partial_trips[i].iterrows():                           # iterate through df
                threads.append(executor.submit(threading_poi_finder, yelp_api, headers, row))      # each task assigned to a thread
            for task in as_completed(threads):
                pois.append(task.result())                                       # append results to final list
        time1 = time.time()

        # write to csv
        partial_trips[i]["restaurant_info"] = pois
        partial_trips[i].to_csv('data_outputs/trips_od_yelp_'+str(i+1)+'.csv')

        print(i, "Threading time elapsed: ", time1-time0)

if __name__ == "__main__":
    main()
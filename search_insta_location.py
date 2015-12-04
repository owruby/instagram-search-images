# -*- coding: utf-8 -*-

from instagram.client import InstagramAPI
import inspect
import os
import requests
import csv
import glob

CLIENT_ID = ''
CLIENT_SECRET = ''
ACCESS_TOKEN = ''

OUTPUT_CSV = "download/images.csv"
OUTPUT_IMAGE_DIR = "download/images"

LIMIT = 90 # 1箇所に対しての画像枚数の制限

LAT = 40.68975001664651  # 緯度
LNG = -74.04029846191406 # 経度
DISTANCE = 1000 # 緯度,経度を中心とした半径
LOCATION_COUNT = 10 # 場所の取得数

class InstagramCrawler:

    def __init__(self):
        self.api = InstagramAPI(
            access_token=ACCESS_TOKEN,
            client_id = CLIENT_ID,
            client_secret = CLIENT_SECRET)
        self.clean_dir_csv()

    
    def clean_dir_csv(self):
        if os.path.exists(OUTPUT_CSV):
            os.remove(OUTPUT_CSV)

        if os.path.exists(OUTPUT_IMAGE_DIR):
            files = glob.glob(OUTPUT_IMAGE_DIR + '/*.jpg')
            for path in files:
                os.remove(path)
        else:
            os.mkdir(OUTPUT_IMAGE_DIR)


    def search_instagram(self):
        location_ids, location_lls = self.__search_location_ids()
        count = 1

        for location_id,location_ll in zip(location_ids,location_lls):

            max_id = ""
            next = True
            while(not next is None):
                media_ids,next = self.api.location_recent_media(
                    count = 30,
                    location_id = location_id,
                    max_id = max_id)
            
                with open(OUTPUT_CSV, 'w') as csvfile:
                    writer = csv.writer(csvfile, delimiter=str(','), quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(['origin_url', 'file_name', 'latitude', 'longitude', 'location_id'])
                    for media_id in media_ids:
                        thumb_url = media_id.images['thumbnail'].url
                        print "now %d downloading" % count
                        try:
                            r = requests.get(thumb_url)
                            if r.status_code == 200:
                                file_name = "%04d.jpg" % count
                                path = "{0}/{1}".format(OUTPUT_IMAGE_DIR, file_name)
                                f = open(path,"wb")
                                f.write(r.content)
                                f.close()
                            
                                writer.writerow([thumb_url, file_name, location_ll[0], location_ll[1], location_id])
                             
                        except Exception as e:
                            pass

                        if not next is None:
                            temp, max_location_id = next.split("max_id=")
                            max_id = str(max_location_id)

                        count += 1
                    
    
    def __search_location_ids(self):
        media_ids = self.api.location_search(
            count = LOCATION_COUNT,
            lat = LAT,
            lng = LNG,
            distance = DISTANCE)

        return [
            [media_id.id for media_id in media_ids],
            [[media_id.point.latitude, media_id.point.longitude] for media_id in media_ids]]


if __name__ == '__main__':
    crawler = InstagramCrawler()
    crawler.search_instagram()
        
    print "download complete"

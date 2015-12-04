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
START = 0
END = 30 # 30区切りで

LAT = 35.681184078 # 緯度
LNG = 139.764846082 # 軽度

class InstagramCrawler:

    def __init__(self):
        self.api = InstagramAPI(
            access_token=ACCESS_TOKEN,
            client_id = CLIENT_ID,
            client_secret = CLIENT_SECRET)
        clean_dir_csv()
    
    def clean_dir_csv():
        if os.path.exists(OUTPUT_CSV):
            os.remove(OUTPUT_CSV)

        if os.path.exists(OUTPUT_IMAGE_DIR):
            files = glob.glob(OUTPUT_IMAGE_DIR + '/*.jpg')
            for path in files:
                os.remove(path)
        else:
            os.mkdir(OUTPUT_IMAGE_DIR)


    def search_instagram(self):
        location_ids = self.__search_location_ids()
        count = 1
        
        for location_id in location_ids:
            media_ids,next = self.api.location_recent_media(
                count = 30,
                location_id = location_id)
            
            with open(OUTPUT_CSV, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=str(','), quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['origin_url', 'file_name', 'latitude', 'longitude'])
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
                   
                    except Exception as e:
                        pass
                    count += 1
    
    def __search_location_ids(self):
        media_ids = self.api.location_search(
            count = 50,
            lat = LAT,
            lng = LNG,
            distance = 1000)

        return [media_id.id for media_id in media_ids]

if __name__ == '__main__':
    crawler = InstagramCrawler()
    crawler.search_instagram()
        
    print "download complete"

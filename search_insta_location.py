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
OUTPUT_IMAGE320_DIR = "download/images320"

LIMIT = 90 # 1箇所に対しての画像枚数の制限

LAT = 35.681282860023565  # 緯度
LNG = 139.76674675941467 # 経度
DISTANCE = 1000 # 緯度,経度を中心とした半径(m)
LOCATION_COUNT = 2 # 場所の取得数

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

        if os.path.exists(OUTPUT_IMAGE320_DIR):
            files = glob.glob(OUTPUT_IMAGE320_DIR + '/*.jpg')
            for path in files:
                os.remove(path)
        else:
            os.mkdir(OUTPUT_IMAGE320_DIR)
                


    def search_instagram(self):
        location_ids, location_lls = self.__search_location_ids()
        count = 0

        for location_id,location_ll in zip(location_ids,location_lls):

            max_id = ""
            next = True
            while(not next is None):
                media_ids,next = self.api.location_recent_media(
                    count = 30,
                    location_id = location_id,
                    max_id = max_id)
            
                with open(OUTPUT_CSV, 'w') as csvfile:
                    #writer = csv.writer(csvfile, delimiter=str(','), quoting=csv.QUOTE_MINIMAL)
                    writer = csv.writer(csvfile, delimiter=str(','), quoting=csv.QUOTE_MINIMAL)                    
                    writer.writerow(['origin_url', 'file_name', 'latitude', 'longitude', 'location_id', 'tags'])
                    for media_id in media_ids:
                        thumb_url = media_id.images['thumbnail'].url
                        thumb320_url = media_id.images['low_resolution'].url

                        print "now %d downloading" % count
                        try:
                            r = requests.get(thumb_url)
                            r2 = requests.get(thumb320_url)
                            if r.status_code == 200 and r2.status_code == 200:
                                file_name = "%04d.jpg" % count
                                path = "{0}/{1}".format(OUTPUT_IMAGE_DIR, file_name)
                                self.__save_image(path, r.content)
                                path = "{0}/{1}".format(OUTPUT_IMAGE320_DIR, file_name)
                                self.__save_image(path, r2.content)

                                tags = [tag.name for tag in media_id.tags]
                                print tags
                                tags = unicode(','.join(tags)).encode('utf_8')

                                print writer.writerow([thumb_url, file_name, location_ll[0], location_ll[1], location_id, tags])
                                print file_name
                             
                        except Exception as e:
                            print type(str(e))
                            print e.message
                            pass

                        if not next is None:
                            temp, max_location_id = next.split("max_id=")
                            max_id = str(max_location_id)
                        count += 1

                next = None
                    
    
    def __search_location_ids(self):
        media_ids = self.api.location_search(
            count = LOCATION_COUNT,
            lat = LAT,
            lng = LNG,
            distance = DISTANCE)

        return [
            [media_id.id for media_id in media_ids],
            [[media_id.point.latitude, media_id.point.longitude] for media_id in media_ids]]

    def __save_image(self, save_path, img_contents):
        f = open(save_path, "wb")
        f.write(img_contents)
        f.close()


if __name__ == '__main__':
    crawler = InstagramCrawler()
    crawler.search_instagram()
        
    print "download complete"

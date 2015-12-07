# -*- coding: utf-8 -*-

from instagram.client import InstagramAPI
import inspect
import os
import requests
import csv
import glob
import codecs

CLIENT_ID = 'b6bf0a570ee54c97b8a49748b0e574a1'
CLIENT_SECRET = '40e8a61730c545aeab7f610650119d80'
ACCESS_TOKEN = '1536083749.b6bf0a5.b67f844eda234d069442f99209aed2be'

OUTPUT_CSV = "download/images.csv"
OUTPUT_IMAGE_DIR = "download/images"
OUTPUT_IMAGE320_DIR = "download/images320"
START = 0
END = 30 # 30区切りで
TAG_NAME = "shibuya"

def clean_dir_csv():
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
            

def instagram_search(max_id="", skip=0):
    api = InstagramAPI(
        access_token=ACCESS_TOKEN,
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET)
    
    media_ids,next = api.tag_recent_media(
        tag_name=TAG_NAME, 
        count=30, 
        max_tag_id = max_id)

    print next
    
    with open(OUTPUT_CSV, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=str(','), quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['origin_url', 'file_name', 'latitude', 'longitude', 'tags'])
        count = 0 + skip

        for media_id in media_ids:
            
            thumb_url = media_id.images['thumbnail'].url
            thumb320_url = media_id.images['low_resolution'].url

            print "now %d downloading ..." % count
            try:
                r = requests.get(thumb_url)
                r2 = requests.get(thumb320_url)
                if r.status_code == 200 and r2.status_code == 200:
                    file_name = "%04d.jpg" % count
                    path = "{0}/{1}".format(OUTPUT_IMAGE_DIR, file_name)
                    save_image(path, r.content)
                    path = "{0}/{1}".format(OUTPUT_IMAGE320_DIR, file_name)
                    save_image(path, r2.content)
                    
                    tags = [tag.name for tag in media_id.tags]
                    tags = unicode(','.join(tags)).encode('sjis')

                    if hasattr(media_id, "location"):
                        latitude = media_id.location.point.latitude
                        longitude = media_id.location.point.longitude
                        writer.writerow([thumb_url, file_name, latitude, longitude, tags])
                    else:
                        writer.writerow([thumb_url, file_name, "", "", tags])
                        
            except Exception as e:
                print str(type(e))
                pass
            count += 1
        temp,max_tag_id = next.split("max_tag_id=")
        max_tag_id = str(max_tag_id)
        
        return max_tag_id

def save_image(save_path, img_contents):
    f = open(save_path, "wb")
    f.write(img_contents)
    f.close()


if __name__ == '__main__':
    clean_dir_csv()
    max_tag_id = ""
    for skip in range(START, END, 30):
        max_tag_id = instagram_search(max_tag_id, skip)
        
    print "download complete"

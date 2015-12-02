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
END = 120 # 30区切りで
TAG_NAME = "apple"

def clean_dir_csv():
    if os.path.exists(OUTPUT_CSV):
        os.remove(OUTPUT_CSV)

    if os.path.exists(OUTPUT_IMAGE_DIR):
        files = glob.glob(OUTPUT_IMAGE_DIR + '/*.jpg')
        for path in files:
            os.remove(path)
    else:
        os.mkdir(OUTPUT_IMAGE_DIR)

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
        writer.writerow(['origin_url', 'file_name'])
        count = 0 + skip

        for media_id in media_ids:
            
            thumb_url = media_id.images['thumbnail'].url
            print "now %d downloading ..." % count
            try:
                r = requests.get(thumb_url)
                if r.status_code == 200:
                    file_name = "%04d.jpg" % count
                    path = "{0}/{1}".format(OUTPUT_IMAGE_DIR, file_name)
                    f = open(path,"wb")
                    f.write(r.content)
                    f.close()
                    writer.writerow([thumb_url, file_name])
            except Exception:
                pass
            count += 1
        temp,max_tag_id = next.split("max_tag_id=")
        max_tag_id = str(max_tag_id)
        
        return max_tag_id

if __name__ == '__main__':
    clean_dir_csv()
    max_tag_id = ""
    for skip in range(START, END, 30):
        max_tag_id = instagram_search(max_tag_id, skip)
        
    print "download complete"

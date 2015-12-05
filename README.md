# Instagram API Crawler

## Setup
```
pip install python-instagram
```

## Usage
https://instagram.com/developer/ から
* client_id
* client_secret
* access_token
を取得する.

参考サイト
http://www.dcrew.jp/ja-instagram-api-doc-v1/,
http://iaseteam.eshizuoka.jp/e1237677.html

## Search method

* Search by tags（タグ検索）
* Search by location（場所検索）

### Search by tags（タグ検索）
#### Description
インスタグラムの```#tag```のようなタグを含む画像をダウンロードする.
ダウンロード情報は以下の内容を,images.csvに記載.
* origin_url
* file_name
* latitude
* longitude

#### Usage
1. 取得したclient_id,client_secret,access_tokenを```search_insta_tag.py``` に書き込む.
2. ```TAG_NAME```の箇所に検索するタグ名を入力.```END```にダウンロードする画像枚数を設定.
3. 
```
python search_insta_tag.py
```
で実行


### Search by location（場所検索）
#### Description
(緯度,経度)をもとに,その緯度,経度の周りの```location_id```を取得する.
その取得した```location_id```をもとに検索する.
images.csvには以下を記載
* origin_url
* file_name
* latitude
* longtitude
* location_id

#### Usage
1. 取得したclient_id,client_secret,access_tokenを```search_insta_tag.py``` に書き込む.
2. ```LAT```に緯度,```LOG```に経度をいれ```DISTANCE```に,緯度と経度の```location_id```を取得する半径を指定,```LOCATION_COUNT```に取得するlocation_idの数を指定.

緯度,経度の情報は以下のサイトを参照
http://maihamakyo.org/etc/locastagram/

3.
``` python search_insta_location.py ```
で実行

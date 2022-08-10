#
# from skimage.io import imread
# import cv2
#
# # image_filename = "https://i.imgur.com/XyUC9tj.jpg"
# # image_numpy = imread( image_filename )
# #
# # h, w, _ = image_numpy.shape
# #
# # image_numpy = cv2.resize(image_numpy, (int(0.25 * w), int(0.25 * h)))
# #
# # cv2.imshow("ball", image_numpy)
# # cv2.waitKey(0)
#
# from imgurpython import ImgurClient
#
# client_id = 'e49d2b92ff34d25'
# client_secret = '82e5351fe887fb688025e32207e101ce0412cdc1'
#
# client = ImgurClient(client_id, client_secret)
#
# # Example request
# items = client.gallery_tag(tag="dog")
# print(items.link)

# import requests
#
# url = "https://imgur-apiv3.p.rapidapi.com/3/gallery/t/dog/%7Bsort%7D/%7Bwindow%7D/%7Bpage%7D"
#
# headers = {
# 	"Authorization": "Bearer 5da2720397675730cfdf5942d174fd7bbf6d50e0",
# 	"X-RapidAPI-Key": "13c019e184msh22d0b73311482b8p19e004jsn94800ef961a9",
# 	"X-RapidAPI-Host": "imgur-apiv3.p.rapidapi.com"
# }
#
# response = requests.request("GET", url, headers=headers)
#
# for items in response.data:
#     print(items.data)

import http.client
import json
from bg_contours_function import *
import matplotlib

matplotlib.use('Agg')

clientId = 'e49d2b92ff34d25'
tagName = 'bowl'
sort = ''
window = ''
page = ''

conn = http.client.HTTPSConnection("api.imgur.com")
boundary = ''
payload = ''
headers = {
  'Authorization': f'Client-ID {clientId}',
  'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
}
conn.request("GET", f"/3/gallery/t/{tagName}/{sort}/{window}/{page}", payload, headers)
res = conn.getresponse()
data = res.read()
gallery = data.decode("utf-8")
gallery = json.loads(gallery)

images = []

for item in gallery["data"]["items"]:
    if (item['is_album'] == True):
        #print('album')
        for image in item['images']:
            if ('.jpg' in image['link']) or ('.png' in image['link']):
                #print(image['link'])
                images.append(image['link'])
    else:
        if ('.jpg' in item['link']) or ('.png' in item['link']):
            #print(image['link'])
            images.append(image['link'])


print(images)

for url in images[0:10]:
    for i in range(0,2):
        print("%s %s" % (url, str(i)))

        try:
            bg_contours_func(url, i)
        except Exception as e:
            print(str(e))
            continue
#from pycocotools.coco import COCO
import requests
import os
import pandas as pd
from datetime import datetime, timedelta

# configurations
folder_img_count = 5

images = pd.read_csv(r'E:/Cemtrex Labs/Open Images/dummy.csv')
img_name = images.iloc[:,0].tolist()
img_url = images.iloc[:,1].tolist()
# image = list(zip(img_name, img_url))

total_images = len(img_name)
#print(total_images)
counter = 0
timer = datetime.now()
for img,url in zip(img_name, img_url):
    if counter % 5 == 0:
        tt = (datetime.now() - timer).seconds
        print('time required for 50 images  ', tt, 'remaining time ',
              (total_images - counter) * timedelta(seconds=tt / 5))
        timer = datetime.now()
    if counter < 0:
        counter += 1
        continue
    print(counter, ": ", img)
    ####### uncomment this when failure occurs #######
    # if '000000385341.jpg' == img['file_name']:
    #     quit()
    ####### till here #######

    ####### comment this when failure occurs #######
    img_data = requests.get(url).content

    folder_name = 'open_data/open_v' + str(counter // folder_img_count)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

        #img_data = requests.get(url).content

    filename = folder_name + '/' + img
    with open(filename, 'wb') as handler:
         handler.write(img_data)
#     ####### till here #######
    counter += 1

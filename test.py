import requests
import os
import pandas as pd
from datetime import datetime, timedelta

# configurations
folder_img_count = 500

images = pd.read_csv(r'E:/Cemtrex Labs/Open Images/dummy.csv')
img_name = images.iloc[:, 0].tolist()
img_url = images.iloc[:, 1].tolist()
# image = list(zip(img_name, img_url))

total_images = len(img_name)
# print(total_images)
starting_index = 0
counter = starting_index
timer = datetime.now()
for img, url in zip(img_name, img_url):
    folder_name = 'open_data/open_v' + str(counter // folder_img_count)
    filename = folder_name + '/' + img

    if os.path.isfile(filename):
        counter = +1
        continue

    print(counter, ": ", img)

    if counter % 50 == 0:
        tt = (datetime.now() - timer).seconds
        remaining_img = (starting_index + total_images - counter)
        print('time required for 50 images  ', tt, 'remaining time ', remaining_img, 'Images',
              remaining_img * timedelta(seconds=tt / 50))
        timer = datetime.now()

    img_data = requests.get(url).content

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

        # img_data = requests.get(url).content

    with open(filename, 'wb') as handler:
        handler.write(img_data)
    #     ####### till here #######
    counter += 1

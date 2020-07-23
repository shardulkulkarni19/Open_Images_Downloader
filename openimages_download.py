from pycocotools.coco import COCO
import requests
import os
from datetime import datetime, timedelta

# configurations
folder_img_count = 500


counter = 0
timer = datetime.now()
for img in images:
    if counter % 50 == 0:
        tt = (datetime.now() - timer).seconds
        print('time required for 50 images  ', tt, 'remaining time ',
              (total_images - counter) * timedelta(seconds=tt / 50))
        timer = datetime.now()
    if counter < 0:
        counter += 1
        continue
    print(counter, ": ", img['file_name'])
    ####### uncomment this when failure occurs #######
    # if '000000385341.jpg' == img['file_name']:
    #     quit()
    ####### till here #######

    ####### comment this when failure occurs #######
    img_data = requests.get(img['image_url']).content

    folder_name = 'coco_data/car/coco_v' + str(counter // folder_img_count)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        with open(folder_name + "/annotations_v" + str(counter // folder_img_count) + '.csv', "a+") as myfile:
            myfile.write('file_name,classes,xmin,ymin,xmax,ymax\n')

    filename = folder_name + '/' + img['file_name']
    with open(filename, 'wb') as handler:
        handler.write(img_data)
        annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds)
        anns = coco.loadAnns(annIds)
        with open(folder_name + "/annotations_v" + str(counter // folder_img_count) + '.csv', "a+") as myfile:
            for i in range(len(anns)):
                xmin = anns[i]["bbox"][0]
                ymin = anns[i]["bbox"][1]
                xmax = anns[i]["bbox"][2] + anns[i]["bbox"][0]
                ymax = anns[i]["bbox"][3] + anns[i]["bbox"][1]

                mystring = img['file_name'] + ',' + required_categories[anns[i]['category_id']] + ',' + str(
                    xmin) + ',' + str(ymin) + ',' + str(xmax) + "," + str(ymax)
                myfile.write(mystring + '\n')
    ####### till here #######
    counter += 1

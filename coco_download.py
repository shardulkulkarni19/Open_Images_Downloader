from pycocotools.coco import COCO
import requests
import os

# configurations
#required_categories = {1: 'person'}
#annFile = "../instances_train2017.json"
folder_img_count = 500

# initialize COCO api for instance annotations
#coco = COCO(annFile)
# display COCO categories and supercategories
#cats = coco.loadCats(coco.getCatIds())
#nms = [cat['name'] for cat in cats]
# print('COCO categories: \n{}\n'.format(' '.join(nms)))

# get all images containing given categories, select one at random
# catNms = [category for category in required_categories.values()]
# catIds = coco.getCatIds(catNms=catNms)
# imgIds = coco.getImgIds(catIds=catIds)
# print(len(imgIds))
# images = coco.loadImgs(imgIds)
# print(images)


counter = 0
for img in images:
    if counter < 3453:
        counter += 1
        continue
    print(counter, ": ", img['file_name'])
    ####### uncomment this when failure occurs #######
    # if '000000385341.jpg' == img['file_name']:
    #     quit()
    ####### till here #######


    ####### comment this when failure occurs #######
    img_data = requests.get(img['coco_url']).content

    folder_name = 'coco_v' + str(counter // folder_img_count)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        # with open(folder_name + "/annotations_v" + str(counter // folder_img_count) + '.csv', "a+") as myfile:
        #     myfile.write('file_name,classes,xmin,ymin,xmax,ymax\n')

    # filename = folder_name + '/' + img['file_name']
    # with open(filename, 'wb') as handler:
    #     handler.write(img_data)
    #     annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds)
    #     anns = coco.loadAnns(annIds)
    #     with open(folder_name + "/annotations_v" + str(counter // folder_img_count) + '.csv', "a+") as myfile:
    #         for i in range(len(anns)):
    #             xmin = anns[i]["bbox"][0]
    #             ymin = anns[i]["bbox"][1]
    #             xmax = anns[i]["bbox"][2] + anns[i]["bbox"][0]
    #             ymax = anns[i]["bbox"][3] + anns[i]["bbox"][1]
    #
    #             mystring = img['file_name'] + ',' + required_categories[anns[i]['category_id']] + ',' + str(
    #                 xmin) + ',' + str(ymin) + ',' + str(xmax) + "," + str(ymax)
    #             myfile.write(mystring + '\n')
    ####### till here #######
    counter += 1

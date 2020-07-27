from pandas import read_csv
from requests import get
import os
from datetime import datetime, timedelta
from queue import Queue
import threading


def downnload_images(q, q1, total_images):
    timer_image_count = 50
    folder_img_count = 500
    timer = datetime.now()
    while not q.empty():
        counter, img, url = q.get()
        folder_name = 'E:/Cemtrex Labs/Open Images/test_present/open_v' + str(counter // folder_img_count)
        filename = folder_name + '/' + img + '.jpg'
        print(counter, ": ", img)
        if os.path.isfile(filename):
            continue
        if counter % timer_image_count == 0:
            tt = (datetime.now() - timer).seconds
            remaining_img = (total_images - counter)
            print('time required for 50 images ', tt, 'remaining time for ', remaining_img, ' images ',
                  remaining_img * timedelta(seconds=tt / timer_image_count))
            timer = datetime.now()

        if not os.path.exists(folder_name):
            try:
                os.makedirs(folder_name)
            except FileExistsError:
                pass

        response = get(url)
        status = str(response.status_code)
        size = len(response.content)  # Returns size in bytes
        if size > 1024:
            if status[0] == '2':
                with open(filename, 'wb') as handler:
                    handler.write(response.content)
                data = (img, 0)
            else:
                data = (img, 1)
            q1.put(data)
    q1.put(('a', 2))


def write_to_file(q):
    filetxt = 'E:/Cemtrex Labs/Open Images/test_success.csv'
    file = 'E:/Cemtrex Labs/Open Images/test_fail.csv'
    while True:
        img, flag = q.get()
        if flag == 0:
            with open(filetxt, 'a') as s:
                s.write(img + "\n")
        elif flag == 1:
            with open(file, 'a') as f:
                f.write(img + "\n")
        elif flag == 2:
            break


if __name__ == '__main__':
    q0 = Queue()
    q1 = Queue()
    q2 = Queue()
    q3 = Queue()
    q4 = Queue()
    # configurations
    annFile = "E:/Cemtrex Labs/Open Images/test_occ_present_list.csv"
    csv_file = read_csv(annFile)

    imgs = csv_file.ImageID.tolist()
    urls = csv_file.OriginalURL.tolist()
    total_images = len(imgs)
    counter = 80500
    flag = 0
    for img, url in zip(imgs, urls):
        if flag == 0:
            q0.put((counter, img, url))
            flag += 1
        elif flag == 1:
            q1.put((counter, img, url))
            flag += 1
        elif flag == 2:
            q2.put((counter, img, url))
            flag += 1
        elif flag == 3:
            q3.put((counter, img, url))
            flag = 0
        counter += 1

    t0 = threading.Thread(target=downnload_images, args=(q0, q4, total_images)).start()
    t1 = threading.Thread(target=downnload_images, args=(q1, q4, total_images)).start()
    t2 = threading.Thread(target=downnload_images, args=(q2, q4, total_images)).start()
    t3 = threading.Thread(target=downnload_images, args=(q3, q4, total_images)).start()
    t4 = threading.Thread(target=write_to_file, args=(q4,)).start()

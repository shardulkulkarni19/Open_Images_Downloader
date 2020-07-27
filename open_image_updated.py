from pandas import read_csv
from requests import get
import os
from datetime import datetime, timedelta
from queue import Queue
import threading
import config



def downnload_images(q, q1, total_images, starting_counter):

    timer = datetime.now()

    while not q.empty():
        counter, img, url = q.get()
        folder_name = config.FOLDER_NAME + str(counter // config.FOLDER_IMG_COUNT)
        filename = folder_name + '/' + img + '.jpg'
        print(counter, ": ", img)

        if os.path.isfile(filename):
            continue

       #    TIME CALCULATION FOR DATA DOWNLOADING
        if counter % config.TIMER_IMAGE_COUNT == 0:
            tt = (datetime.now() - timer).seconds
            remaining_img = (total_images - (counter - config.STARTING_COUNTER))
            print('time required for 50 images ', tt, 'remaining time for ', remaining_img, ' images ',
                  remaining_img * timedelta(seconds=tt / config.TIMER_IMAGE_COUNT))
            timer = datetime.now()

        #      CHECK IF FOLDER EXITS......IF NOT CREATES NEW FOLDER
        if not os.path.exists(folder_name):
            try:
                os.makedirs(folder_name)
            except FileExistsError:
                pass

        # DOWNLOADING IMAGES
        response = get(url)
        status = str(response.status_code)
        size = len(response.content)  # Returns size in bytes

        # DOWNLOADING VALID IMAGES
        if size > config.THRESHOLD_IMG_SIZE and status[0] == '2':
            with open(filename, 'wb') as handler:
                handler.write(response.content)
                data = (img, 0)
        else:
            data = (img, 1)
        q1.put(data)
    q1.put(('a', 2))


# CREATING LOG LIST
def write_to_file(q):

    while True:
        img, flag = q.get()
        if flag == 0:
            with open(config.SUCCESS_FILE, 'a') as s:
                s.write(img + "\n")

        elif flag == 1:
            with open(config.FAIL_FILE, 'a') as f:
                f.write(img + "\n")

        elif flag == 2:
            break

if __name__ == '__main__':
    # INITIALIZING QUEUE

    q0 = Queue()
    q1 = Queue()
    q2 = Queue()
    q3 = Queue()
    q4 = Queue()


    csv_file = read_csv(config.ANN_FILE)

    imgs = csv_file.ImageID.tolist()
    urls = csv_file.OriginalURL.tolist()
    total_images = len(imgs)
    counter = config.STARTING_COUNTER

    flag = 0

    #
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

    t0 = threading.Thread(target=downnload_images, args=(q0, q4, total_images, config.STARTING_COUNTER)).start()
    t1 = threading.Thread(target=downnload_images, args=(q1, q4, total_images, config.STARTING_COUNTER)).start()
    t2 = threading.Thread(target=downnload_images, args=(q2, q4, total_images, config.STARTING_COUNTER)).start()
    t3 = threading.Thread(target=downnload_images, args=(q3, q4, total_images, config.STARTING_COUNTER)).start()
    t4 = threading.Thread(target=write_to_file, args=(q4,)).start()


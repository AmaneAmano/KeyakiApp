"""
Using Azure FaceAPI, detect faces.
save face image to output directory

todo: joblibが原因？のエラーをなんとかする
todo: エラー処理書け

"""
import requests
import cv2
import glob
import os
import dotenv
import hashlib
from random import random
from datetime import datetime
from joblib import Parallel, delayed

path = os.path.join(os.path.dirname(__file__), ".env")
dotenv.load_dotenv(path)
API_KEY = os.environ.get("FACE_API_KEY")

FILE_PATH_LIST = glob.glob("..\\images\\*\\*")


def call_api(binary_image, api_key):
    """
    call face api.
    :param binary_image:
    :return: response.json())
    """
    URL = "https://eastasia.api.cognitive.microsoft.com/face/v1.0/detect"

    headers = {'Content-Type': 'application/octet-stream',
               'Ocp-Apim-Subscription-Key': api_key,
               }

    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
    }
    res = requests.post(url=URL, params=params, headers=headers, data=binary_image)

    return res.json()


def detect_face_areas(response_json):
    """
    detect face area.

    :param response_json:
    :return:
    """
    top = response_json['faceRectangle']['top']
    left = response_json['faceRectangle']['left']
    width = response_json['faceRectangle']['width']
    height = response_json['faceRectangle']['height']

    return top, left, width, height


def create_saving_path(file_path):
    save_dir = "..\\face_images\\"

    ext = file_path.split(".")[-1]
    image_dir, filename = file_path.split("\\")[2:]
    image_dir = save_dir + image_dir
    filename = hashlib.md5(f"{filename}+{random()}".encode("utf-8")).hexdigest() + f".{ext}"

    file_path = os.path.join(image_dir, filename)
    return file_path


def save_face_area(image_file_path, x_, y_, w_, h_):
    # save face area as image file.

    image = cv2.imread(image_file_path)
    image_file_path = create_saving_path(image_file_path)
    image = image[x_:x_ + h_, y_:y_ + w_]  # 顔領域を切り出す
    cv2.imwrite(image_file_path, image)


def make_dir(dir_path):
    dir_path = dir_path.split("\\")[-1]
    dir_path = os.path.join("..\\face_images", dir_path)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def write_log(log_file, image_path, response):
    with open(log_file, "a") as log:
        log_text = datetime.strftime(datetime.now(), "<%Y-%m-%d %H:%M:%S>") + " " \
                   + "Found_face " + f"[{image_path}] " + "Result " + str(response) + "\n"
        log.write(log_text)


def main_process(image_file_path, apk):
    LOG_FILE = ".\\save_faces_log.txt"

    with open(image_file_path, "rb") as f:
        img = f.read()
        response = call_api(img, apk)

        if response == []:
            print(f"No result: {image_file_path}")
            write_log(LOG_FILE, image_file_path, response)
        else:
            for r in response:
                x, y, w, h = detect_face_areas(r)
                save_face_area(image_file_path, x, y, w, h)
                print(f"Save a face of {image_file_path}")
                write_log(LOG_FILE, image_file_path, r)


# Parallel(n_jobs=-1)([delayed(main_process)(file_path, API_KEY) for file_path in file_path_list])

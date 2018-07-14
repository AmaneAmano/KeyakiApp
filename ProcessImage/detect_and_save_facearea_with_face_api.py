"""
Using Azure FaceAPI, detect faces.
save face image to output directory

todo: 並列処理の実装
todo:  ログ出力機能
todo: 省メモリ

"""
import requests
import cv2
import glob
import os
import dotenv


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


def save_face_area(image_file_path, x_, y_, w_, h_):
    # save face area as image file.

    image = cv2.imread(image_file_path)
    file_name = image_file_path.split("\\")[2]
    image = image[x_:x_ + h_, y_:y_ + w_]  # 顔領域を切り出す
    cv2.imwrite(".\\output\\" + file_name, image)


if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), ".env")
    dotenv.load_dotenv(path)
    API_KEY = os.environ.get("FACE_API_KEY")

    file_path_list = glob.glob(".\\sample\\*")


def main(image_file_path, apk):
    with open(image_file_path, "rb") as f:
        img = f.read()
        response = call_api(img, apk)

        if response == []:
            print(f"No result: {image_file_path}")
        else:
            for r in response:
                x, y, w, h = detect_face_areas(r)
                save_face_area(image_file_path, x, y, w, h)
                print(f"Save a face of {image_file_path}")

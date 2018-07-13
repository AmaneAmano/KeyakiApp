import os
import cv2
import json
import codecs
from joblib import Parallel, delayed


def compare_hists(target_image_path, comparing_image_path):
    """

    :param target_image_path:
    :param comparing_image_path:
    :return: result of compareHist(), target_image_path, comparing_image_path
    """
    # read images
    target_image = cv2.imread(target_image_path)
    comparing_image = cv2.imread(comparing_image_path)
    # image size. hight and width
    target_hight, target_width = target_image.shape[:2]
    comparing_hight, comparing_width = comparing_image.shape[:2]
    # resize images
    target_image = cv2.resize(target_image,
                              (target_hight // 2, target_width // 2),
                              interpolation=cv2.INTER_AREA)
    comparing_image = cv2.resize(comparing_image,
                                 (comparing_hight // 2, comparing_width // 2),
                                 interpolation=cv2.INTER_AREA)
    # calculate image hists
    target_hist = cv2.calcHist([target_image], [0], None, [256], [0, 256])
    comparing_hist = cv2.calcHist([comparing_image], [0], None, [256], [0, 256])
    # compare hists
    correlation = cv2.compareHist(target_hist, comparing_hist, 0)

    return correlation, target_image_path, comparing_image_path


def is_over_threshold(correlation, threshold=0.98):
    if correlation > threshold:
        return True
    else:
        return False


def create_file_path_list(directory_path):
    file_list = os.listdir(directory_path)
    result = []
    for file in file_list:
        result.append(os.path.join(directory_path, file))

    return result


def create_dir_path_list(root_path):
    dir_list = os.listdir(root_path)  # rootディレクトリ下のdirリスト
    result = []
    for directory in dir_list:
        result.append(os.path.join(path, directory))

    return result


def process_comparison_file_list(file_path__list):
    file_list_length = len(file_path__list)

    output = dict()
    for i in range(1, file_list_length):
        target_file = file_path__list[i - 1]

        tmp = list()
        for j in range(i, file_list_length):
            corr, target, comparing = compare_hists(target_file, file_path__list[j])
            if is_over_threshold(corr):
                x = [comparing, corr]
                tmp.append(x)
        output[target_file] = tmp

    return output


if __name__ == "__main__":
    path = "..\\images"
    dir_path_list = create_dir_path_list(path)

    for dir_path in dir_path_list:
        file_path_list = create_file_path_list(dir_path)
        # dir_result = Parallel(n_jobs=-1)([delayed(process_comparison_file_list)(fp) for fp in file_path_list])
        dir_result = process_comparison_file_list(file_path_list)
        with codecs.open(".\\duplicate_images.json", "a", "utf-8") as f:
            json.dump(dir_result, f, ensure_ascii=False, indent=2)












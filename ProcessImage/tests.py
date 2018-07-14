import unittest
import glob
import detect_and_save_facearea_with_face_api as dff


class TestDetectFace(unittest.TestCase):
    """
    test  detect_and_save_facearea_with_face_api.py
    """

    def test_create_file_path(self):
        path = "..\\images\\akane_moriya\\00001_akane_moriya.jpg"
        exp = "..\\face_images\\akane_moriya\\00001_akane_moriya.jpg"
        self.assertEqual(exp, dff.create_saving_path(path))


if __name__ == "__main__":
    unittest.main()
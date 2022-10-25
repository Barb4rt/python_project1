import requests
import re


class Download:
    """A class for download data"""

    @staticmethod
    def download_image(name, image_url, path):
        """
        static method to download an image

        Args:
            name (string): How name the image
            image_url (string): Where is the image
            path (string): Where save the image
        """
        filename = re.sub("[^A-Za-z0-9]", "", name)
        file_ext = image_url.split(".", -1)[-1]
        filename = filename + "." + file_ext
        img_data = requests.get(image_url, stream=True).content
        with open(path + filename, "wb") as fi:
            fi.write(img_data)
            fi.close

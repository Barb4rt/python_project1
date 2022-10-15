
import threading
import requests
import re
from queue import Empty

class DownloadImage():
    def __init__(self, q ):
        self.q = q

    def add_to_queue(self, name, image_url, path):
        add_thread = threading.Thread(target=self._set_to_queue , args=(name, image_url, path,))
        add_thread.start()

    def _set_to_queue(self, name, image_url, path):
        self.q.put(self.download_image_in_queue(name, image_url, path))

    def download_image_in_queue(self, name, image_url, path):
        filename = re.sub('[^A-Za-z0-9]', '', name)
        file_ext = image_url.split(".", -1)[-1]
        filename = filename + '.'+file_ext
        img_data = requests.get(image_url, stream=True).content
        with open(path+filename, 'wb') as fi:
            fi.write(img_data)
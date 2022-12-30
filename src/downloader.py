import threading
import requests, time
import os, re
from tqdm import tqdm

from src.constants import *

class MediaDownloader:
    def init(self, urls):
        self.urls = urls
        self.threads = []
        self.download_path = DOWNLOAD_PATH
        # self.user_name = ''
        
    def download(self, url, file_name):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(os.path.join(self.download_path, file_name) , 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        else:
            print("Error downloading file")

    def run(self):
        i = 0
        for url in tqdm(self.urls):
            file_name = url.split("/")[-1]
            thread = threading.Thread(target=self.download, args=(url, file_name))
            thread.start()
            self.threads.append(thread)
            i += 1
            if i%200 == 0:
                time.sleep(1)
        
        for thread in self.threads:
            thread.join()
        
        print("All files have been downloaded.")
        
        
    def start_down(self, urls, user_name):
        self.urls = urls
        self.threads = []
        self.download_path = os.path.join(DOWNLOAD_PATH, user_name)
        self.run()


downloader = MediaDownloader()

def download_user_media(user_name):
    USER_FOLDER = os.path.join(DOWNLOAD_PATH, user_name)
    CSV_FILE = os.path.join(USER_FOLDER, user_name + ".csv")
    txt = ''
    with open(CSV_FILE, 'r') as f:
        txt = f.read()
    to_match = 'https://64.media.tumblr.com/.*?\.jpg'
    urls = re.findall(to_match, txt)
    downloader.start_down(urls, user_name)
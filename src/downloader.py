import threading
import requests, time
import os, re
from tqdm import tqdm

from src.constants import *

class MediaDownloader:
    def init(self, urls):
        self.urls = urls
        self.threads = []
        self.middle = False
        self.download_path = DOWNLOAD_PATH
        # self.user_name = ''
        
    def download(self, url, file_name):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(os.path.join(self.download_path, file_name) , 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        else:
            # print("Error downloading file")
            pass

    def run(self, downloaded_files):
        i = 0
        for url in tqdm(self.urls):
            file_name = url.split("/")[-1]
            if file_name in downloaded_files:
                continue
                        
            thread = threading.Thread(target=self.download, args=(url, file_name))
            thread.start()
            self.threads.append(thread)
            
            if i%400 == 0 and i != 0:
                print("\nPausing download for 60 seconds\n")
                time.sleep(10)
                return
                print("\nResuming download\n")
            i+=1
        for thread in self.threads:
            thread.join()
        
        print("All files have been downloaded.")
        
        
    def start_down(self, urls, user_name, middle = False):
        if middle:
            self.middle = True
        self.urls = urls
        self.threads = []
        self.download_path = os.path.join(DOWNLOAD_PATH, user_name)
        downloaded_files = os.listdir(self.download_path)
        self.run(downloaded_files)


downloader = MediaDownloader()

def download_user_media(user_name, middle = False):
    USER_FOLDER = os.path.join(DOWNLOAD_PATH, user_name)
    CSV_FILE = os.path.join(USER_FOLDER, user_name + ".csv")
    txt = ''
    with open(CSV_FILE, 'r', encoding='utf8') as f:
        txt = f.read()
    to_match = 'https://64.media.tumblr.com/.*?\.[jpgn]{3,4}'
    urls = re.findall(to_match, txt)
    downloader.start_down(urls, user_name, middle)
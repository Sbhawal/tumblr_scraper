import os, shutil
import pandas as pd
from PIL import Image
from tqdm import tqdm
import time, warnings
warnings.filterwarnings("ignore")

dest = r'C:\Users\mailt\Desktop\github_projects\folder_sync'
CSV = "image_darkness.csv"
backup_loc = r'D:\tumblr'
src = r'C:\Users\mailt\Desktop\github_projects\tumblr_scraper'

df = pd.DataFrame(columns=['image', 'darkness'])
if os.path.exists(CSV):
    df = pd.read_csv(CSV)
  
def return_percent_image_dark(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    width, height = img.size
    pixels = img.load()
    dark_pixels = 0
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            if r < 100 and g < 100 and b < 100:
                dark_pixels += 1
    percent_dark = (dark_pixels / (width * height)) * 100
    return percent_dark


def add_entry_to_df(image, darkness):
    global df
    df = df.append({'image': image, 'darkness': darkness}, ignore_index=True)


def save_df():
    global df
    df.to_csv(CSV, index=False)
    
def scrape_throught_src(src):
    global df
    image_paths = df['image'].tolist()
    i = 0
    for root, dirs, files in os.walk(src):
        # print("\n", root)
        if len(files) > 5:
            for file in tqdm(files):
                try:
                    file_path = os.path.join(root, file)
                    if file_path not in image_paths:
                        darkness = return_percent_image_dark(file_path)
                        add_entry_to_df(file_path, darkness)
                        image_paths.append(file_path)
                    if i%25 == 0:
                        save_df()
                except:
                    pass

while True:
    scrape_throught_src(src)
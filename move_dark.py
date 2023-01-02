import os, shutil
import pandas as pd
from tqdm import tqdm
import time, warnings
warnings.filterwarnings("ignore")

dest = r'C:\Users\mailt\Desktop\github_projects\folder_sync'
CSV = "image_darkness.csv"
done_files_txt = r"txt\done_files.txt"
backup_loc = r'D:\tumblr'
src = r'C:\Users\mailt\Desktop\github_projects\tumblr_scraper'

try:
    with open(done_files_txt, "r") as f:
        done_files = f.read().split("\n")
except:
    with open(done_files_txt, "w") as f:
        f.write("")
    done_files = []
    
    

df = pd.DataFrame(columns=['image', 'darkness'])
if os.path.exists(CSV):
    df = pd.read_csv(CSV)
  
  
def remove_done_files_from_db():
    global df
    global done_files
    df = df[~df['image'].isin(done_files)]
    df.to_csv(CSV, index=False)
 
def move_top_2_percentile():
    global df
    global dest
    global done_files
    remove_done_files_from_db()
    df = df.sort_values(by=['darkness'], ascending=False)
    top_2_percentile = df['darkness'].quantile(0.98)
    print("Total images: ", len(df))
    print("Top 2 percentile values: ", top_2_percentile)
    top_2_percentile_df = df[df['darkness'] >= top_2_percentile]
    print("Total images in top 2 percentile: ", len(top_2_percentile_df))
    for index, row in tqdm(top_2_percentile_df.iterrows()):
        try:
            image = row['image']
            dest_path = os.path.join(dest, image.split("\\")[-1])
            shutil.copy(image, dest_path)
            done_files.append(image)
        except Exception as e:
            print(e)
            pass
    with open(done_files_txt, "w") as f:
        f.write("\n".join(done_files))

move_top_2_percentile()
             
             


from src.constants import *
from src.downloader import *
import os, re
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

def extract_photos(photo_dataframe):
  photo_urls = []
  for photo in photo_dataframe:
    photo_urls.append(photo['original_size']['url'])
  return ("+").join(photo_urls)

def parse_post(post):
  post_id = post['id']
  post_type = post['type']
  tags = re.sub(r"[\[\]']", '', str(post['tags']))
  reblog_key = post['reblog_key']
  try:
    post_url = extract_photos(post['photos'])
  except:
    post_url =  '-'
  return [post_id, post_type, tags, reblog_key, post_url]

def add_to_dataframe(response):
    global post_dataframe
    for post in response['posts']:
        parsed_post = parse_post(post)
        post_dataframe = post_dataframe.append(pd.Series(parsed_post, index=post_dataframe.columns), ignore_index=True)

def write_dataframe_to_csv(dataframe, filename):
  dataframe.to_csv(filename, index=False)
  # print("Dataframe written to csv")
  
  
def get_starting_point(filename):
    try:
        temp = pd.read_csv(filename)
        start = temp.shape[0]
        return start
    except:
        return 0
  
def get_posts_from_blog(user_name, stop=-1):
    blog_name = user_name + ".tumblr.com"
    USER_FOLDER = os.path.join(DOWNLOAD_PATH, user_name)
    response = client.posts(blog_name)
    total_posts = response['total_posts']
    try:
        os.makedirs(USER_FOLDER)
    except FileExistsError:
        pass
    CSV_FILE = os.path.join(USER_FOLDER, user_name + ".csv")
    START = 0
    if total_posts >= 50:
      
      START = get_starting_point(CSV_FILE)
           
      if total_posts - START <= 60:
        print("Already scraped all posts")
        return

      print("\nTotal posts: ", total_posts)
      print("Starting from: ", START, '\n')
      time.sleep(2)
      
    for i in tqdm(range(START, total_posts, limit)):
        if i%500 == 0 and i != 0:
            write_dataframe_to_csv(post_dataframe, CSV_FILE)
            # print("\n\nStarting to download media files, Scraping Paused.\n")
            # time.sleep(5)
            # download_user_media(user_name, middle = True)
            # print("\n\nResuming Scraping.\n")
        
        response = client.posts(blog_name, offset=i, limit=50)
        add_to_dataframe(response)
        if i%stop == 0 and i != 0 and stop>0:
          write_dataframe_to_csv(post_dataframe, CSV_FILE)
          return
    write_dataframe_to_csv(post_dataframe, CSV_FILE)
    
    print("\nCompleted scraping\n")
    


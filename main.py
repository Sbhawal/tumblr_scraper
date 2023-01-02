from src.constants import *
from src.helper_functions import *
from src.downloader import *
import random

with open("include.txt", "r") as f:
    unames = f.read().split("\n")




while True:
    for user_name in random.sample(unames, len(unames)):
        print(user_name)
    # user_name = input("Enter the user name: ")
    # if user_name.count("tumblr.com") == 1:
    #     user_name = re.findall(r"//(.+?)\.", user_name)[0]
        get_posts_from_blog(user_name, stop=501)
        download_user_media(user_name)
        # time.sleep(60)
# download_user_media('darkscollection')
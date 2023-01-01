from src.constants import *
from src.helper_functions import *
from src.downloader import *

user_name = input("Enter the user name: ")
if user_name.count("tumblr.com") == 1:
    user_name = re.findall(r"//(.+?)\.", user_name)[0]


# get_posts_from_blog(user_name)



download_user_media(user_name)
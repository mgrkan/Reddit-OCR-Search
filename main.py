import praw
from pytesseract import image_to_string
import requests
import io
from PIL import Image
from fuzzywuzzy import fuzz

reddit = praw.Reddit(Auth)

sub_input = input("subreddit: ") #Which sub to search 
post_input = input("post: ") #What was written on the image (Doesn't need to be %100 accurate)

sub = reddit.subreddit(sub_input)

hot_sub = sub.hot(limit = 1000) #I always scroll in hot

imgs = [] #List for storing reddit image urls
results = [] #List for the images that are matching with the post_input

for post in hot_sub:
    if not post.stickied:
        url = post.url
        imgs.append(url)


for link in imgs:
    
    if ".jpg" or ".jpeg" or ".png" or ".gif" in link: #I once scraped an imgur link without any file extensions 

        response = requests.get("{}".format(link))

        img = Image.open(io.BytesIO(response.content))

        ratio = fuzz.ratio(post_input.lower(), image_to_string(img).lower())
    
        if ratio >= 50:
            results.append(link)
    elif (".jpg" or ".jpeg" or ".png" or ".gif" in link) == False:
        
        try:
            response = requests.get("{}.jpg".format(link))
            img = Image.open(io.BytesIO(response.content))
            ratio = fuzz.ratio(post_input.lower(), image_to_string(img).lower())
            if ratio >= 50:
                results.append(link)
        except:
            try:
                response = requests.get("{}.jpeg".format(link))
                img = Image.open(io.BytesIO(response.content))
                ratio = fuzz.ratio(post_input.lower(), image_to_string(img).lower())
                if ratio >= 50:
                    results.append(link)
            except:
                try:
                    response = requests.get("{}.png".format(link))
                    img = Image.open(io.BytesIO(response.content))
                    ratio = fuzz.ratio(post_input.lower(), image_to_string(img).lower())
                    if ratio >= 50:
                        results.append(link)
                except:
                    try:
                        response = requests.get("{}.gif".format(link))
                        img = Image.open(io.BytesIO(response.content))
                        ratio = fuzz.ratio(post_input.lower(), image_to_string(img).lower())
                        if ratio >= 50:
                            results.append(link)
                    except:
                        pass
    else:
        pass

print(results) #Finally prints the matching image links

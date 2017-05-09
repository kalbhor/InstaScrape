from os import mkdir, path
from bs4 import BeautifulSoup
import urllib.request


def get_img_urls(source, count):

    img_urls = []

    response = source.split('class="_nljxa">',1)[1]
    soup = BeautifulSoup(response, "html.parser")

    for i in soup.find_all('img', {'class' : '_icyx7'}):
    	img_urls.append(i.get('src'))

    return img_urls

        
def download_imgs(img_list, user, x):

    if path.exists(user) == False:
        mkdir(user)

    for url in img_list:
        val = url.split('/')[-1]
        urllib.request.urlretrieve(url, "{}/{}".format(user, val))  


def convert_to_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
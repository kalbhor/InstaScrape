from os import mkdir, path
from sys import argv
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib.request


def simulate_page(user, count):
    
    page_url = "https://instagram.com/{user}".format(user=user)

    driver = webdriver.PhantomJS()
    driver.get(page_url)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element_by_css_selector('._8imhp._glz1g').click()

    if count > 24:
        loop_count = 1 + (count - 24)/12
        i = 0

        while i <= loop_count:
            if wait_for_visibility(driver, 23 + i*12):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(0.05)
                i = i + 1
            else:
                pass


    source = driver.page_source
    driver.close()

    return source


def get_img_urls(source, count):

    img_urls = []

    response = source.split('class="_nljxa">',1)[1]
    soup = BeautifulSoup(response, "html.parser")

    for i in soup.find_all('img', {'class' : '_icyx7'}):
    	img_urls.append(i.get('src'))

    print(len(img_urls))

    return img_urls[:count]

        
def download_imgs(img_list, user):

    if path.exists(user) == False:
        mkdir(user)
	
    for i,val in enumerate(img_list):
        urllib.request.urlretrieve(val, "{}/{}.jpg".format(user, i))

def wait_for_visibility(driver, num):

    try:
        element = driver.find_element_by_id('pImage_{}'.format(num))
        if element.is_displayed():
            return True
    except Exception as e:
        return False

        
if __name__ == '__main__':
    
    user = argv[1]
    count = int(argv[2])
    source = simulate_page(user, count)
    imgs = get_img_urls(source, count)
    print(len(imgs))
    download_imgs(imgs, user)
    

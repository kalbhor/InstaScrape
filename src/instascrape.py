from os import mkdir, path
from sys import argv
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from progress.bar import Bar, FillingSquaresBar
import threading
import urllib.request

def get_number_posts(driver, user):

    source = driver.page_source 
    soup = BeautifulSoup(source, "html.parser")
    posts = soup.find('span', {'class' : '_bkw5z'}).get_text()

    return int(posts)


def scroll_page(driver, count, num ):

    loop_count = int(1 + (count - 24)/12)
    loading_bar = Bar('Scraping', max=loop_count+1, suffix='%(percent)d%%')

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element_by_css_selector('._8imhp._glz1g').click()

    if count > 24:
        i = 0
        while i <= loop_count:
            if wait_for_visibility(driver, 22 + i*12):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(0.05)
                i += 1
                loading_bar.next()
            elif wait_for_visibility(driver, num-1):
                break
            else:
                sleep(0.05)
        loading_bar.finish()

    return driver


def simulate_page(user, count):

    page_url = "https://instagram.com/{user}".format(user=user)
    driver = webdriver.Chrome()
    driver.get(page_url)

    num = get_number_posts(driver, user)

    count = (num if count > num else count)

    print("Requesting page..\n")

    driver = scroll_page(driver, count, num )
    source = driver.page_source
    driver.close()  

    return source


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

    loading_bar = Bar('Thread #{}'.format(x), max=len(img_list), suffix='%(index)d/%(max)d')
	
    for url in img_list:
        val = url.split('/')[-1]
        urllib.request.urlretrieve(url, "{}/{}".format(user, val))
        loading_bar.next()
    loading_bar.finish()
    

def wait_for_visibility(driver, num):
    try:
        element = driver.find_element_by_id('pImage_{}'.format(num))
        if element.is_displayed():
            return True
    except Exception as e:
        return False


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def command_line():
    user = argv[1]
    count = int(argv[2])
    source = simulate_page(user, count)
    imgs = get_img_urls(source, count)
    print(len(imgs))
    c = input('>')
    c = int(c)
    x = 1
    
    for i in chunks(imgs, c):
        t = threading.Thread(target=download_imgs, args=(i, user, x,))
        t.start()
        x += 1
    
    download_imgs(imgs, user, x)


if __name__ == '__main__':
    command_line()
    

    

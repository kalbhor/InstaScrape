from os import mkdir, path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib.request

from time import sleep
def simulate_page(user):
    
    page_url = "https://instagram.com/{user}".format(user=user)

    driver = webdriver.Chrome()
    driver.get(page_url)
    #delay = 5

    #try:
    #    element = WebDriverWait(driver, delay).until(
    #    EC.presence_of_element_located((By.XPATH, '//*[@class="_i572c notranslate"]')))
    #except TimeoutException:
    #    print("Timeout")
    #    exit()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element_by_css_selector('._8imhp._glz1g').click()

    for i in range(21):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)


    sleep(2)
    source = driver.page_source
    driver.close()

    return source


def get_img_urls(source):

    img_urls = []

    response = source.split('class="_nljxa">',1)[1]
    soup = BeautifulSoup(response, "html.parser")

    for i in soup.find_all('img', {'class' : '_icyx7'}):
    	img_urls.append(i.get('src'))

    return img_urls

        
def download_imgs(img_list, user):

    if path.exists(user) == False:
        mkdir(user)
	
    for i,val in enumerate(img_list):
        urllib.request.urlretrieve(val, "{}/{}.jpg".format(user, i))

        
if __name__ == '__main__':
    user = input('>')
    source = simulate_page(user)
    imgs = get_img_urls(source)
    print(len(imgs))
    download_imgs(imgs, user)
    

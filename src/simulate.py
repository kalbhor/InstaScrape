from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from progress.bar import Bar, FillingSquaresBar


def number_posts(*, driver, user):

    element = driver.find_element_by_css_selector('._bkw5z') 
    posts = element.get_attribute('innerHTML')

    return int(posts)


def scroll_page(*, driver, count, num ):

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


def main_page(*, driver, user, count):

    page_url = "https://instagram.com/{user}".format(user=user)
    driver.get(page_url)

    num = number_posts(driver = driver, user = user)

    count = (num if count > num else count)

    print("Requesting page..\n")

    driver = scroll_page(driver = driver, count = count, num = num )
    source = driver.page_source
    driver.close()  

    return source


def wait_for_visibility(driver, num):

    try:
        element = driver.find_element_by_id('pImage_{}'.format(num))
        if element.is_displayed():
            return True
    except Exception as e:
        return False

    

    

import utils
import simulate
from selenium import webdriver
import threading
from sys import argv


def command_line():
    user = argv[1]
    count = int(argv[2])
    driver = webdriver.Chrome()
    source = simulate.main_page(driver = driver, user = user, count = count)
    imgs = utils.get_img_urls(source, count)
    imgs = imgs[:count]
    print(len(imgs))
    c = 12
    c = int(len(imgs)/int(c))
    x = 1
    
    for i in utils.convert_to_chunks(imgs, c):
        t = threading.Thread(target=utils.download_imgs, args=(i, user, x,))
        t.start()
        x += 1

if __name__ == '__main__':
    command_line()
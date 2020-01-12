import os
import time
from pathlib import Path
from urllib.request import Request, urlopen
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

_IMAGE_BATCH_SIZE_ = 80

searchQuery = '"Rice+paper+-+idea+leuconoe"+-egg+-caterpillar'
queryLimit = 160
imageLinks = []

modulePath = Path(__file__).parent
driverPath = (modulePath/'drivers/chromedriver.exe').resolve()
chromeBinaryPath = (modulePath/'chrome-win/chrome.exe')

downloadDir = (modulePath/'train/rice_paper')

opts = Options()
opts. binary_location = str(chromeBinaryPath)
opts.headless = True

assert opts.headless
browser = Chrome(executable_path=str(driverPath), options=opts)


def loadMore():
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(0.5)
    try:
        browser.find_element_by_id('smd').click()
        time.sleep(0.5)
    except:
        pass

def downloadImage(image_url, downloadDir):
    try:
        os.makedirs(str(downloadDir))
    except OSError as e:
        if e.errno != 17:
            raise
        pass
        
    req = Request(str(image_url))
    response = urlopen(req, None, 10)
    imagedata = response.read()
    response.close()
    
    image_name = str(image_url)
    image_name = image_name[48:len(image_name) - 2] + '.png'

    try:
        image_file = open(str(downloadDir) + "/" + image_name, 'wb')
        image_file.write(imagedata)
        image_file.close()
    except IOError as e:
        raise e
    except OSError as e:
        raise e
        

def scrape(searchQuery, queryLimit, downloadDir):
    browser.get('https://www.google.com/search?tbm=isch&q=' + searchQuery)
    for i in range(queryLimit//_IMAGE_BATCH_SIZE_ - 1):
        loadMore();

    imageLinks = [image.get_attribute("data-src") for image in browser.find_elements_by_class_name('rg_ic') if image.get_attribute("data-src")]

    print(len(imageLinks))

    for image_url in imageLinks:
        downloadImage(image_url, downloadDir)


scrape(searchQuery, queryLimit, downloadDir)

browser.close()
quit()
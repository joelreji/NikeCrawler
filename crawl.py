import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

productDict = {}
baseUrl = "https://www.nike.com"
search = "Converse CTAS Duck Boot x AMBUSH 'Black' Release Date"
pref_size = "M 7.5 / W 9.5"
email = "jreji@ncsu.edu"
pwd = "Test1234"
cvv = 849

# Connect to URL for SNKR
SNRKS_URL = baseUrl + "/launch?cp=65052578087_search_%7Cnike%20snkrs%7Cg%7C11856077755%7C115377939556%7Ce%7Cc&s=in-stock"

# Send request and grab the results
page = requests.get(SNRKS_URL)
soup = BeautifulSoup(page.content, 'html.parser')
productList = soup.find_all('figure', class_='pb2-sm va-sm-t ncss-col-sm-6 ncss-col-md-3 ncss-col-xl-2 prl1-sm')

# Iterate through elements till you find the element you want
for product in productList:
    productSelected = (product.find('a', class_="card-link d-sm-b")["aria-label"]).strip()
    if productSelected == search:
        productDict[productSelected] = (product.find('a', class_="card-link d-sm-b")["href"]).strip()
        # print(productDict)
        break

# Setting up Selenium with headless operation to trigger clicks
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
#options.add_argument('--headless')
driver = webdriver.Chrome("/Users/joelreji/Downloads/chromedriver", chrome_options=options)
driver.get(baseUrl + productDict[search])
# print(baseUrl + productDict[search])

# Getting all the size buttons that are available and selecting the preferred one
size_buttons = driver.find_elements_by_xpath("//li[@class='size va-sm-m d-sm-ib va-sm-t ta-sm-c  ' and @data-qa='size-available']")
for size in size_buttons:
    if size.text.strip() == pref_size.strip():
        # print("Size is available!")
        # print(size.text)
        size.click()
        break

# Get Add to Cart Button and click it
add_button = driver.find_element_by_xpath("//button[@type='button' and @data-qa='add-to-cart']")
add_button.click()

# Go to your Cart and click Checkout
driver.get(baseUrl + "/us/en/cart")
checkout_button = driver.find_element_by_xpath("//button[@type='button' and @data-automation='go-to-checkout-button']")
driver.implicitly_wait(5)
driver.get(baseUrl + "/checkout/tunnel")

# Entering login information and authenticating
inputUser = driver.find_element_by_xpath("//input[@type='email' and @data-componentname='emailAddress']")
inputUser.send_keys(email)
inputPwd = driver.find_element_by_xpath("//input[@type='password' and @data-componentname='password']")
inputPwd.send_keys(pwd)
driver.find_element_by_xpath("//input[@value='MEMBER CHECKOUT']").click()

# Enter security code for CC and Review order
driver.find_element_by_xpath("//button[@type='button' and @class='continuePaymentBtn']").click()
inputCV = driver.find_element_by_id("cvNumber")
inputCV.send_keys(cvv)
driver.find_element_by_xpath("//button[@data-attr='continueToOrderReviewBtn']").click()




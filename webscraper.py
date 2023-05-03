from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import time
from geopy import Nominatim
import json


def click_button_with_xpath(driver, wait, xpath):
    WebDriverWait(driver, wait).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()

def click_button_with_selector(driver, wait, sel):
    WebDriverWait(driver, wait).until(EC.element_to_be_clickable((By.CSS_SELECTOR,sel))).click()


# This 4 files have to be replaced by your own paths
driver = webdriver.Chrome("C:\\bin\\chromedriver.exe")
json_file = "reviews.json"
geojson_file = "reviews.geojson"
location_file = "locations.txt"


# read and modify the location names so that they can added to the url
# google needs lpus instaed of single space in url
with open(location_file, 'r', encoding='utf-8') as file:
    location_list_str = file.read()

location_list_with_plus = location_list_str.replace(" ","+")

locations = location_list_with_plus.split(";")


## main url
url = 'https://www.google.com/maps/search/'


# some path and class names for scraping
xpath = {
    "coockies": '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button',
    "all_reviews": '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[24]/div/div[2]/button',
    "all_reviews2": '.HHrUdb.fontTitleSmall.rqjGif'
    }

classes = {
    "reviews": 'jJc9Ad',
    "show_more_button": 'w8nwRe kyuRq',
    "adress": 'Io6YTe fontBodyMedium',
    "review_text": 'wiI7pd',
    "rating": 'kvMYJc',
    "date": 'rsqaWe',
    }


# set  i to 0 

# Important: If the webscraper stoped, you can set the counter to the last i
i = 0
first_try = True

# for every location
while i < len(locations):
    # search location
    search_url = url + locations[i]
    driver.get(search_url)
    name = locations[i].replace("+"," ")
    
    action = ActionChains(driver)
    
    # accept coockies
    if first_try == True:
        click_button_with_xpath(driver, 10, xpath['coockies'])
        first_try = False
        time.sleep(2)
    
    # get html
    response = BeautifulSoup(driver.page_source, 'html.parser')
    result_found = True
    try:
        adress = response.find('div', class_= classes["adress"]).text
    except:
        result_found = False
        
    if result_found == True:
        try: 
            # Adress and geotag
            locator = Nominatim(user_agent= "myGeocoder")
            coordinates = locator.geocode(adress)
            longitude = coordinates.longitude
            latitude = coordinates.latitude
        except:
            longitude = 0
            latitude = 0
        
        reviews_exitst = True
        try:
            click_button_with_selector(driver, 3, xpath['all_reviews2'])
        except:
            reviews_exitst = False
        time.sleep(2.5)
        
        if reviews_exitst == True:
        
        
            scrollable_div = driver.find_element(By.CSS_SELECTOR,
              '.m6QErb.DxyBCb.kA9KIf.dS8AEf'
                                  )
            
            
            # move to element operation
            action.move_to_element(scrollable_div)
            
        
            response_old = BeautifulSoup(driver.page_source, 'html.parser')
            new_content = True
            #scroll review list down while new content
            while new_content == True:
                driver.execute_script(
                                     'arguments[0].scrollTop = arguments[0].scrollHeight', 
                                      scrollable_div
                                      )
                time.sleep(2.5)
                response_new = BeautifulSoup(driver.page_source, 'html.parser')
                if (response_old == response_new):
                    new_content = False
                else:
                    response_old = response_new
            
 
            try: #click on show more on every entry
                elements = WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.w8nwRe.kyuRq')))
                for btn in elements:
                    btn.click()
            except Exception as e: 
                print(e)
            
            response = BeautifulSoup(driver.page_source, 'html.parser')
            rlist = response.find_all('div', class_= classes["reviews"])
            #get all list as reviews
            
            
            for r in rlist:

                try:
                    review_text = r.find('span', class_=classes["review_text"]).text
                    rating = r.find('span', class_=classes["rating"])['aria-label'][1]
                    date = r.find('span', class_=classes["date"]).text
                    json_out = {
                        "location": name,
                        "adress": adress,
                        "review": review_text,
                        "rating": rating,
                        "date": date,
                        "longitude": longitude,
                        "latidude": latitude
                        }
                    geojson_out = {
                        "type": "Feature",
                        "geometry" : {
                            "type": "Point",
                            "coordinates": [longitude, latitude],
                            },
                        "properties": {
                            "location": name,
                            "adress": adress,
                            "review": review_text,
                            "rating": rating,
                            "date": date
                            }
                        }
                    print(geojson_out)
                    #write to outfile
                    with open (json_file, 'a', encoding='utf8') as outfile:
                        json.dump( json_out, outfile, ensure_ascii=False)
                        outfile.write("\n,")
                    with open (geojson_file, 'a', encoding='utf8') as outfile:
                        json.dump( geojson_out, outfile, ensure_ascii=False)
                        outfile.write("\n,")
            
                except Exception as e:
                    print(e)
    i+=1
    print (i)
        








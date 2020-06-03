from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.flipkart.com/"
driver = webdriver.Chrome(r"E:\Projects\Flipkart Scraper\chromedriver.exe")
driver.get(url)

page = driver.page_source

soup = BeautifulSoup(page,"html.parser")


div_tag   = soup.find("div",class_ ="_3zdbog _3Ed3Ub")

listings = div_tag.find_all("li",class_="Wbt_B2 _1YVU3_")

category_list = []
df = pd.DataFrame()
for category in listings:
    # Main topics like Electronics, men,Women
    category_list.append(category.find("span","_1QZ6fC _3Lgyp8").text)
    # In each topic like Electronics under that we find mobiles, laptops etc
    sub_categories = category.find_all("li",class_="_2GG4xt")  
    for item in sub_categories:
        differentiate_li = []
        get_all_li_tags = item.find_all("li")
        # Getting the class names to categorize them
        for li in get_all_li_tags:
            differentiate_li.append((" ".join(li.get("class"))))
        # getting indexes of the sub categories
        indices = [i for i, x in enumerate(differentiate_li) if x == "_1KCOnI _2BfSTw _1h5QLb _3ZgIXy" or x=="_1KCOnI _2BfSTw"]
        if len(indices)==1:
            start = indices[0]
            temp = get_all_li_tags[start+1:]
            for i in temp:
                temp_df  = pd.DataFrame({'category':[category.find("span","_1QZ6fC _3Lgyp8").text],'sub_category':[get_all_li_tags[start].text],'item':[i.text],'item_link':["https://www.flipkart.com"+i.find("a",href = True)['href']]})
                df = df.append(temp_df)
        else:
            for idx in range(len(indices)):
                print("The index ",idx)
                if idx == indices.index(indices[-1]):
                    print(idx)
                    start = indices[idx]
                    end   =  len(differentiate_li)-1
                    temp = get_all_li_tags[start+1:end+1]
                else:
                    start = indices[idx]
                    end = indices[idx+1]
                    temp  = get_all_li_tags[start+1:end]
                print("The length of temp: ",len(temp))
                print("The start is ",start,"The end is ",end)
                    
                if len(temp) > 0:
                    for i in temp:
                        print(i.text)
                        try:
                            item_link = i.find("a",href = True)['href']
                        except:
                            item_link  = ""
                        temp_df  = pd.DataFrame({'category':[category.find("span","_1QZ6fC _3Lgyp8").text],'sub_category':[get_all_li_tags[start].text],'item':[i.text],'item_link':["https://www.flipkart.com"+item_link]})
                        df = df.append(temp_df)
                elif len(temp)==0:
                    print(start,"\t",end)
                    try:
                        item_link = get_all_li_tags[start].find("a",href = True)['href']    
                    except:
                        item_link = ""
                    temp_df = pd.DataFrame({'category':[category.find("span","_1QZ6fC _3Lgyp8").text],'sub_category':[get_all_li_tags[start].text],'item':[""],'item_link':["https://www.flipkart.com"+item_link]})
                    df  =df.append(temp_df)
            
df = df.reset_index()
df = df.drop("index",axis=1)
df.to_csv("Flipkart_product_links.csv")



    
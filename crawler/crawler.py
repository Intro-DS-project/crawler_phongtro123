from bs4 import BeautifulSoup 
from lxml import etree 
import requests 
import json
from datetime import datetime

import api

now = datetime.now()

today = now.strftime("%d/%m/%Y")

base_url = "https://phongtro123.com/tinh-thanh/ha-noi?orderby=moi-nhat&page="

header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\
            Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;\
            q=0.9,image/webp,image/apng,*/*;q=0.8"}

def get_dom(web_url):
    webpage = requests.get(web_url, headers=header)
    
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    
    return soup, dom

def merge_dict(dict1, dict2):
    return(dict2.update(dict1))

def delete_markdown(s):
    s = s.replace("```json", "").replace("```", "")
    return s.strip()

if __name__ == "__main__":
    
    list_url_post = []
    
    loop = True
    page = 1
    while loop:
        url = base_url + str(page)
        soup, dom = get_dom(url)
        
        for num in range(1, 21):
            time_post = dom.xpath(f'/html/body/div[1]/main/div[3]/div/section[1]/ul/li[{num}]/div/div[1]/time')[0].get("title")
            today_post = time_post.split()[-1]
            if today_post == today:
                url_post = dom.xpath(f'/html/body/div[1]/main/div[3]/div/section[1]/ul/li[{num}]/div/h3/a')[0].get("href")
                full_url_post = "https://phongtro123.com" + url_post
                
                list_url_post.append(full_url_post)
            else:
                loop = False
                print("Xong!")
                break
        if loop:
            page += 1
        
    print(list_url_post)
    
    for url in list_url_post:
        soup, dom = get_dom(url)
        
        # Get price value
        price_raw = dom.xpath("/html/body/div[1]/main/div/div[2]/article/header/div[2]/div[1]/span")[0].text
        price = 0
        if price_raw.split()[-1].strip() == "triệu/tháng":
            price = float(price_raw.split()[0].strip())

        # Get area value
        area_raw = dom.xpath("/html/body/div[1]/main/div/div[2]/article/header/div[2]/div[2]/span")[0].text
        area = 0
        if area_raw[-1]== "m":
            area = float(area_raw[:-1].strip())
            print(area)
        
        # Get location values
        location_raw = dom.xpath("/html/body/div[1]/main/div/div[2]/article/header/address")[0].text
        location = location_raw.strip('"')
        
        while True:
            try:
                location_extracted = str(api.extract_location(location)).split(",")
                print(location_extracted)
                street, ward, district = location_extracted 
                break
            except Exception as e:
                print("Error!")
                continue
         
        # Get description values
        description_raw = ""
        description_raw_all = soup.find(attrs={"class":"section-content"})
        
        for des in description_raw_all.find_all('p'):
            description_raw += des.text
            description_raw += " "
        description = description_raw.strip()
        while True:
            try:
                description_extracted = str(api.extract_description(description)).split(",")
                print(description_extracted)
                num_bedroom, num_diningroom, num_kitchen, num_toilet, num_floor, current_floor, direction, street_width = description_extracted
                break
            except Exception as e:
                print("Error!")
                continue 
        
        # Combine all the information
        dictionary = {
            "price": price,
            "area": area,
            "location": location,
            "street": street,
            "ward": ward,
            "district": district,
            "post_date": today,
            "url": url,
            "description": description,
            "num_bedroom": num_bedroom,
            "num_diningroom": num_diningroom,
            "num_kitchen": num_kitchen,
            "num_toilet": num_toilet,
            "num_floor": num_floor,
            "current_floor": current_floor,
            "direction": direction,
            "street_width": street_width
        }
        
        # Save to file
        json_object = json.dumps(dictionary, indent=4, ensure_ascii=False)
        with open("output.json", "a", encoding="utf-8") as outfile:
            outfile.write(json_object)
            outfile.write("\n")
        
        
        
        
        
        
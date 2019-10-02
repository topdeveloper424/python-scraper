from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options 
import requests
from bs4 import BeautifulSoup
import json
import time
import platform


class Cook:
    def __init__(self):
        self.url = "https://cookingwithdog.com/recipes/#recipes-isotope+course:"
        self.headers = {'authority':'cookingwithdog.com','accept':'*/*','content-type':'application/x-www-form-urlencoded; charset=UTF-8','sec-fetch-site':'same-origin','sec-fetch-mode':'cors','scheme':'https','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        self.recipe_list = ['beef','beverage','chicken','dessert','egg','fish','hot-pot','main-dish','meat','noodles','pork','rice','rice-bowl','salad','seafood','side-dish','snack','soup','stir-fry','tofu','vegetable']
        self.data = {'action':'wpupg_get_filter_posts','security':'4c17684084','grid':'recipes-isotope'}
        self.chrome_options = Options()
        self.chrome_path = ""
        if "Windows" in platform.system():
            self.chrome_path = "driver/chromedriver.exe"
        else:
            self.chrome_path = "driver/chromedriver"
        self.chrome_options.add_argument("--disable-features=NetworkService")
        self.chrome_options.add_argument('headless')
        prefs = {'profile.managed_default_content_settings.images':2}
        self.chrome_options.add_experimental_option("prefs", prefs)

        
    def scrape(self):
        link_list = []
        for recipe in self.recipe_list:
            cur_url = self.url + recipe
            driver = webdriver.Chrome(self.chrome_path,chrome_options=self.chrome_options)
            driver.get(cur_url)
            try:
                element_present = EC.presence_of_element_located((By.ID,"wpupg-grid-recipes-isotope"))
                WebDriverWait(driver, 20).until(element_present)
                time.sleep(5)
                container = driver.find_element_by_id("wpupg-grid-recipes-isotope")
                a_tags = container.find_elements_by_tag_name("a")
                counter = 0
                for a_tag in a_tags:
                    href = a_tag.get_attribute("href")
                    print(href)
                    link_list.append(href)
                    counter += 1
                print("number : " + str(counter))
            except TimeoutException:
                print("timeout!")
            driver.quit()
        link_list = list(dict.fromkeys(link_list))
        total_json = []
        for link in link_list:
            en_res = self.get_en_details(link)
            ja_res = self.get_ja_details(link)
            json_data = {}
            en_item = {}
            ja_item = {}
            en_item['Source'] = 0
            en_item['From'] = 'null'
            en_item['Value'] = en_res['description']
            ja_item['Source'] = 0
            ja_item['From'] = 'null'
            ja_item['Value'] = ja_res['description']
            item = {}
            item['en'] = en_item
            item['ja'] = ja_item
            json_data['Description'] = item
            
            
            en_item = {}
            ja_item = {}
            en_item['Source'] = 0
            en_item['From'] = 'null'
            en_item['Value'] = en_res['name']
            ja_item['Source'] = 0
            ja_item['From'] = 'null'
            ja_item['Value'] = ja_res['name']
            item = {}
            item['en'] = en_item
            item['ja'] = ja_item
            json_data['Name'] = item
            

            en_item = {}
            ja_item = {}
            en_item['Source'] = 0
            en_item['From'] = 'null'
            en_item['Value'] = en_res['course']
            ja_item['Source'] = 0
            ja_item['From'] = 'null'
            ja_item['Value'] = ja_res['course']
            item = {}
            item['en'] = en_item
            item['ja'] = ja_item
            json_data['Course'] = item


            en_item = {}
            ja_item = {}
            en_item['Source'] = 0
            en_item['From'] = 'null'
            en_item['Value'] = en_res['cuisine']
            ja_item['Source'] = 0
            ja_item['From'] = 'null'
            ja_item['Value'] = ja_res['cuisine']
            item = {}
            item['en'] = en_item
            item['ja'] = ja_item
            json_data['Cuisine'] = item


            
            sections = []

            for i in range(0,len(en_res['Ingredients'])):
                section_item = {}
                try:
                    en_res_item = en_res['Ingredients'][i]
                    ja_res_item = ja_res['Ingredients'][i]
                    section_name = {}
                    en_item = {}
                    ja_item = {}
                    en_item['Source'] = 0
                    en_item['From'] = 'null'
                    en_item['Value'] = en_res_item['SectionName']
                    ja_item['Source'] = 0
                    ja_item['From'] = 'null'
                    ja_item['Value'] = ja_res_item['SectionName']
                    section_name['en'] = en_item
                    section_name['ja'] = ja_item
                    
                    section_item['SectionName'] = section_name
                except Exception:
                    continue
                
                section_list = []
                for j in range(0,len(en_res_item['list'])):
                    try:
                        en_list = en_res_item['list'][j]
                        ja_list = ja_res_item['list'][j]
                        list_item = {}
                        en_item = {}
                        ja_item = {}
                        name_item = {}
                        en_item['Source'] = 0
                        en_item['From'] = 'null'
                        en_item['Value'] = en_list['name']
                        ja_item['Source'] = 0
                        ja_item['From'] = 'null'
                        ja_item['Value'] = ja_list['name']
                        name_item['en'] = en_item
                        name_item['ja'] = ja_item
                        list_item['Name'] = name_item
                        list_item['Amount'] = en_list['amount']
                        list_item['Unit'] = en_list['unit']
                        
                        section_list.append(list_item)
                    except Exception:
                        pass
                    
                section_item['List'] = section_list
                sections.append(section_item)
            json_data['Ingredients'] = sections
            
            steps = []
            for i in range(0,len(en_res['steps'])):
                try:
                    en_res_step = en_res['steps'][i]
                    ja_res_step = ja_res['steps'][i]
                    step_item = {}
                    text_item = {}
                    en_item = {}
                    ja_item = {}
                    en_item['Source'] = 0
                    en_item['From'] = 'null'
                    en_item['Value'] = en_res_step['text']
                    ja_item['Source'] = 0
                    ja_item['From'] = 'null'
                    ja_item['Value'] = ja_res_step['text']
                    text_item['en'] = en_item
                    text_item['ja'] = ja_item
                    step_item['Text'] = text_item
                    step_item['PictureUrl'] = en_res_step['picture']
                    steps.append(step_item)
                except Exception:
                    pass
            json_data['Steps'] = steps
                
            note_item = {}
            en_item = {}
            ja_item = {}
            en_item['Source'] = 0
            en_item['From'] = 'null'
            en_item['Value'] = en_res['notes']
            ja_item['Source'] = 0
            ja_item['From'] = 'null'
            ja_item['Value'] = ja_res['notes']
            note_item['en'] = en_item
            note_item['ja'] = ja_item
            
            json_data['Note'] = note_item
            print(json_data)
            total_json.append(json_data)
        with open('Cook.json', 'w',encoding='utf-16') as outfile:
            temp = json.dumps(total_json,ensure_ascii=False, sort_keys=True, indent=4).encode('utf-16')            
            outfile.write(temp.decode('utf-16'))
                    
            
    def get_en_details(self,link):
        print(link)
        json_data = {}
        source = requests.get(link,headers=self.headers).text
        soup = BeautifulSoup(source,'lxml')
        
        container = soup.find('main',{'id':'main'})
        article = container.find('article',{'class':'recipe'})
        content = article.find('div',{'class':'entry-content'})
        description = content.select_one('p:nth-child(6)').text
        json_data['description'] = description
        cont = content.find('div',{'class':'wpurp-container'})
        
        name_content = cont.select_one('div > div:nth-child(1)')
        name_content = name_content.find('div',{'class':'wpurp-rows'})
        name_rows = name_content.findAll('div',{'class':'wpurp-rows-row'})
        name = name_rows[1].text
        name = name.strip()
        json_data['name'] = name
        
        course_entry = cont.find('div',{'class':'wpurp-recipe-tags-course'})
        course_tds = course_entry.findAll('td')
        course = course_tds[1].text
        course = course.strip()
        json_data['course'] = course
        
        cuisine_entry = cont.find('div',{'class':'wpurp-recipe-tags-cuisine'})
        cui_tds = cuisine_entry.findAll('td')
        cuisine = cui_tds[1].text
        cuisine = cuisine.strip()
        json_data['cuisine'] = cuisine
        
        ingredient_entry = cont.find('div',{'class':'wpurp-recipe-ingredients'})
        json_data['ingredient'] = cuisine
        ingredients_json = []
        groups = ingredient_entry.findAll('div',{'class':'wpurp-recipe-ingredient-group-container'})
        for group in groups:
            section_json = {}
            section_name = ""
            section = group.find('span',{'class':'wpurp-recipe-ingredient-group'})
            if section:
                section_name = section.text
            section_json['SectionName'] = section_name
            section_entry = group.find('ul',{'class':'wpurp-recipe-ingredient-container'})
            section_items = section_entry.findAll('li',{'class':'wpurp-recipe-ingredient'})
            section_list = []
            for section_item in section_items:
                item = {}
                table = section_item.find('table',{'class':'wpurp-columns'})
                item_name = table.find('span',{'class':'wpurp-recipe-ingredient-name'}).text
                item_amount = ''
                amount = table.find('span',{'class':'wpurp-recipe-ingredient-quantity'})
                if amount:
                    item_amount = amount.text
                item_unit = ''
                unit = table.find('span',{'class':'wpurp-recipe-ingredient-unit'})
                if unit:
                    item_unit = unit.text
                item['name'] = item_name
                item['amount'] = item_amount
                item['unit'] = item_unit
                section_list.append(item)
            section_json['list'] = section_list
            if len(section_list) > 0:
                ingredients_json.append(section_json)
        json_data['Ingredients'] = ingredients_json
        
        instruction_entry = cont.find('div',{'class':'wpurp-recipe-instructions'})
        instruction_groups = instruction_entry.findAll('div',{'class':'wpurp-recipe-instruction-group-container'})
        instr_json = []
        for group in instruction_groups:
            instruction_container = group.find('ol',{'class':'wpurp-recipe-instruction-container'})
            instructions = instruction_container.findAll('li',{'class':'wpurp-recipe-instruction'})
            for instruction in instructions:
                instr_item = {}
                inst_text = instruction.find('span',{'class':'wpurp-recipe-instruction-text'}).text
                inst_text = inst_text.strip()
                photo = instruction.find('img',{'class':'wpurp-recipe-instruction-image'})
                picture = ''
                if photo:
                    picture = photo['data-src']
                instr_item['text'] = inst_text
                instr_item['picture'] = picture
                instr_json.append(instr_item)
        json_data['steps'] = instr_json
        notes = cont.find('div',{'class':'wpurp-recipe-notes'}).text
        notes = notes.strip()
        json_data['notes'] = notes

        return json_data

    def get_ja_details(self,link):
        ja_link = link.replace('cookingwithdog.com/','cookingwithdog.com/ja/')
        print(ja_link)
        json_data = {}
        source = requests.get(ja_link,headers=self.headers).text
        soup = BeautifulSoup(source,'lxml')
        
        container = soup.find('main',{'id':'main'})
        article = container.find('article',{'class':'recipe'})
        content = article.find('div',{'class':'entry-content'})
        description = content.select_one('p:nth-child(6)').text
        json_data['description'] = description
        cont = content.find('div',{'class':'wpurp-container'})
        
        name_content = cont.select_one('div > div:nth-child(1)')
        name_content = name_content.find('div',{'class':'wpurp-rows'})
        name_rows = name_content.findAll('div',{'class':'wpurp-rows-row'})
        name = name_rows[1].text
        name = name.strip()
        json_data['name'] = name
        
        course_entry = cont.find('div',{'class':'wpurp-recipe-tags-コース'})
        course_tds = course_entry.findAll('td')
        course = course_tds[1].text
        course = course.strip()
        json_data['course'] = course
        
        cuisine_entry = cont.find('div',{'class':'wpurp-recipe-tags-料理'})
        cui_tds = cuisine_entry.findAll('td')
        cuisine = cui_tds[1].text
        cuisine = cuisine.strip()
        json_data['cuisine'] = cuisine
        
        ingredient_entry = cont.find('div',{'class':'wpurp-recipe-ingredients'})
        ingredients_json = []
        groups = ingredient_entry.findAll('div',{'class':'wpurp-recipe-ingredient-group-container'})
        for group in groups:
            section_json = {}
            section_name = ""
            section = group.find('span',{'class':'wpurp-recipe-ingredient-group'})
            if section:
                section_name = section.text
            section_json['SectionName'] = section_name
            section_entry = group.find('ul',{'class':'wpurp-recipe-ingredient-container'})
            section_items = section_entry.findAll('li',{'class':'wpurp-recipe-ingredient'})
            section_list = []
            for section_item in section_items:
                item = {}
                table = section_item.find('table',{'class':'wpurp-columns'})
                item_name = table.find('span',{'class':'wpurp-recipe-ingredient-name'}).text
                item_amount = ''
                amount = table.find('span',{'class':'wpurp-recipe-ingredient-quantity'})
                if amount:
                    item_amount = amount.text
                item_unit = ''
                unit = table.find('span',{'class':'wpurp-recipe-ingredient-unit'})
                if unit:
                    item_unit = unit.text
                item['name'] = item_name
                item['amount'] = item_amount
                item['unit'] = item_unit
                section_list.append(item)
            section_json['list'] = section_list
            if len(section_list) > 0:
                ingredients_json.append(section_json)
        json_data['Ingredients'] = ingredients_json
        
        instruction_entry = cont.find('div',{'class':'wpurp-recipe-instructions'})
        instruction_groups = instruction_entry.findAll('div',{'class':'wpurp-recipe-instruction-group-container'})
        instr_json = []
        for group in instruction_groups:
            instruction_container = group.find('ol',{'class':'wpurp-recipe-instruction-container'})
            instructions = instruction_container.findAll('li',{'class':'wpurp-recipe-instruction'})
            for instruction in instructions:
                instr_item = {}
                inst_text = instruction.find('span',{'class':'wpurp-recipe-instruction-text'}).text
                inst_text = inst_text.strip()
                photo = instruction.find('img',{'class':'wpurp-recipe-instruction-image'})
                picture = ''
                if photo:
                    picture = photo['data-src']
                instr_item['text'] = inst_text
                instr_item['picture'] = picture
                instr_json.append(instr_item)
        json_data['steps'] = instr_json
        notes = cont.find('div',{'class':'wpurp-recipe-notes'}).text
        notes = notes.strip()
        json_data['notes'] = notes
        return json_data
        
        
def main():
    
    crawler = Cook()
    crawler.scrape()
    
    
if __name__ == "__main__":main()
        
        
        
        

        
        
        
        
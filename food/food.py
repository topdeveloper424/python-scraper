import requests
from bs4 import BeautifulSoup
import json
import csv
import time

class Food:
    def __init__(self):
        self.url = "http://kyoudo-ryouri.com"
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        self.food_links = []
    def scrape(self):
        area_url = self.url + "/area" 
        source = requests.get(area_url,headers=self.headers).text
        soup = BeautifulSoup(source,'lxml')
        link_list = []
        area_container = soup.find('div',{'class':'area-list'})
        areas = area_container.findAll('ul',{'class':'area-list-btn'})
        for area in areas:
            links = area.findAll('a')
            for link in links:
                link_list.append(link['href'])
        for link in link_list:
            self.get_food_links(link)
        
        json_data = []
        for link in self.food_links:
            json_item = {}
            en_res = self.get_details(link,1)
            ja_res = self.get_details(link,0)
            title_json = {}
            en_title = {}
            ja_title = {}
            en_title['Source'] = 0
            en_title['From'] = 'null'
            en_title['Value'] = en_res['title']
            
            ja_title['Source'] = 0
            ja_title['From'] = 'null'
            ja_title['Value'] = ja_res['title']
            title_json['en'] = en_title
            title_json['ja'] = ja_title
            json_item['title'] = title_json
            
            des_json = {}
            en_title = {}
            ja_title = {}
            en_title['Source'] = 0
            en_title['From'] = 'null'
            en_title['Value'] = en_res['description']
            
            ja_title['Source'] = 0
            ja_title['From'] = 'null'
            ja_title['Value'] = ja_res['description']
            des_json['en'] = en_title
            des_json['ja'] = ja_title
            json_item['title'] = des_json
            
            photo_json = {}
            en_title = {}
            ja_title = {}
            en_title['Source'] = 0
            en_title['From'] = 'null'
            en_title['Value'] = en_res['photo']
            
            ja_title['Source'] = 0
            ja_title['From'] = 'null'
            ja_title['Value'] = ja_res['photo']
            photo_json['en'] = en_title
            photo_json['ja'] = ja_title
            json_item['title'] = photo_json
            
            mat_list = []
            for i in range(0,len(en_res['material'])):
                en_mat = en_res['material'][i]
                ja_mat = ja_res['material'][i]
                
                mat_json = {}
                en_title = {}
                ja_title = {}
                en_title['Source'] = 0
                en_title['From'] = 'null'
                en_title['Value'] = en_mat
                
                ja_title['Source'] = 0
                ja_title['From'] = 'null'
                ja_title['Value'] = ja_mat
                mat_json['en'] = en_title
                mat_json['ja'] = ja_title
                mat_list.append(mat_json)
            json_item['Materials'] = mat_list
            
            pro_list = []
            for i in range(0,len(en_res['procedure'])):
                en_pro = en_res['procedure'][i]
                ja_pro = ja_res['procedure'][i]
                
                pro_json = {}
                en_title = {}
                ja_title = {}
                en_title['Source'] = 0
                en_title['From'] = 'null'
                en_title['Value'] = en_pro
                
                ja_title['Source'] = 0
                ja_title['From'] = 'null'
                ja_title['Value'] = ja_pro
                pro_json['en'] = en_title
                pro_json['ja'] = ja_title
                pro_list.append(pro_json)
            json_item['Procedure'] = pro_list
            json_data.append(json_item)
            
        with open('Food.json', 'w',encoding='utf-16') as outfile:
            temp = json.dumps(json_data,ensure_ascii=False, sort_keys=True, indent=4).encode('utf-16')            
            outfile.write(temp.decode('utf-16'))
            
    def get_food_links(self,link):
        cur_url = self.url + link
        print(cur_url)
        source = requests.get(cur_url,headers=self.headers).text
        soup = BeautifulSoup(source,'lxml')
        container = soup.find('ul',{'id':'js-food-list'})
        foods = container.findAll('figure',{'class':'food-photo'})
        for food in foods:
            food_link = food.find('a')['href']
            self.food_links.append(food_link)
        all_a_tag = soup.find('a',{'id':'js-all-list'})
        if all_a_tag:
            ids = all_a_tag['data-entry-ids']
            id_list = ids.split(",")
            taxonomy = all_a_tag['data-entry-taxonomy']
            term = all_a_tag['data-entry-term']
            data = {'action':'food_list','term':term,'taxonomy':taxonomy,'ids':ids,'offset':len(id_list)}
            sub_source = requests.post('http://kyoudo-ryouri.com/wp-admin/admin-ajax.php',data=data,headers=self.headers).text
            add_json = json.loads(sub_source)
            for add_food in add_json:
                print(add_food['url'])
                self.food_links.append(add_food['url'])
        
    def get_details(self,link,mode):
        cur_link = link
        if mode == 1:
            cur_link = cur_link.replace("http://kyoudo-ryouri.com/","http://kyoudo-ryouri.com/en/")
        source = requests.get(cur_link,headers=self.headers).text
        soup = BeautifulSoup(source,'lxml')
        json_data = {}
        article = soup.find('article')
        header = article.find('header',{'class':'food-kv'})
        title = header.find('h1').text
        title = title.strip()
        description = header.find('p',{'class':'desc'}).text
        thumb = header.find('div',{'class':'thumb'})
        photo = thumb.find('img')['src']
        json_data['title'] = title
        json_data['description'] = description
        json_data['photo'] = photo
        
        recipe = article.find('section',{'class':'recipe'})
        
        headline = recipe.find('div',{'class':'headline'})
        persons = ''
        if headline:
            try:
                persons = headline.find('p').text
                persons = persons.strip()
            except Exception:
                pass
        
        json_data['persons'] = persons
        
        material = recipe.find('div',{'class':'material'})
        mat_list = []
        if material:
            lis = material.findAll('li')
            for li in lis:
                mat_item = {}
                name = li.find('span',{'class':'name'}).text
                quantity = li.find('span',{'class':'quantity'}).text
                mat_item['name'] = name
                mat_item['quantity'] = quantity
                mat_list.append(mat_item)
        
        json_data['material'] = mat_list
        
        procedure = recipe.find('dl',{'class':'procedure'})
        procedure_list = []
        if procedure:
            dds = procedure.findAll('dd')
            for dd in dds:
                content = dd.text
                content = content.strip()
                procedure_list.append(content)
        json_data['procedure'] = procedure_list
        
        offer = recipe.find('p',{'class':'offer'}).text
        offer = offer.strip()
        json_data['offer'] = offer
            
        return json_data
        
        
def main():
    crawler = Food()
    crawler.scrape()
    
if __name__ == "__main__":main()

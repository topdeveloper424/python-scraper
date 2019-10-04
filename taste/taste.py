import requests
from bs4 import BeautifulSoup
import json
import time

class Taste:
    def __init__(self):
        self.detail_url = "https://www.tasteofjapan.jp/api/JP/?r="
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',}
    def scrape(self):
        url = "https://www.tasteofjapan.jp/recipes/search/?video=0&meal=&dish=&ingredient=&season=&q=&page="
        flag = False
        page = 1
        link_list = []
        while flag == False:
            cur_url = url +""+ str(page)
            print(cur_url)
            source = requests.get(cur_url,headers=self.headers).text
            soup = BeautifulSoup(source, 'lxml')
            container = soup.find('div',{'class':'detaillist-block'})
            items = container.findAll('div',{'class':'has-grid-item'})
            if len(items) == 0:
                flag = True
            for item in items:
                a_tag = item.find('a',{'class':'item-block'})
                link = a_tag['href']
                link_list.append(link)
            page += 1
        json_data = []
        for link in link_list:
            res_json = self.get_details(link)
            json_data.append(res_json)
        with open('Taste.json', 'w',encoding='utf-16') as outfile:
            temp = json.dumps(json_data,ensure_ascii=False, sort_keys=True, indent=4).encode('utf-16')            
            outfile.write(temp.decode('utf-16'))
    
    def remove_space(self,input_str):
        temp = input_str.strip()
        temp = temp.replace("&nbsp;","")
        
        return temp

    def get_details(self,link):
        print(link)
        json_data = {}
        
        en_url = "https://www.tasteofjapan.jp/api/EN/?r="+link
        ja_url = "https://www.tasteofjapan.jp/api/JP/?r="+link
        cn_url = "https://www.tasteofjapan.jp/api/CH/?r="+link
        
        en_source = requests.get(en_url,headers=self.headers).text
        en_soup = BeautifulSoup(en_source, 'lxml')
        ja_source = requests.get(ja_url,headers=self.headers).text
        ja_soup = BeautifulSoup(ja_source, 'lxml')
        cn_source = requests.get(cn_url,headers=self.headers).text
        cn_soup = BeautifulSoup(cn_source, 'lxml')
        
        en_container = en_soup.find('div',{'class':'content-mainblock'})
        en_title = en_container.find('h3',{'class':'page-title-sub'}).text
        en_title = en_title.strip()
        en_head = en_container.find('div',{'class':'has-flex-pc2colandsp1col'})
        en_description = en_head.find('div',{'class':'item-info'}).text
        en_description = en_description.strip()
        en_ingredient = en_container.find('div',{'class':'content-ingredients'})
        en_detail = en_ingredient.find('div',{'class':'item-detail'})
        en_content = en_detail.decode_contents(formatter="html")

        en_ingre_array = en_content.split('<br/>')
        
        for ingre in en_ingre_array:
            if ingre.find('<strong>') != -1:
                en_ingre_array.remove(ingre)

        en_step = en_container.find('div',{'class':'sequential-item-list'})
        en_ul = en_step.find('ul',{'class':'item-detail'})
        en_steps = en_ul.findAll('li',{'class':'item-list'})
        en_step_list = []
        for step in en_steps:
            [s.extract() for s in step('span')]
            step_item = step.text
            step_item = step_item.strip()
            en_step_list.append(step_item)
        


        ja_container = ja_soup.find('div',{'class':'content-mainblock'})
        ja_title = ja_container.find('h3',{'class':'page-title-sub'}).text
        ja_title = ja_title.strip()
        ja_head = ja_container.find('div',{'class':'has-flex-pc2colandsp1col'})
        ja_description = ja_head.find('div',{'class':'item-info'}).text
        ja_description = ja_description.strip()
        ja_ingredient = ja_container.find('div',{'class':'content-ingredients'})
        ja_detail = ja_ingredient.find('div',{'class':'item-detail'})
        ja_content = ja_detail.decode_contents(formatter="html")

        ja_ingre_array = ja_content.split('<br/>')
        ja_step = ja_container.find('div',{'class':'sequential-item-list'})
        ja_ul = ja_step.find('ul',{'class':'item-detail'})
        ja_steps = ja_ul.findAll('li',{'class':'item-list'})
        ja_step_list = []
        for step in ja_steps:
            [s.extract() for s in step('span')]
            step_item = step.text
            step_item = step_item.strip()
            ja_step_list.append(step_item)
        


        cn_container = cn_soup.find('div',{'class':'content-mainblock'})
        cn_title = cn_container.find('h3',{'class':'page-title-sub'}).text
        cn_title = cn_title.strip()
        cn_head = cn_container.find('div',{'class':'has-flex-pc2colandsp1col'})
        cn_description = cn_head.find('div',{'class':'item-info'}).text
        cn_description = cn_description.strip()
        cn_ingredient = cn_container.find('div',{'class':'content-ingredients'})
        cn_detail = cn_ingredient.find('div',{'class':'item-detail'})
        cn_content = cn_detail.decode_contents(formatter="html")

        cn_ingre_array = cn_content.split('<br/>')

        cn_step = cn_container.find('div',{'class':'sequential-item-list'})
        cn_ul = cn_step.find('ul',{'class':'item-detail'})
        cn_steps = cn_ul.findAll('li',{'class':'item-list'})
        cn_step_list = []
        for step in cn_steps:
            [s.extract() for s in step('span')]
            step_item = step.text
            step_item = step_item.strip()
            cn_step_list.append(step_item)
        
        title_json = {}
        en_json = {}
        ja_json = {}
        cn_json = {}
        en_json['Source'] = 0
        en_json['From'] = 'null'
        en_json['Value'] = en_title
        ja_json['Source'] = 0
        ja_json['From'] = 'null'
        ja_json['Value'] = ja_title
        cn_json['Source'] = 0
        cn_json['From'] = 'null'
        cn_json['Value'] = cn_title
        title_json['en'] = en_json
        title_json['ja'] = ja_json
        title_json['cn'] = cn_json
        json_data['Title'] = title_json
        

        des_json = {}
        en_json = {}
        ja_json = {}
        cn_json = {}
        en_json['Source'] = 0
        en_json['From'] = 'null'
        en_json['Value'] = en_description
        ja_json['Source'] = 0
        ja_json['From'] = 'null'
        ja_json['Value'] = ja_description
        cn_json['Source'] = 0
        cn_json['From'] = 'null'
        cn_json['Value'] = cn_description
        des_json['en'] = en_json
        des_json['ja'] = ja_json
        des_json['cn'] = cn_json
        json_data['Description'] = des_json

        des_json = {}
        en_json = {}
        ja_json = {}
        cn_json = {}
        en_json['Source'] = 0
        en_json['From'] = 'null'
        en_json['Value'] = en_description
        ja_json['Source'] = 0
        ja_json['From'] = 'null'
        ja_json['Value'] = ja_description
        cn_json['Source'] = 0
        cn_json['From'] = 'null'
        cn_json['Value'] = cn_description
        des_json['en'] = en_json
        des_json['ja'] = ja_json
        des_json['cn'] = cn_json
        json_data['Description'] = des_json
        
        
        ingre_json = []
        for i in range(0,len(en_ingre_array)):
            try:
                ingre_item = {}
                en_igre = en_ingre_array[i]
                ja_igre = ja_ingre_array[i]
                cn_igre = cn_ingre_array[i]
                
                en_igre = self.remove_space(en_igre)
                if en_igre == "":
                    continue
                ja_igre = self.remove_space(ja_igre)
                cn_igre = self.remove_space(cn_igre)
                
                ingre_item['en'] = en_igre
                ingre_item['ja'] = ja_igre
                ingre_item['cn'] = cn_igre
                
                ingre_json.append(ingre_item)
            except Exception:
                print(en_igre)
                break
            
        json_data['Ingredients'] = ingre_item
        
        step_json = []
        for i in range(0,len(en_step_list)):
            step_item = {}
            en_step = en_step_list[i]
            ja_step = ja_step_list[i]
            cn_step = cn_step_list[i]
            
            en_step = en_step.strip()
            ja_step = ja_step.strip()
            cn_step = cn_step.strip()
            step_item['en'] = en_step
            step_item['ja'] = ja_step
            step_item['cn'] = cn_step
            
            step_json.append(step_item)
        json_data['Steps'] = step_json
        print(json_data)
        
        return json_data
            
            
def main():
    crawler = Taste()
    crawler.scrape()
    
if __name__ == "__main__":main()

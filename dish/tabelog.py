import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import os

class Tabelog:
    def __init__(self):
        self.url = "https://tabelog.com/tokyo/rstLst/{}/"
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        
    def scrape(self):
        page_count = 0
        flag = True
        
        with open("temp.csv","w",newline='',encoding='utf-16') as fout:
            out = csv.writer(fout, delimiter=",", quoting=csv.QUOTE_ALL) 
            
            while flag == True:
                page_count += 1
                print("page number : " + str(page_count))
                cur_url = self.url.format(page_count)
                link_list = []
                source = requests.get(cur_url,headers=self.headers).text
                soup = BeautifulSoup(source,'lxml')
                container = soup.find('ul',{'class':'js-rstlist-info'})
                
                if container:
                    stores = container.findAll('li',{'class':'list-rst'})

                    for store in stores:
                        content = store.find('div',{'class':'list-rst__wrap'})
                        link = content.find('a',{'class':'list-rst__rst-name-target'})['href']
                        link_list.append(link)
                        print(link)

                    for sub_url in link_list:
                        self.get_details(sub_url,out)
                else:
                    flag = False
                
    def get_details(self,link,out):
        en_url = link.replace("tabelog.com/tokyo","tabelog.com/en/tokyo")
        cn_url = link.replace("tabelog.com/tokyo","tabelog.com/cn/tokyo")
        tw_url = link.replace("tabelog.com/tokyo","tabelog.com/tw/tokyo")
        kr_url = link.replace("tabelog.com/tokyo","tabelog.com/kr/tokyo")

        en_source = requests.get(en_url,headers=self.headers).text
        source = requests.get(link,headers=self.headers).text
        cn_source = requests.get(cn_url,headers=self.headers).text
        tw_source = requests.get(tw_url,headers=self.headers).text
        kr_source = requests.get(kr_url,headers=self.headers).text
        
        soup = BeautifulSoup(source,'lxml')
        en_soup = BeautifulSoup(en_source,'lxml')
        cn_soup = BeautifulSoup(cn_source,'lxml')
        tw_soup = BeautifulSoup(tw_source,'lxml')
        kr_soup = BeautifulSoup(kr_source,'lxml')
        
        content = soup.find('div',{'class':'rstinfo-table'})
        en_content = en_soup.find('section',{'id':'anchor-rd-detail'})
        cn_content = cn_soup.find('section',{'id':'anchor-rd-detail'})
        tw_content = tw_soup.find('section',{'id':'anchor-rd-detail'})
        kr_content = kr_soup.find('section',{'id':'anchor-rd-detail'})

        sections = content.findAll('table',{'class':'rstinfo-table__table'})
        en_sections = en_content.findAll('section')
        cn_sections = cn_content.findAll('section')
        tw_sections = tw_content.findAll('section')
        kr_sections = kr_content.findAll('section')

        section_len = len(sections)
        json_list = {}
        for section_count in range(0,section_len):
            table = sections[section_count]
            en_table = en_sections[section_count].find('table',{'class':'rd-detail-info'})
            cn_table = cn_sections[section_count].find('table',{'class':'rd-detail-info'})
            tw_table = tw_sections[section_count].find('table',{'class':'rd-detail-info'})
            kr_table = kr_sections[section_count].find('table',{'class':'rd-detail-info'})

            trs = table.findAll('tr')
            en_trs = en_table.findAll('tr')
            cn_trs = cn_table.findAll('tr')
            tw_trs = tw_table.findAll('tr')
            kr_trs = kr_table.findAll('tr')
            tr_len = len(en_trs)
            count = 0
            try:
                for tr_count in range(0,tr_len):
                    en_th_name = en_trs[tr_count].find('th').text
                    en_th_name = en_th_name.strip()
                    if en_th_name == "TEL/reservation":
                        count = count + 1
                    
                    td_content = trs[count].find('td').text
                    td_content = td_content.strip()

                    en_td_content = en_trs[tr_count].find('td').text
                    en_td_content = en_td_content.strip()

                    cn_td_content = cn_trs[tr_count].find('td').text
                    cn_td_content = cn_td_content.strip()

                    tw_td_content = tw_trs[tr_count].find('td').text
                    tw_td_content = tw_td_content.strip()

                    kr_td_content = kr_trs[tr_count].find('td').text
                    kr_td_content = kr_td_content.strip()
                    
                    en_item = {}
                    en_item['Source'] = 0
                    en_item['From'] = 'null'
                    en_item['Value'] = en_td_content
                    
                    item = {}
                    item['Source'] = 0
                    item['From'] = 'null'
                    item['Value'] = td_content
                    
                    cn_item = {}
                    cn_item['Source'] = 0
                    cn_item['From'] = 'null'
                    cn_item['Value'] = cn_td_content
                    
                    tw_item = {}
                    tw_item['Source'] = 0
                    tw_item['From'] = 'null'
                    tw_item['Value'] = tw_td_content
                    
                    kr_item = {}
                    kr_item['Source'] = 0
                    kr_item['From'] = 'null'
                    kr_item['Value'] = kr_td_content
                    
                    json_data = {}
                    json_data['en'] = en_item
                    json_data['ja'] = item
                    json_data['cn'] = cn_item
                    json_data['tw'] = tw_item
                    json_data['kr'] = kr_item

                    json_list[en_th_name] = json_data
                    count += 1
            except Exception:
                pass
        temp = json.dumps(json_list,ensure_ascii=False).encode('utf-16')
        out.writerow([temp.decode('utf-16')])
    def parse_json(self):
        with open('temp.csv',"r",encoding='utf-16') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            json_list = []
            
            for csv_row in csv_reader:
                json_item = csv_row[0]
                json_parsed = json.loads(json_item)
                json_list.append(json_parsed)                
                
            with open('tabelog.json', 'w',encoding='utf-16') as outfile:
                temp = json.dumps(json_list,ensure_ascii=False, sort_keys=True, indent=4).encode('utf-16')            
                # content = unicode(temp)
                outfile.write(temp.decode('utf-16'))
                   
def main():
    crawler = Tabelog()
    crawler.scrape()
    time.sleep(1)
    crawler.parse_json()
    if os.path.exists("temp.csv"):
        os.remove("temp.csv")    
    
if __name__ == "__main__":main()
        
        


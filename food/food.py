import requests
from bs4 import BeautifulSoup
import json
import csv
import time

class Food:
    def __init__(self):
        self.url = "http://kyoudo-ryouri.com"
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
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
            self.get_details(link)
            
    def get_details(self,link):
        cur_url = self.url + link
        pass
        
        
                
            
        
def main():
    crawler = Food()
    crawler.scrape()
    
if __name__ == "__main__":main()

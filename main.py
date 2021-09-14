import asyncio
import requests
from bs4 import BeautifulSoup
import lxml
from aiohttp import ClientSession
from multiprocessing.pool import ThreadPool

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}
url = 'https://www.stepstone.de'
url1 ='https://www.stepstone.de/5/job-search-simple.html?ke=produktmanager&se=21000'
async def main(main_link):
    async with ClientSession(headers=headers) as session:
        async with session.get(main_link) as response:
            page_content = await response.text()
            with open('test.html','w') as f:
                f.write(page_content)
            launch_soup = BeautifulSoup(page_content,'lxml')
            count = int(launch_soup.find(class_='at-facet-header-total-results').text)
            if count/25-count//25 > 0: 
                count =count//25+1
            else:
                count = count//25
            for i in range(1,count):
                print(i)
                async with session.get(url1+f'&page={i}',headers=headers) as local_page:
                    local_page = await local_page.text()
                    local_soup = BeautifulSoup(local_page,'lxml')
                    all_links = local_soup.find_all(class_ = 'sc-fzoiQi eRNcm',href=True)
                    for link in all_links:
                        link = url+str(link)[58:str(link).find('.html')+5]
                        print(link)
                        async with session.get(link,headers=headers) as work_page:
                            work_page = await work_page.text()
                            work_soup = BeautifulSoup(work_page,'lxml')
                            with open(f'test{i}.html','w',encoding='utf-8') as f:
                                f.write(work_page)
                            company_name = work_soup.find(class_='at-listing-nav-company-name-link at-header-company-name sc-jWBwVP ddpySo sc-cvbbAY fbKzzw').text
                            work_name = work_soup.find(class_='listing__job-title at-header-company-jobTitle sc-brqgnP bFVWpz').text
                            close_to_location = list(work_soup.find(class_='sc-kgoBCf dtbzVv sc-chPdSV eQgpKY')).split('li')
                            for string in close_to_location:
                                if string.find('location'):
                                    print(string)
loop = asyncio.get_event_loop()
if __name__ == '__main__':
    loop.run_until_complete(main(url1))
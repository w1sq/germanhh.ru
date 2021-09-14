import time
from time import sleep
import csv
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

global browser
url = 'https://www.stepstone.de'
links = ['https://www.stepstone.de/5/ergebnisliste.html?ke=product%20manager&suid=bd1c1f93-141b-4aa5-9003-f123a65c15fa&action=facet_selected%3Bsectors%3B21000&se=21000',
'https://www.stepstone.de/5/ergebnisliste.html?ke=produktmanager&suid=dfd7e1b9-54f9-4187-b43d-97abf4677f61&action=facet_selected%3Bsectors%3B21000&se=21000',
'https://www.stepstone.de/5/ergebnisliste.html?ke=Product%20Owner%2Fin&whattype=autosuggest&suid=1633092f-61ca-400b-bb76-fb6d2e214c83&action=facet_selected%3Bsectors%3B21000&se=21000'
    ]
os.remove('first.csv')
os.remove('second.csv')
os.remove('third.csv')
def main(main_link,id=0,job_id=0):
    global browser
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4147.125 Safari/537.36")
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver')
    browser.implicitly_wait(5)
    browser.maximize_window()
    browser.get(main_link)
    try:
        button = browser.find_element_by_xpath('//*[@id="ccmgt_explicit_accept"]')
        button.click()
    except Exception:
        pass
    count = browser.find_element_by_class_name("at-facet-header-total-results").text
    if '.' in count:
        count = count.replace('.','')
    count = int(count)
    if count/25-count//25 > 0: 
        count =count//25+1
    else:
        count = count//25
    with open('first.csv','a',encoding='utf-8',newline='') as first:
        with open('second.csv','a',encoding='utf-8',newline='') as second:
            with open('third.csv','a',encoding='utf-8',newline='') as third:
                fieldnames1 = ['id', 'job','city','company','description']
                fieldnames2 = ['id','job_id','task']
                fieldnames3 = ['id','job_id','profile']
                writer1 = csv.DictWriter(first, fieldnames=fieldnames1)
                writer2 = csv.DictWriter(second, fieldnames=fieldnames2)
                writer3 = csv.DictWriter(third, fieldnames=fieldnames3)
                id = id
                job_id = job_id
                for page in range(1,count):
                    browser.get(main_link+f'&page={page}')
                    all_blocks = browser.find_elements_by_class_name("sc-fzoiQi.eRNcm")
                    all_locations = list(map(lambda x: x.text,browser.find_elements_by_class_name('sc-fznzOf.gmOWPW')))
                    all_companies = list(map(lambda x: x.text,browser.find_elements_by_class_name('sc-AxheI.cOZDZM')))
                    all_jobs = list(map(lambda x: x.text,browser.find_elements_by_class_name('sc-fzqARJ.iyolKq')))
                    all_links = list(map(lambda x: x.get_attribute('href'),all_blocks))
                    for i,link in enumerate(all_links):
                        browser.get(link)
                        #company = browser.find_element_by_class_name('at-listing-nav-company-name-link at-header-company-name sc-jWBwVP ddpySo sc-cvbbAY fbKzzw').text
                        try:
                            description = browser.find_element_by_class_name('at-section-text-introduction-content.listingContentBrandingColor.sc-lhVmIH.cjyXx').text
                        except Exception:
                            description =''
                            print('no_descr',link)
                        try:
                            profile = browser.find_elements_by_class_name('at-section-text-profile-content.listingContentBrandingColor.sc-lhVmIH.kiChPJ')[0].text
                        except Exception:
                            profile = ''
                            print('no_prof',link)
                        try:
                            tasks = browser.find_elements_by_class_name('at-section-text-description-content.listingContentBrandingColor.sc-lhVmIH.kiChPJ')[0].text
                        except Exception:
                            tasks=''
                            print('no_task',link)
                        writer1.writerow({'id': id, 'job': all_jobs[i],'city':all_locations[i],'company':all_companies[i],'description':description})
                        for task in tasks.split('\n'):
                            if task.split() != '':
                                writer2.writerow({'id': id, 'job_id': job_id,'task':task})
                        for skill in profile.split('\n'):
                            if skill.split() != '':
                                writer3.writerow({'id': id, 'job_id': job_id,'profile':skill})
                        id += 1
                        job_id += 1
    return id,job_id



if __name__ == "__main__":
    # input("Нажмите Enter для старта")
    # print("Нажмите CTRL + C для завершения работы")
    id = 0
    job_id = 0
    for link in links:
        id,job_id = main(main_link=link,id=id,job_id=job_id)
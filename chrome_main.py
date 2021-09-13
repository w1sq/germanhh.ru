from time import sleep
import csv
from shutil import copyfile
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

url = 'https://www.stepstone.de'
links = ['https://www.stepstone.de/5/ergebnisliste.html?ke=Product%20Owner%2Fin&whattype=autosuggest&suid=1633092f-61ca-400b-bb76-fb6d2e214c83&action=facet_selected%3Bsectors%3B21000&se=21000',
'https://www.stepstone.de/5/ergebnisliste.html?ke=product%20manager&suid=bd1c1f93-141b-4aa5-9003-f123a65c15fa&action=facet_selected%3Bsectors%3B21000&se=21000',
'https://www.stepstone.de/5/ergebnisliste.html?ke=produktmanager&suid=dfd7e1b9-54f9-4187-b43d-97abf4677f61&action=facet_selected%3Bsectors%3B21000&se=21000'
    ]

chrome_options = Options()
chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4147.125 Safari/537.36")
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--headless")
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
browser = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)
browser.implicitly_wait(5)

fieldnames1 = ['id', 'job','city','company','description']
fieldnames2 = ['id','task']
fieldnames3 = ['id','profile']

def process_page(link,i,id,all_locations,all_companies,all_jobs,writer1,writer2,writer3):
    browser.get(link)
    button = browser.find_elements_by_css_selector('.at-exit-intent-modal-button')
    if button:
        button[0].click() 
    description = browser.find_elements_by_css_selector(".at-section-text-introduction-content")
    tasks = browser.find_elements_by_css_selector('.at-section-text-description-content')
    profile = browser.find_elements_by_css_selector('.at-section-text-profile-content')
    if not description:     
        description =''
        print('no_descr',link)
    else:
        description = description[0].text
    if not profile:
        profile =''
        print('no_prof',link)
    else:
        profile = profile[0].text
    if not tasks:
        tasks =''
        print('no_tasks',link)
    else:
        tasks = tasks[0].text

    writer1.writerow({'id': id, 'job': all_jobs[i],'city':all_locations[i],'company':all_companies[i],'description':description})
    for task in tasks.split('\n'):
        if task.strip() != '':
            writer2.writerow({'id': id,'task':task})
    for skill in profile.split('\n'):
        if skill.strip() != '':
            writer3.writerow({'id': id,'profile':skill})

def process_blocks(link):
    browser.get(link)
    all_locations = list(map(lambda x:x.text,browser.find_elements_by_xpath('//article[@data-at="job-item"]//li[@data-at="job-item-location"]')))
    all_companies = list(map(lambda x:x.text,browser.find_elements_by_xpath('//article[@data-at="job-item"]//div[@data-at="job-item-company-name"]')))
    all_jobs = browser.find_elements_by_xpath('//article[@data-at="job-item"]//a[@data-at="job-item-title"]')
    all_jobs_names = list(map(lambda x:x.text,all_jobs))
    all_links = list(map(lambda x:x.get_attribute('href'),all_jobs))
    return all_locations,all_companies,all_jobs_names,all_links

def main(main_link,id=0):
    browser.get(main_link)
    print(browser.page_source)
    button = browser.find_elements_by_xpath('//*[@id="ccmgt_explicit_accept"]')
    if button:
        button[0].click()
    # count = browser.find_element_by_css_selector(".at-facet-header-total-results").text
    # print(count)
    # if '.' in count:
    #     count = count.replace('.','')
    # count = int(count)
    # if count/25-count//25 > 0:
    #     count =count//25+1
    # else:
    #     count = count//25
    id = id
    page = 1
    while browser.find_element_by_xpath('//a[@data-at="pagination-next"]').get_attribute('href'):
        blocks_link = main_link+f'&page={page}'
        all_locations,all_companies,all_jobs,all_links = process_blocks(blocks_link)
        for i,link in enumerate(all_links):
            process_page(link,i,id,all_locations,all_companies,all_jobs,writer1,writer2,writer3)
            id += 1
        page += 1
    return id

if __name__ == "__main__":
    print('Script_has started')
    while True:
        first = open('./first.csv','w',encoding='utf-8',newline='')
        second = open('./second.csv','w',encoding='utf-8',newline='')
        third = open('./third.csv','w',encoding='utf-8',newline='')
        writer1 = csv.DictWriter(first, fieldnames=fieldnames1, delimiter=';')
        writer2 = csv.DictWriter(second, fieldnames=fieldnames2, delimiter=';')
        writer3 = csv.DictWriter(third, fieldnames=fieldnames3, delimiter=';')
        id = 0
        for link in links:
            id = main(main_link=link,id=id)
        first.close()
        second.close()
        third.close()
        copyfile('./first.csv','ready_files/first.csv')
        copyfile('./second.csv','ready_files/second.csv')
        copyfile('./third.csv','ready_files/third.csv')
        sleep(20*3600)

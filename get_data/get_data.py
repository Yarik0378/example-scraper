import time
from bs4 import BeautifulSoup
import csv
from api.proxy_auth_data import login, password
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument('lang=en')
# options.add_argument('--proxy-server=181.177.87.144:9234')
# options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--lang=en') <- Tried this option as well

# proxy_options = {
#     'proxy': {
#         'https': f'http://{login}:{password}@181.177.87.144:9234'
#     }
# }

driver = webdriver.Chrome(chrome_options=options)
wait = WebDriverWait(driver, 3)

current = 3  # the file number from which the function is allowed to run
file_number = 1  # the file number from which the function starts


def write_last_data(currents, last_file_number):
    with open('last_data/current.txt', 'a', encoding="utf-8") as file:
        file.write(str(currents) + '\r\n')
    with open('last_data/last_file_number.txt', 'a', encoding="utf-8") as file:
        file.write(str(last_file_number) + '\r\n')


def web_driver(screen_name_link):
    url = f"https://twitter.com/{screen_name_link}"
    driver.get(url)


def check_next_file(current):
    try:
        open(f'csv_api/csv_{current}.csv')
        return True
    except IOError as e:
        print('File could not be opened')
        return False


def write_csv(data):
    with open('good_data.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow((data['name'],
                         data['screen_name'],
                         data['description'],
                         data['followers'],
                         data['following'],
                         data['created_at'],
                         data['link_last_tweet'],
                         data['date_published_tweet']
                         ))


def get_inf(file_number):
    with open(f'csv_api/csv_{file_number}.csv', 'r', encoding='UTF8') as file:
        headers = ["name", "screen_name", "description", "followers_count",
                   'friends_count', "listed_count", "favourites_count", "created_at"]
        reader = csv.DictReader(file, fieldnames=headers)
        for item in reader:
            screen_name = item['screen_name'].replace('\n', '')
            web_driver(screen_name_link=screen_name)
            add_inf = scrap_data(item['screen_name'])

            data = {
                'name': item['name'],
                'screen_name': item['screen_name'],
                'description': item['description'],
                'followers': item['followers_count'],
                'following': item['friends_count'],
                'created_at': item['created_at'],
                'link_last_tweet': add_inf['link_last_tweet'],
                'date_published_tweet': add_inf['date_published_tweet'],
            }
            write_csv(data)
        return f'csv_{file_number}'


def scrap_data(screen_name):
    try:
        wait.until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "div[class='css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu']")))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        date_add = soup.select_one('a[dir=auto][role=link]>time').get('datetime')
        link = soup.select_one("div[class='css-1dbjc4n r-1d09ksm r-18u37iz r-1wbh5a2']").find_all('a')[1].get('href')
        if date_add is None:
            date_add = ''
            link = ''
        else:
            date_add.replace('T', ' ').replace('Z', ' ')
            link = f'https://twitter.com{link}'

        data = {
            'link_last_tweet': link,
            'date_published_tweet': date_add
        }
        return data
    except:
        print(f'No tweet: account : {screen_name}')
        data = {
            'link_last_tweet': '',
            'date_published_tweet': ''
        }
        return data


def return_to_work(value):
    global currents, file_numbers
    try:
        if value == 'file_number':
            file_name = 'last_file_number'
        else:
            file_name = 'current'
        for i in range(1, 20):
            with open(f'last_data/{file_name}.txt', encoding='utf-8') as f_read:
                last_line = f_read.readlines()[-i]
                cleaned_line = last_line.strip()
            if cleaned_line:
                return int(cleaned_line)
    except:
        print(f'No recent entries : {value}')
        if value == 'file_number':
            return 1
        else:
            return 3


def pars_twit():
    print('PARSING CSVs')
    global current, file_number
    current = return_to_work("current")
    file_number = return_to_work("file_number")
    while True:
        access = check_next_file(current)
        if access is True:
            print(f"I'm working on cvs_{file_number}")
            get_inf(file_number)
            current += 1
            file_number += 1
            write_last_data(current, file_number)
        elif access is False:
            time.sleep(60)

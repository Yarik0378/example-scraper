import time
import csv
import requests

# consumer_key = '6UftcdxVGgkNPJ2Org9t0ZbUX'
#
# consumer_secret = 'XayrAwHSx7nXKlyZDzpByCXbdd3CejnR1DuzxLAymlbe6nKmcu'
#
# access_token = '1325791799689011201-MmkyA5dXLWlLqnTu5YrmumWL5DGpsL'
#
# access_token_secret = 'k28uWqgocgzLoiJRcRFlnLYDmJpGvbSyFobdOxMy9ZZEY'
#
# # authorization of consumer key and consumer secret
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#
# # set access to user's access key and access secret
# auth.set_access_token(access_token, access_token_secret)
#
# # calling the api
#
# api = tweepy.API(auth)
# the screen_name of the targeted user
# screen_name = "path"
last_dirty_file = 1
new_str = 0
headers = {"Authorization": 'Bearer AAAAAAAAAAAAAAAAAAAAAC99NgEAAAAAEj6PoEyQGFqkQ2B4ItGaERYM1xE%3DPDULU6C'
                            'x73TCP3Pm9M420nrNQEbM1brpid1dAOut6rcViVxD5R'}
cursor = "-1"


def continue_work(value):
    try:
        if value == 'cursor':
            file_name = 'cursor'
        else:
            file_name = 'last_dirty_file'
        for i in range(1, 20):
            with open(f'last_data/{file_name}.txt', encoding='utf-8') as f_read:
                last_line = f_read.readlines()[-i]
                cleaned_line = last_line.strip()
            if cleaned_line and cleaned_line != '-1':
                return cleaned_line
    except:
        if value == 'cursor':
            print('Last cursor not detected')
            return '-1'
        else:
            print('Last last_file_number not detected')
            return 1


def write_txt(cursor):
    with open('last_data/cursor.txt', 'a', encoding="utf-8") as file:
        file.write(cursor + '\r\n')


def write_last_dirty_file(laste_dirty_file):
    with open('last_data/last_dirty_file.txt', 'a', encoding="utf-8") as file:
        file.write(str(laste_dirty_file) + '\r\n')


def get_followers():
    global new_str, last_dirty_file, cursor
    cursor = continue_work("cursor")
    last_dirty_file = continue_work('last_dirty_file')
    while True:
        try:
            url = f'https://api.twitter.com/1.1/followers/list.json?cursor={cursor}&screen_name=path&skip_status=true&include_user_entities=false'
            root = requests.get(url, headers=headers).json()
            cursor = root['next_cursor_str']
            print(f'Next cursor {cursor}')
            write_txt(cursor)
            page = root['users']
            new_str += len(page)
            if new_str > 300:
                write_last_dirty_file(last_dirty_file)
                last_dirty_file += 1
                new_str -= 300
            save_followers_to_csv(page)
        except Exception as e:
            print(e)
            print("Going to sleep:")
            print(time.sleep(60))


def save_followers_to_csv(data):
    global last_dirty_file
    headers = ["name", "screen_name", "description", "followers_count",
               'friends_count', "listed_count", "favourites_count", "created_at"]
    with open(f"csv_api/csv_{last_dirty_file}.csv", 'a', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        for profile_data in data:
            profile = []
            for header in headers:
                profile.append(profile_data[header])
            csv_writer.writerow(profile)
    last_dirty_file += 1

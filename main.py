from get_data import get_data
from api import get_data_api
import threading


class Thread(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.func = func

    def run(self):
        self.func()


def main():
    thread_1 = Thread(get_data_api.get_followers)
    thread_2 = Thread(get_data.pars_twit)
    thread_1.start()
    thread_2.start()
    threads = []
    threads.append(thread_1)
    threads.append(thread_2)
    for t in threads:
        t.join()


if __name__ == '__main__':
    main()

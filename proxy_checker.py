import threading
import queue
import requests
import time


BASE_URL = "https://books.toscrape.com/"

valid_proxy = []
q=queue.Queue()

with open("proxy.txt", 'r') as f:
    proxies = f.read().split('\n')
    for item in proxies:
        q.put(item)

def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get(f'{BASE_URL}',
                               proxies={'http': proxy,
                                        'https': proxy})
        except:
            continue
        if res.status_code == 200:
            print(proxy)


for t in range (10):
    threading.Thread(target=check_proxies).start()
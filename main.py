import requests, random
from bots.run import Automation

with open("valid_proxy.txt", 'r') as f:
    proxies = f.read().split("\n")

for index,proxy in enumerate(proxies[:1]):
    with Automation(proxy=proxy) as bot:
        bot.open_window()
        bot.waiting()
        """print(f"Using proxy {index+1} - proxy: {proxy}")
        bot.waiting()
        bot.get_first_name()
        bot.get_last_name()
        bot.generate_password()
        bot.get_user_data()"""
        bot.go_to_acc_creation()
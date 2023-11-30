from bots.run import Automation

with open("valid_proxy.txt", 'r') as f:
    proxies = f.read().split("\n")

for index,proxy in enumerate(proxies[:1]):
    with Automation(proxy=proxy) as bot:
        bot.open_window()
        bot.go_to_acc_creation()
        bot.pass_first_last_name()
        bot.pass_birthday_details()
        bot.get_email_adress()
        bot.set_password()
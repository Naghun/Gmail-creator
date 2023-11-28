from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random, time, string
from fake_useragent import UserAgent

"""
    pip install free-proxy 1.1.1 then check if you want
    from fp.fp import FreeProxy - import 

    optimizations for chrome:
    prefs = {"profile.password_manager_enabled": False, "credentials_enable_service": False, "useAutomationExtension": False}:  -   uklanjanje password managera, autorizacije i auto ekstenzija
    options.add_experimental_option("prefs", prefs):    -   ovdje ih dodajemo
    options.add_experimental_option("useAutomationExtension", False):   -   korisno da se ne mijesaju ekstenzije ukoliko postoje pojedine koje pokusavaju sprijeciti automatizaciju
    options.add_experimental_option("excludeSwitches", ["enable-automation"]):  -   također korisno za sprjecavanje otkrivanja skripti
    options.add_argument('--disable-dev-shm-usage'): shared memory ako se ne varam, disabla je da bi ubrzao proces
    options.add_argument('--no-sandbox'):   -    disablea sand
    options.add_argument("disable-popup-blocking"): -   ...
    options.add_argument("disable-notifications"):
    options.add_argument('--ignore-ssl-errors=yes'):    -   ukoliko postoje errori sa SSL certifikatom tokom testiranja - ISTRAZITI!!!
    options.add_argument('--ignore-certificate-errors'):    -   nastavit ce sa otvaranjem stranica iako postoji SSL error
        more options:
    # options.add_argument('--headless') # UI   -   without window
    # options.add_argument("--incognito")   -   probably in incognito mode
    # options.add_argument(r"--user-data-dir=C:\\Users\\Username\\AppData\\Local\\Google\\Chrome\\User Data")
    # options.add_argument(r'--profile-directory=ProfileName')

"""

SITE_LIST = [
    'https://google.com',
    'https://wizardrytechnique.webflow.io/',
    'https://www.rachelbavaresco.com/',
    'https://lightning-bolt.webflow.io/'
]

TIME_WAIT = 4

SELECTORS = {
    

}

class Automation(webdriver.Chrome):
    def __init__(self, proxy=None):
        executable_path = ChromeDriverManager().install()
        self.service = Service(executable_path)
        self.options = Options()
        self.options.add_argument('--detach=false')
        self.proxy=proxy
        self.user_agent = None
        prefs = {"profile.password_manager_enabled": False, "credentials_enable_service": False, "useAutomationExtension": False}
        self.options.add_experimental_option("prefs", prefs)
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("disable-popup-blocking")
        self.options.add_argument("disable-notifications")
        self.options.add_argument('--ignore-ssl-errors=yes')
        self.options.add_argument('--ignore-certificate-errors')
        super(Automation, self).__init__(options=self.options, service=self.service)
        
    def waiting(self):
        time.sleep(random.randint(1,3))

    def open_window(self):
        if self.proxy:
            self.options.add_argument(f'--proxy-server={self.proxy}')
        self.user_agent = UserAgent(fallback="Mozilla/5.0 (Macintosh; Intel Mac OS X10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36").random
        self.options.add_argument(f"user-agent={self.user_agent}")
        print(f"user agent: {self.user_agent}")
        self.random_url = random.choice(SITE_LIST)
        print(self.random_url)
        super(Automation, self).get(f"{self.random_url}")

    def close_window(self):
        self.quit()

    def get_first_name(self):
        first_name_file=open("first_names.txt", 'r')
        try:
            first_names= [line.strip() for line in first_name_file]
            random_name=random.sample(first_names, 1)
            print(random_name)
        except:
            print("Name not found, check your code or names list")
            self.quit()

    def get_last_name(self):
        last_name_file=open("last_names.txt", 'r')
        try:
            last_names= [line.strip() for line in last_name_file]
            random_last_name=random.sample(last_names, 1)
            return random_last_name
        except:
            print("Last name not found, check your code or names list")
            self.quit()

    def generate_password(self):
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
        size = random.randint(8,12)
        try:
            password = ''.join(random.choice(chars) for x in range(size))
            return password
        except:
            print("Password generation failed!")
            self.quit()

    def get_user_data(self):
        first_name=self.get_first_name()
        last_name=self.get_last_name()
        password =self.generate_password()
        birthday=str(random.randint(1,12)) + "/" + str(random.randint(1,28)) + "/" +  str(random.randint(1980,1999))
        print(str(first_name) + "\t" + str(last_name) + "\t" + str(password) + '\t' + str(birthday))

    def go_to_acc_creation(self):
        random_way=random.randint(1,4)
        print(f"random way choose way number: {random_way}")

        if random_way == 1:
            print("Way Number 1")
            self.get('https://support.google.com/accounts/answer/27441?hl=en')
        elif random_way==2:
            print("Way Number 2")
            self.get("https://accounts.google.com")
        elif random_way==3:
            print("Way Number 3")
            self.get('https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp')
        elif random_way==4:
            print("Way Number 4")
            self.get('https://support.google.com/mail/answer/56256?hl=en')

from selenium import webdriver
from selenium.webdriver.support.ui import Select
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
        #self.options.add_argument('--headless')  # Dodajte ovu opciju za headless režim
        #self.options.add_argument('--disable-gpu')  # Opciono, može pomoći sa headless režimom
        self.options.add_argument('--detach=false')
        self.proxy=proxy
        self.user_agent = None
        self.wait=WebDriverWait(self, 15)
        prefs = {"profile.password_manager_enabled": False, "credentials_enable_service": False, "useAutomationExtension": False}
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
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
        self.position=self.get_window_position()
        self.new_position = (self.position['x'] + 500, self.position['y'])
        self.set_window_position(*self.new_position)
        self.first_name = None
        self.last_name = None

        
    def waiting(self):
        time.sleep(random.randint(1,3))

    def open_window(self):
        if self.proxy:
            self.options.add_argument(f'--proxy-server={self.proxy}')
        """self.user_agent = UserAgent(fallback="Mozilla/5.0 (Macintosh; Intel Mac OS X10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36").random
        self.options.add_argument(f"user-agent={self.user_agent}")"""
        #print(f"user agent: {self.user_agent}")
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
            return random_name
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

    def get_birthday(self):
        month=random.randint(1,12)
        day=random.randint(1,28)
        year=random.randint(1980,2004)
        birthday={'month':month,
                  'day': day,
                  'year':year}
        return birthday

    def go_to_acc_creation(self):
        random_way=random.randint(1,3)
        print(f"random way choose way number: {random_way}")

        if random_way == 1:
            print(f"proxy is: {self.proxy}")
            print("Way Number 1")
            try:
                self.get('https://support.google.com/accounts/answer/27441?hl=en')
                target_element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div[1]/a')))
                target_element.click()
                create_new=self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div/button')))   
                create_new.click()
                selector=self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div/ul/li[1]')))    
                selector.click()  
                print("Way 1 acc creation page successfully open")
            except:
                print("Page not opened, task failed - program closing...!")

        elif random_way==2:
            print(f"proxy is: {self.proxy}")
            print("Way Number 2")
            try:
                self.get("https://accounts.google.com")
                target_element2 = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf ksBjEc lKxP2d LQeN7 FliLIb uRo0Xe TrZEUc Xf9GD']")))
                target_element2.click()
                for_personal_use = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li[@class='G3hhxb VfPpkd-StrnGf-rymPhb-ibnC6b']"))).click()
                print("Way 2 acc creation page successfully open")
            except:
                print("Page not opened, task failed - program closing...!")


        elif random_way==3:
            print(f"proxy is: {self.proxy}")
            print("Way Number 3")
            try:
                self.get('https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp')
                print("Way 3 acc creation page successfully open")
            except:
                print("Page not opened, task failed - program closing...!")


    def pass_first_last_name(self):
        first_name_tag = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='firstName']")))    #//*[@id="firstName"] #//*[@id="firstName"]
        
        if first_name_tag:
            first_name_tag.clear()
            self.first_name = self.get_first_name()
            print(self.first_name)
            first_name_tag.send_keys(self.first_name)
        else:
            print("Element nije pronađen.")

        time.sleep(1)
        last_name_tag=self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="lastName"]')))
        if last_name_tag:
            last_name_tag.clear()
            time.sleep(1)
            self.last_name=self.get_last_name()
            print(self.last_name)
            last_name_tag.send_keys(self.last_name)
        else:
            print("Element nije pronađen.")

        
        next_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="collectNameNext"]/div/button')))
        if next_button:
            next_button.click()
        


    def pass_birthday_details(self):
        birthday_details=self.get_birthday()
        month_tag=self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="month"]')))
        if month_tag:
            desired_month=Select(month_tag)
            desired_month.select_by_value(str(birthday_details["month"]))
        else:
            print("Month element not located")

        day_tag=self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="day"]')))
        if day_tag:
            day_tag.send_keys(birthday_details["day"])
        else:
            print("Day Input field element not located")

        year_tag=self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="year"]')))
        if year_tag:
            year_tag.send_keys(birthday_details["year"])
        else:
            print("Year Input field element not located")

        gender = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="gender"]')))
        if gender:
            desired_gender=Select(gender)
            desired_gender.select_by_value(str(random.randint(1,2)))
        else:
            print("Gender field error")

        time.sleep(1)
        next_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="birthdaygenderNext"]')))
        if next_button:
            next_button.click()
        else:
            print("Problem with confirming button")

        time.sleep(1)

    def get_email_adress(self):
        if self.first_name is not None and self.last_name is not None:
            digits = random.randint(1, 1000)
            gmail_adress = f"{self.first_name[0]}{self.last_name[0]}.{digits}"
            print(gmail_adress)
        else:
            print("Error unpacking name data")


        attempts = 0
        while attempts < 3:
            try:
                print("Attempt:", attempts + 1)
                make_username = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/span/div[3]/div'))) 
                make_username.click()
                break 
            except Exception as e:
                print(f"Error clicking 'Make Username' button: {e}")
                attempts += 1

        if attempts == 3:
            print("Failed to click 'Make my own username' button after 3 attempts.")


        try:
            new_username_field=self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input')))
            if new_username_field:
                new_username_field.clear()
                new_username_field.send_keys(gmail_adress)
        except:
            print("Error entering new Gmail username")

        try:
            next_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="next"]/div/button')))
            next_button.click()
        except:
            print("Error finding next button")
        time.sleep(3)

    def set_password(self):
        print("Setting password...")
        characters = string.ascii_letters + string.digits  # slova + brojevi
        password_length = random.randint(8, 12)
        password = ''.join(random.choice(characters) for _ in range(password_length))
        print(f"Password is: {password}")

        try:
            password_field=self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="passwd"]/div[1]/div/div[1]/input')))
            password_field.clear()
            password_field.send_keys(password)
        except:
            print("Error setting password")

        try:
            confirm_field=self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="confirm-passwd"]/div[1]/div/div[1]/input')))
            confirm_field.clear()
            confirm_field.send_keys(password)
        except:
            print("Error setting password")

        time.sleep(2)

        try:
            next_button=self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="createpasswordNext"]/div/button')))
            next_button.click()
        except:
            print("Error setting password")

        print("Password is set")
        time.sleep(4)

        

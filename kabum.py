from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

SLEEP_TIME = 3

class KabumBot():
    def __init__(self) -> None:
        self.retailer_id = 'a86c4af6-572f-482c-8dff-50914970e427'
        op = webdriver.ChromeOptions()
        op.add_argument("--window-size=1920,1080")
        op.add_argument('--disable-gpu')
        op.add_argument('--no-sandbox')
        op.add_argument('--headless')
        op.add_argument('--disable-dev-shm-usage')
        op.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        #service = Service(ChromeDriverManager().install())
        op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        self.browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=op)
    
    def login(self, email, password):
        self.browser.get('https://kabum.com.br/login')
        time.sleep(SLEEP_TIME)
        self.browser.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[1]/form/div/div[1]/div/div/input').send_keys(email)
        self.browser.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[1]/form/div/div[2]/div/div/input').send_keys(password)
        self.browser.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[1]/form/div/button').click()
        time.sleep(SLEEP_TIME)
    
    def accessCart(self, url):
        self.browser.get(url)
        time.sleep(SLEEP_TIME)
        try:
            
            price = int(self.browser.find_element(By.XPATH, '/html/body/div[1]/main/article/section/div[3]/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/h4').text[3:].replace(',', '').replace('.', ''))
        except:
            try:
                price = int(self.browser.find_element(By.XPATH, '/html/body/div[1]/main/article/section/div[2]/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/h4').text[3:].replace(',', '').replace('.', ''))
            except:
                raise
        try:
            self.browser.find_element(By.XPATH, '/html/body/div[1]/main/article/section/div[3]/div[1]/div/div/div[2]/div[1]/div[2]/div[2]/button').click()
        except:
            try:
                self.browser.find_element(By.XPATH, '/html/body/div[1]/main/article/section/div[2]/div[1]/div/div/div[2]/div[1]/div[2]/div[2]/button').click()
            except Exception as e:
                print('Página do produto incompatível em: ', url)
        time.sleep(SLEEP_TIME)
        try:
            self.browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/div/div/button[2]').click()
        except:
            try:
                self.browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[3]/div/button[2]').click()
            except:
                print('Página pré-carrinho incompatível em URL: ', url)
        time.sleep(2*SLEEP_TIME)
        return price
    
    def tryCoupon(self, couponCode, **kwargs):
        available = False
        self.browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[2]/div/section/div/form/div/div/div/div/input').send_keys(couponCode)
        self.browser.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div/div/div[2]/div/section/div/form/button').click()
        time.sleep(2*SLEEP_TIME)
        couponResponse = self.browser.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div/div/div[2]/div/section/div/div').get_attribute('innerHTML')

        if 'CUPOM APLICADO COM SUCESSO' in couponResponse:
            available = True
        return available
            
            
    def refreshCart(self):
        self.browser.refresh()
        time.sleep(SLEEP_TIME)
    
    def removeProductFromCart(self):
        self.browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[2]/section/div[1]/button').click()
        time.sleep(SLEEP_TIME)
        self.browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[2]/section/div[1]/div[2]/div/button[2]').click()
        time.sleep(SLEEP_TIME)

    def closeBrowser(self):
        self.browser.quit()
    
if __name__ == '__main__':
    url = 'https://tidd.ly/3H8guSg'
    k = KabumBot()
    k.login('bboyrafinhazika@gmail.com', '123321asddsa')
    k.accessCart(url)
    k.tryCoupon('SEJANINJA')
    #print(k.couponVerify(url, 'SEJANINJA'))
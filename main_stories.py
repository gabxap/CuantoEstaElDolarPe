from PIL import ImageFont, ImageDraw, Image
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import math

pyautogui.FAILSAFE = False

def generate_image_1():
    today = datetime.today()
    today_text = today.strftime("%d/%m/%Y %I:%M %p")

    image = Image.open("images/bases/stories/1.png")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("fonts/Montserrat-Regular.ttf", 40)

    draw.text((112, 1510), "Actualizado " + today_text, font=font)

    image.save("images/outputs/1.png")


def generate_image_venta(venta):
    image = Image.open("images/bases/stories/2.png")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("fonts/Montserrat-Bold.ttf", 65)

    draw.text((365, 980), f"{venta[0]} Soles", font=font)
    draw.text((370, 1385), f"{venta[1]} Soles", font=font)

    image.save("images/outputs/2.png")


def generate_image_compra(compra):
    image = Image.open("images/bases/stories/3.png")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("fonts/Montserrat-Bold.ttf", 65)

    draw.text((365, 980), f"{compra[0]} Soles", font=font)
    draw.text((370, 1385), f"{compra[1]} Soles", font=font)

    image.save("images/outputs/3.png")

def generate_image(venta, compra):
    today = datetime.today()
    today_text = today.strftime("%d/%m/%Y %I:%M %p")
    
    image = Image.open("images/bases/stories/only_one.png")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("fonts/Montserrat-Bold.ttf", 65)
    font2 = ImageFont.truetype("fonts/Montserrat-Regular.ttf", 40)

    draw.text((375, 830), f"{venta[0]} Soles", font=font)
    draw.text((390, 1000), f"{venta[1]} Soles", font=font)
    draw.text((375, 1370), f"{compra[0]} Soles", font=font)
    draw.text((390, 1535), f"{compra[1]} Soles", font=font)
    draw.text((220, 1680), "Actualizado " + today_text, font=font2)
    image.save("images/outputs/only_one.png")


def get_data():
    def round_half_up(n, decimals=2):
        multiplier = 10 ** decimals
        return math.floor(n * multiplier + 0.5) / multiplier

    precio_compra = []
    precio_venta = []
    site = requests.get('https://cuantoestaeldolar.pe/cambio-de-dolar-online', headers={'Referer' : 'https://cuantoestaeldolar.pe'})
    soup = BeautifulSoup(site.content, 'html.parser')
    table = soup.find_all("div", {"class": "Quotation_root__MlWtc md:mt-0 md:mr-6"})[0]
    all_ps = table.find_all("p", {"class": "ValueQuotation_text___mR_0"})
    precio_compra_sunat = "{:.2f}".format(round_half_up(float(all_ps[0].text)))
    precio_venta_sunat = "{:.2f}".format(round_half_up(float(all_ps[1].text)))
    precio_compra_calle = "{:.2f}".format(round_half_up(float(all_ps[2].text)))
    precio_venta_calle = "{:.2f}".format(round_half_up(float(all_ps[3].text)))

    print(precio_compra_sunat)    
    print(precio_venta_sunat)    
    print(precio_compra_calle)    
    print(precio_venta_calle)    
    precio_venta = [precio_venta_sunat, precio_venta_calle]
    precio_compra = [precio_compra_sunat, precio_compra_calle]
   
    return [precio_venta, precio_compra]


def upload_story(number):
    options = Options()
    
    options.add_argument("--user-data-dir=chrome-data22")
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    mobile_emulation = { "deviceName": "Nexus 5" }
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(options=options, service=Service('/home/gabriel/Desktop/chromedriver'))
    driver.get('https://www.instagram.com')
    time.sleep(5)
    pyautogui.click(x=300, y=180)
    time.sleep(1)
    pyautogui.click(x=300, y = 240)
    time.sleep(2)
    pyautogui.click(x=500, y = 240)
    for i in range(number-1):
        pyautogui.press('down')
    pyautogui.press('enter')
    print("here")
    time.sleep(10)
    pyautogui.rightClick(x=100, y=200)
    time.sleep(3)
    pyautogui.click(x=130, y=340)
    time.sleep(15)
    pyautogui.hotkey('ctrl', 'shift', 'm')
    time.sleep(10)
    pyautogui.click (x=750, y=850)
    time.sleep(5)
    driver.quit()
    
def generate_all_and_upload(precios):
    generate_image(precios[0], precios[1])
    upload_story(1)

    

def main():
    precios = []
    while True:
        print('---------------------------')
        print('attempted')
        now = datetime.now()
        current_time = now.strftime("%I:%M:%S %p")
        print(current_time)
        print(precios)
        if len(precios) == 0:
            precios = get_data()
            generate_all_and_upload(precios)
        else:
            new_precios = get_data()
            print(new_precios)
            changed = False
            for i in range(2):
                for e in range(2):
                    if precios[i][e] != new_precios[i][e]:
                        changed = True
                        break
                if changed:
                    break
                
            if changed:
                print('it changed!!!')
                precios = new_precios
                generate_all_and_upload(precios)        
        time.sleep(1800)

def main_test():
    precios = get_data()
    generate_image(precios[0], precios[1])
    #generate_image_1()
    #generate_image_venta(precios[0])
    #generate_image_compra(precios[1])
    #print('ok')
    
if __name__ == '__main__':
    main()



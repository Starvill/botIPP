from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json

url = 'https://www.copart.com/lot/48907953/2022-honda-accord-sport-dc-washington-dc'

'''
    Соф, тут сразу можно импортировать на вход подается url запрос типа того что выше этого комментария
'''

def pasre_url(lot_url):
    options = webdriver.ChromeOptions()
    options.add_argument(
        "User-Agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )
    service = Service(executable_path="D:\\5sem\\IPP\\bot\\chrome_driver\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    def check_exists_by_xpath(xpath):
        try:
            driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def check_text_exists_by_xpath(xpath):
        try:
            driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return "Нет\Неизвестно\Не указано на сайте"
        return driver.find_element(By.XPATH, xpath).text

    def copart_parser_lot():
        name_car = driver.find_element(By.CSS_SELECTOR, '.title-and-highlights').text  # Название машины
        lot_number = driver.find_element(By.ID, 'LotNumber').text  # Номер лота
        vin = driver.find_element(By.ID, 'vinDiv').text  # Vin
        condition = driver.find_element(By.CSS_SELECTOR,'.lot-details-desc.highlights-popover-cntnt.text-CERT-D.d-flex.j-c_s-b').text  # Run-and-drive
        odometr = driver.find_element(By.CSS_SELECTOR,'.lot-details-desc.odometer-value.w100').text  # Одометр
        type_engine = check_text_exists_by_xpath('//*[@id="lot-details"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div[17]/div/span') # Тип двигателя

        if (check_exists_by_xpath('//*[@id="lot-details"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div[15]/div/span') == True):  # Цвет
            color = driver.find_element(By.XPATH,'//*[@id="lot-details"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div[15]/div/span').text
        else:
            color = driver.find_element(By.XPATH,'//*[@id="lot-details"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div[16]/div/span').text

        if (driver.find_element(By.XPATH,'//*[@id="lot-details"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div[19]/div/label').text == "Drive:"):  # Привод
            transmission = driver.find_element(By.XPATH,'//*[@id="lot-details"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div[19]/div/span').text
        else:
            transmission = driver.find_element(By.XPATH,'//*[@id="lot-details"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div[18]/div/span').text

        if(check_exists_by_xpath('//*[@id="lot-details"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div[25]/div/span') == True and driver.find_element(By.XPATH,'//*[@id="lot-details"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div[23]/div/label').text == 'Fuel:'):# Тип топлива
            fuel = driver.find_element(By.XPATH,'//*[@id="lot-details"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div[25]/div/span').text
        else:
            fuel = driver.find_element(By.XPATH,'//*[@id="lot-details"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div[23]/div/span').text
        primary_damage = check_text_exists_by_xpath('//*[@id="lot-details"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div[8]/span')  # Основное повреждение
        secondary_damage = check_text_exists_by_xpath('//*[@id="lot-details"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div[9]/span') # Вторичное повреждение
        sale_location = check_text_exists_by_xpath('//*[@id="sale-information-block"]/div[2]/div[2]/span/a') # Место продажи

        url_data ={'url': lot_url,
                     'name': name_car,
                     'lot_number': lot_number,
                     'vin': vin,
                     'condition': condition,
                     'odometr': odometr,
                     'type_engine': type_engine,
                     'color': color,
                     'transmission': transmission,
                     'fuel': fuel,
                     'primary_damage': primary_damage,
                     'secondary_damage': secondary_damage,
                     'sale_location': sale_location
                     }
        with open('databaseLots.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            data.append(url_data)

        with open('databaseLots.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
        with open('this_lot_data.txt', 'w', encoding='utf-8') as outfile:
            json.dump(url_data, outfile, indent=4, ensure_ascii=False)

    #Вызов функций
    try:
        driver.get(url=url)
        time.sleep(20)
        if(url.find('www.copart.com')!=-1):
            copart_parser_lot()
        else:
            return "Работает пока только с Copart"
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        return open('this_lot_data.txt', mode='r', encoding='utf-8')


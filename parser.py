from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json

test_data_url = []
test_data_url.append('40000')
test_data_url.append('159000')
test_data_url.append('1987')
test_data_url.append('2019')
test_data_url.append('Volkswagen')
test_data_url.append('Jetta')
test_data_url.append('Normal Wear')
test_data_url.append(True)
'''
    Соф, смотри, пользователь должен будет ввести только в таком порядке 
    Марка, Модель, год с какого по какой, пробег также от и до
    следующий ввод попрошу сделать с кнопками или командами на твоё усмотрение, но ввод может быть только такой:
        Типы повреждений:
            Не указывать - при данном вводе передаётся ""
            Без повреждений - при данном вводе передаётся Normal Wear
            Задняя часть - при данном вводе передаётся Rear End
            Небольшие вмятины или царапины  - при данном вводе передаётся Minor Dent/Scratch
            Передние часть - при данном вводе передаётся Front End
    Последним вводом также сделать кнопками
        Run and Drive?
            Да - на вход True
            Нет - на вход False
    Тоесть на вход подаваться должны в точной последовательности как и в примере выше комментария
    Примечание функция возвращает файл this_url_data.txt
'''


def parser(data_url):
    options = webdriver.ChromeOptions()
    options.add_argument(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
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


    def find_by_copart():
        damage_type_code_copart = {
            "": "",
            "Normal Wear": ",%22PRID%22:%5B%22damage_type_code:DAMAGECODE_NW%22%5D",
            "Rear End": ",%22PRID%22:%5B%22damage_type_code:DAMAGECODE_RR%22%5D",
            "Minor Dent/Scratch": ",%22PRID%22:%5B%22damage_type_code:DAMAGECODE_MN%22%5D",
            "Front End": ",%22PRID%22:%5B%22damage_type_code:DAMAGECODE_FR%22%5D",
        }
        if(data_url[7] == True):
            run_and_drive = '%22FETI%22:%5B%22lot_condition_code:CERT-D%22%5D,'
        else: run_and_drive= ''
        odometr_from = data_url[0]
        odometr_to = data_url[1]
        year_min = data_url[2]
        year_max = data_url[3]
        make = data_url[4]
        model = data_url[5]
        damage_type = data_url[6]
        damage_type_url = ''
        for el in damage_type_code_copart:
            if el == damage_type:
                damage_type_url = damage_type_code_copart[el]
        make_url = '%22MAKE%22:%5B%22lot_make_desc:%5C%22' + make.upper() + '%5C%22%22%5D'
        model_url = ',%22MODL%22:%5B%22manufacturer_model_desc:%5C%22' + model.upper() + '%5C%22%22%5D'
        odometr_from_to_url = ',%22ODM%22:%5B%22odometer_reading_received:%5B' + odometr_from + '%20TO%20' + odometr_to + '%5D%22%5D'
        year_url = ',%22VEHT%22:%5B%22vehicle_type_code:VEHTYPE_V%22%5D,%22YEAR%22:%5B%22lot_year:%5B' + year_min + '%20TO%20' + year_max + '%5D%22%5D%7D'
        url = 'https://www.copart.com/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B' + run_and_drive + make_url + model_url + odometr_from_to_url + damage_type_url + year_url + ',%22sort%22:%5B%22salelight_priority%20asc%22,%22member_damage_group_priority%20asc%22,%22auction_date_type%20desc%22,%22auction_date_utc%20asc%22%5D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=Search%20vehicles&from=%2FvehicleFinder'

        last_urls = []
        data_url.append(url)
        try:
            driver.get(url=url)
            for j in range(2, 5, 1):
                time.sleep(25)
                for i in range(1, 21, 1):
                    str_i = str(i)
                    test_parse_url = '//*[@id="pr_id_1-table"]/tbody/tr[' + str_i + ']/td[2]/span[2]/div/span/a'
                    test_url = (driver.find_element(By.XPATH, test_parse_url).get_attribute('href'))
                    last_urls.append(test_url)
                if j != 4:
                    driver.find_element(By.XPATH,
                                        '//*[@id="pr_id_1"]/p-paginator/div/span[2]/button[' + str(j) + ']').click()

            button4Url = '//*[@id="pr_id_1"]/p-paginator/div/span[2]/button[4]'
            if check_exists_by_xpath(button4Url) == True:
                button4Bool = driver.find_element(By.XPATH, button4Url).is_enabled()
            else:
                button4Bool = False
            while button4Bool == True:
                time.sleep(20)
                if check_exists_by_xpath(button4Url) == True:
                    button4Bool = driver.find_element(By.XPATH, button4Url).is_enabled()
                else:
                    button4Bool = False
                driver.find_element(By.XPATH, button4Url).click()
                for i in range(1, 21, 1):
                    str_i = str(i)
                    test_parse_url = '//*[@id="pr_id_1-table"]/tbody/tr[' + str_i + ']/td[2]/span[2]/div/span/a'
                    test_url = driver.find_element(By.XPATH, test_parse_url).get_attribute('href')
                    last_urls.append(test_url)

        except Exception as ex:
            print(ex)
        finally:
            url_data = {'odometr_from': data_url[0],
                             'odometr_to': data_url[1],
                             'year_min': data_url[2],
                             "year_max": data_url[3],
                             "make": data_url[4],
                             "model": data_url[5],
                             "main-url": data_url[6],
                             "urls": last_urls
                             }
            with open('databaseUrl.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                data.append(url_data)

            with open('databaseUrl.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            with open('this_url_data.txt', 'w', encoding='utf-8') as outfile:
                json.dump(url_data, outfile, indent=4, ensure_ascii=False)
            driver.close()
            driver.quit()

    find_by_copart()
    return open('this_url_data.txt', mode='r', encoding='utf-8')


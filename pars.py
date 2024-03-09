from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
import main

driver = webdriver.Chrome()

def parsing_openedu(login, password):
    with open('info.json', encoding='utf-8') as file:
        info = json.load(file)

    filtered_file = list(map(lambda x: x["lms_web_url"], filter(lambda x: 'Аттестация по теме' in x["display_name"], info['course_blocks']["blocks"].values())))
    
    driver.quit()

    spisok = ('тема1', 'тема2', 'тема3', "тема4", "тема5", "тема6", "тема7", "тема8", "тема9", "тема10", "тема11", "тема12", "тема13", "тема14")
    count = 0

    for url in filtered_file:
        main.script(url, spisok[count], login, password)
        count += 1

def authorization(login:str, password:str):
    login_url = 'https://cas.spbstu.ru/login?service=https%3A%2F%2Fcas.spbstu.ru%2Foauth2.0%2FcallbackAuthorize%3Fclient_id%3D2121fe8d-d9fc-42a8-9478-85575426641b%26redirect_uri%3Dhttps%253A%252F%252Fsso.openedu.ru%252Frealms%252Fopenedu%252Fbroker%252Fspbstu%252Fendpoint%26response_type%3Dcode%26client_name%3DCasOAuthClient'
    
    driver.get(login_url)

    username_input = driver.find_element(By.ID, 'user')
    password_input = driver.find_element(By.ID, 'password')

    username_input.send_keys(login)
    password_input.send_keys(password)

    driver.find_element(By.ID, 'doLogin').click()

    time.sleep(5)

    driver.get('https://courses.openedu.ru/api/course_home/outline/course-v1:spbstu+ACCOUNT+fall_2023')

    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')

    information = soup.body.text

    deserealize = json.loads(information)

    with open('info.json', 'w', encoding='utf-8') as file:
        json.dump(deserealize, file, indent=4, ensure_ascii=False)
    

def first_part():
    new_url = 'https://apps.openedu.ru/learning/course/course-v1:spbstu+ACCOUNT+fall_2023/home'

    driver.get(new_url)
    time.sleep(5)

    xpath = "//*[@id='root']/div/main/div/div[1]/div[3]/ul/li[5]/a"

    driver.find_element(By.XPATH, xpath).click()


def main():
    first_part()
    time.sleep(3)

    authorization('Логин', 'пароль')

    parsing_openedu('Логин', 'пароль')


if __name__ == '__main__':
    main()
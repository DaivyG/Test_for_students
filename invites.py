from selenium import webdriver
from selenium.webdriver.common.by import By

import time


list_of_urls = ['https://app.onlinetestpad.com/tests/v7qnztifxbtak', 'https://app.onlinetestpad.com/tests/qc536adunqjpq', 'https://app.onlinetestpad.com/tests/nnr4knsws7r7o', 'https://app.onlinetestpad.com/tests/warqn4uzn3fjg', 'https://app.onlinetestpad.com/tests/vnixbhan3kd7m', 'https://app.onlinetestpad.com/tests/ng5g4w3hjwrvu', 'https://app.onlinetestpad.com/tests/pyp3ajspe3mcm', 'https://app.onlinetestpad.com/tests/z2c5wczhjuw26', 'https://app.onlinetestpad.com/tests/7mttv3jfdxcmq', 'https://app.onlinetestpad.com/tests/u4i2rmsxnl4x2', 'https://app.onlinetestpad.com/tests/722ajk7kim2xu', 'https://app.onlinetestpad.com/tests/3m5tsiuzbgwau', 'https://app.onlinetestpad.com/tests/sl7oopfjyyyhy', 'https://app.onlinetestpad.com/tests/puve7j57jeyiy', 'https://app.onlinetestpad.com/tests/ah6y74cmsmt34']

driver = webdriver.Chrome()

def doInvites(dict_of_students:dict):
    for url in list_of_urls:
        driver.get(url)
        time.sleep(2)

        driver.find_element(By.XPATH, '/html/body/app-root/basic/div/div[1]/div/div[1]/ul/li[11]/a').click()
        time.sleep(1)

        driver.find_element(By.XPATH, '//*[@id="dpagemain"]/div[2]/div[2]/div[2]/div/test-selector/test-invitations-groups/div/invitations-groups/ul/li[1]/div/div[2]/span').click()
        time.sleep(1)

        driver.find_element(By.XPATH, '//*[@id="dpagemain"]/div[2]/div[2]/div[2]/div/test-selector/test-invitations-users/div/invitations-users/div/div[1]/div[2]/button[1]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/div[2]/label/span').click()
        for email, name in dict_of_students.items():
            
            input_name = driver.find_element(By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/div[1]/form/div[1]/div/input')
            input_email = driver.find_element(By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/div[1]/form/div[2]/div/input')

            input_name.clear()
            input_email.clear()

            input_name.send_keys(name)
            input_email.send_keys(email)

            driver.find_element(By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/div[1]/div/select').click()
            time.sleep(1)

            driver.find_element(By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/div[1]/div/select/option[7]').click()

            driver.find_element(By.XPATH, '/html/body/ngb-modal-window/div/div/div[3]/button[2]').click()
            time.sleep(2)


def doLogin_onlineTestpad():
    url = 'https://onlinetestpad.com/ru/account/login?ReturnUrl=/ru'

    driver.get(url)
    time.sleep(3)

    login = driver.find_element(By.ID, 'txtEmail')
    password = driver.find_element(By.ID, 'txtPassword')

    login.send_keys('guseynov.davidka@mail.ru')
    password.send_keys('pifjy5-capVyr-zyphaw')

    driver.find_element(By.XPATH, '/html/body/div/div/div/div/form/div[5]/button').click()

def main():
    need_to_invite = {} #Ввести mail и имя в формате 'mail':'Имя фамилия'

    doLogin_onlineTestpad()

    doInvites(need_to_invite)

if __name__ == '__main__':
    main()
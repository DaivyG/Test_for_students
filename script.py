from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json


driver = webdriver.Chrome()

def doLogin_onlineTestpad():
    url = 'https://onlinetestpad.com/ru/account/login?ReturnUrl=/ru'

    driver.get(url)
    time.sleep(3)

    login = driver.find_element(By.ID, 'txtEmail')
    password = driver.find_element(By.ID, 'txtPassword')

    login.send_keys('Логин онлайнтестпад') #Ввести логин
    password.send_keys('Пароль онлайнтестпад') #Ввести пароль

    driver.find_element(By.XPATH, '/html/body/div/div/div/div/form/div[5]/button').click()


def doTest(theme):
    driver.find_element(By.XPATH, '//*[@id="dpagemain"]/div[2]/div[2]/div[2]/div/test-selector/test-dashboard/div/div[1]/div[1]/div[1]/div[3]/a/i').click()
    time.sleep(1)

    driver.find_element(By.XPATH, '//*[@id="dAddQuestionsAction"]/button').click()
    time.sleep(1)   #дальше идет добавление конкретных вопросов

    with open(f'Вопросы/{theme}.json', encoding='utf-8') as file:
        information:dict = json.load(file)
        for question, total_answers in information.items():
            try:
                answers = total_answers[0]
                correct_answers = total_answers[1]

                if len(correct_answers) == 1:
                    driver.find_element(By.XPATH, '//*[@id="dpageaside"]/site-pageaside/div[2]/div/div[1]/test-questions-newlist/div/a[1]/button').click()
                    time.sleep(1)

                    for _ in range(len(answers) - 2):
                        driver.find_element(By.XPATH, '//*[@id="qid_0"]/div/test-question-edit/div/div/div[1]/div/test-question-editor/div[4]/test-question-edit-rbchk/div[1]/button').click()
                    time.sleep(1)

                    frames = driver.find_elements(By.CLASS_NAME, 'tox-edit-area__iframe')

                    #Написание вопроса
                    question_frame = frames[0]
                    driver.switch_to.frame(question_frame)

                    question_field = driver.find_element(By.ID, "tinymce")

                    question_field.send_keys(question)
                    driver.switch_to.default_content()
                    #конец

                    frames = frames[1:]
                    count = 0

                    for frame, answer in zip(frames, answers):
                        driver.switch_to.frame(frame)

                        answer_field = driver.find_element(By.ID, 'tinymce')

                        answer_field.send_keys(answer)

                        driver.switch_to.default_content()

                        if answer in correct_answers:
                            score = driver.find_elements(By.XPATH, '//*[@id="asdf123"]')[count]
                            score.clear()

                            score.send_keys('1')

                        count += 1

                    driver.find_element(By.XPATH, '//*[@id="qid_0"]/div/test-question-edit/div/div/div[2]/button[2]').click()
                    time.sleep(0.5)
                
                else:
                    driver.find_element(By.XPATH, '//*[@id="dpageaside"]/site-pageaside/div[2]/div/div[1]/test-questions-newlist/div/a[2]/button').click()
                    time.sleep(1)

                    for _ in range(len(answers) - 2):
                        driver.find_element(By.XPATH, '//*[@id="qid_0"]/div/test-question-edit/div/div/div[1]/div/test-question-editor/div[4]/test-question-edit-rbchk/div[1]/button').click()
                    time.sleep(1)

                    frames = driver.find_elements(By.CLASS_NAME, 'tox-edit-area__iframe')

                    #Написание вопроса
                    question_frame = frames[0]
                    driver.switch_to.frame(question_frame)

                    question_field = driver.find_element(By.ID, "tinymce")

                    question_field.send_keys(question)
                    driver.switch_to.default_content()
                    #конец

                    frames = frames[1:]
                    count = 0

                    for frame, answer in zip(frames, answers):
                        driver.switch_to.frame(frame)

                        answer_field = driver.find_element(By.ID, 'tinymce')

                        answer_field.send_keys(answer)

                        driver.switch_to.default_content()

                        if answer in correct_answers:
                            driver.find_element(By.XPATH, '//*[@id="qid_0"]/div/test-question-edit/div/div/div[1]/div/test-question-editor/div[4]/test-question-edit-rbchk/div[2]/table/tbody/tr[1]/td[4]/div/label/input').click()
                        count += 1

                driver.find_element(By.XPATH, '//*[@id="qid_0"]/div/test-question-edit/div/div/div[2]/button[2]').click()
                time.sleep(1)

            except Exception as e:
                print(f'Ошибка {e}')

        time.sleep(4)

def doGoing_to_directory():

    list_of_themes = ['тема1', 'тема2', 'тема3', 'тема4', 'тема5', 'тема6', 'тема7', 'тема8', 'тема9', 'тема10', 'тема11', 'тема12', 'тема13', 'тема14']

    for theme in list_of_themes:
        driver.get('https://app.onlinetestpad.com/tests')
        time.sleep(3)
        
        driver.find_element(By.XPATH, '//*[@id="dpagemain"]/div[2]/div[2]/div[1]/div/button').click()

        name_of_test = driver.find_element(By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/div[1]/input')
        name_of_test.send_keys(f'Бухучет/{theme}')
        time.sleep(0.5)

        driver.find_element(By.ID, 'newTestType_20').click()
        time.sleep(0.5)

        driver.find_element(By.XPATH, '/html/body/ngb-modal-window/div/div/div[3]/button[1]').click()
        time.sleep(3)

        doTest(theme)

def main():
    doLogin_onlineTestpad()

    doGoing_to_directory()

if __name__ == '__main__':
    main()
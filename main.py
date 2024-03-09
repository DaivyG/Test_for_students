import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from loguru import logger


#Можно попробовать убрать логин, тем самым ускорив процесс формирования теста

def script(course_url, theme, login, password):
    logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")

    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    logger.debug("Старт")
    driver = webdriver.Chrome(options=chrome_options)

    logger.debug("Переход по ссылке")
    driver.get(course_url)

    wait = WebDriverWait(driver, 10)
    logger.debug("Ожидание элемента")
    social_form_item = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.social-form__item:nth-child(5) > a:nth-child(1) > span:nth-child(2)")))
    social_form_item.click()

    logger.debug("Ожидание поля ввода")
    username_field = wait.until(EC.visibility_of_element_located((By.ID, "user")))
    username_field.send_keys(login)
    driver.find_element(By.ID, "password").send_keys(password)

    login_button = wait.until(EC.element_to_be_clickable((By.ID, "doLogin")))
    logger.debug("Логин")
    login_button.click()

    logger.debug("Повторный переход по url")
    driver.get(course_url)

    logger.debug("Прокрутка до конца страницы")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "unit-iframe")))

        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'html.parser')

        # Find all problem wrappers
        problems = soup.find_all('div', class_='problems-wrapper')
        extracted_data = {}

        for problem in problems:
            question = problem.find('h3', {'class': 'problem-header'})
            if question:
                question_text = question.text.strip()
                options = [opt.text.strip() for opt in problem.find_all('label', class_='response-label')]
                correct_answer = [opt.text.strip() for opt in problem.find_all('label', class_='choicegroup_correct')]

                if correct_answer:
                    extracted_data[question_text] = [options, correct_answer]


        with open(f'Вопросы/{theme}.json', 'r', encoding='utf-8') as f:
            try:
                data:dict = json.load(f)

                all_questions = data.keys()

            except:
                data = {}

                all_questions = data.keys()
        
        logger.debug('Прочитал вопросы')
        keys_to_remove = []

        for key in extracted_data.keys():
            if key in all_questions:
                keys_to_remove.append(key)

        logger.debug('Составил список ключей для удаления')

        for key in keys_to_remove:
            del extracted_data[key]

        logger.debug('Удалил повторения')

        data.update(extracted_data)
        logger.debug('Собрал всю информацию в одну переменную')

        with open(f'Вопросы/{theme}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        logger.success(f"Cохранил в {theme}")

    except Exception as e:
        logger.error(f"Ошибка: {e}")

    finally:
        driver.quit()

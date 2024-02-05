import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

conn = sqlite3.connect('resumes.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE resumes (
        id INTEGER PRIMARY KEY,
        job_position TEXT,
        years_of_experience INTEGER,
        skills TEXT,
        location TEXT,
        salary_expectation TEXT
    )
''')
conn.commit()


def parse_work_ua(criteria):
    driver = webdriver.Chrome()

    driver.get('https://www.work.ua/')

    job_position_input = driver.find_element(By.ID, 'id_job')
    job_position_input.send_keys(criteria['job_position'])
    job_position_input.send_keys(Keys.RETURN)

    resumes = driver.find_elements(By.CLASS_NAME, 'card-hover')
    for resume in resumes:
        job_position = resume.find_element(By.CLASS_NAME, 'add-bottom-sm').text
        cursor.execute(
            "INSERT INTO resumes (job_position, years_of_experience, skills, location, salary_expectation) VALUES (?, ?, ?, ?, ?)",
            (job_position, criteria['years_of_experience'], criteria['skills'], criteria['location'],
             criteria['salary_expectation']))

    driver.quit()


def parse_robota_ua(criteria):
    driver = webdriver.Chrome()

    driver.get('https://robota.ua/')

    job_position_input = driver.find_element(By.ID, 'ctl00_content_Keyword')
    job_position_input.send_keys(criteria['job_position'])
    job_position_input.send_keys(Keys.RETURN)

    resumes = driver.find_elements(By.CLASS_NAME, 'f-vacancylist-vacancyblock')
    for resume in resumes:
        job_position = resume.find_element(By.CLASS_NAME, 'card-title').text
        cursor.execute(
            "INSERT INTO resumes (job_position, years_of_experience, skills, location, salary_expectation) VALUES (?, ?, ?, ?, ?)",
            (job_position, criteria['years_of_experience'], criteria['skills'], criteria['location'],
             criteria['salary_expectation']))

    driver.quit()


search_criteria = {
    'job_position': 'Data Scientist',
    'years_of_experience': 2,
    'skills': 'Python, Machine Learning',
    'location': 'Kyiv',
    'salary_expectation': 'Negotiable'
}

parse_work_ua(search_criteria)
parse_robota_ua(search_criteria)

conn.commit()
conn.close()

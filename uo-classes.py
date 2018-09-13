import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



json_data = open("credentials.json").read()
REQUEST = json.loads(json_data)
TERM = "Fall 2018"


driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")

driver.get("https://duckweb.uoregon.edu/")

username = driver.find_element_by_id("UserID")
password = driver.find_element_by_name("PIN")

username.send_keys(REQUEST['username'])
password.send_keys(REQUEST['password'])
password.send_keys(Keys.RETURN)


driver.find_element_by_name("DW- Student Menu Link").click()
driver.find_element_by_link_text("Registration Menu").click()
driver.find_element_by_link_text("Search for Open Classes").click()

term_selector = (Select(driver.find_element_by_id("term_input_id")), driver.find_element_by_id("term_input_id"))
term_selector[0].select_by_visible_text(TERM)
term_selector[1].send_keys(Keys.RETURN)

subject_selector = Select(driver.find_element_by_id("subj_id"))
subject_selector.select_by_visible_text(REQUEST['subject'])

course_number = driver.find_element_by_name("sel_crse")
course_number.send_keys(REQUEST['course_number'])

if driver.find_element_by_id("sel_open_id").is_selected():
    driver.find_element_by_id("sel_open_id").click()

driver.find_element_by_name("SUB_BTN").click()

tbody = driver.find_elements_by_tag_name('tbody')[5]
trs = tbody.find_elements_by_tag_name('tr')[3:]

for tr in trs:
    rem = tr.find_elements_by_tag_name('td')[8].text
    if rem == '0':
        print("No seats remaining.")
    else:
        print("{} seats remaining. Registering...".format(rem))
        td = tr.find_elements_by_tag_name('td')[0]
        checkbox = td.find_element_by_name('sel_crn').click()
        driver.find_element_by_xpath("//input[@value='Register']").click()
        break


driver.close()

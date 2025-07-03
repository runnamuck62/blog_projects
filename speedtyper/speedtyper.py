from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


url = "https://www.typing.com/student/typing-test/1-minute"

driver = webdriver.Chrome()
driver.get(url)

sleep(5)

actions = ActionChains(driver)
actions.send_keys(Keys.ENTER)
actions.perform()

sleep(5)




while True:
    words = []
    elem = driver.find_elements(By.CLASS_NAME, "screenBasic-word")
    for word in elem:
        words.append(word.text)

    fixed_words = []
    for word in words:
        fixed_word = word.replace('\n', '')
        fixed_words.append(fixed_word)
    
    filtered_list = list(filter(None,fixed_words))

    
    for word in filtered_list:
        for char in word:
            actions.send_keys(char)
            actions.perform()
    


    print(filtered_list)









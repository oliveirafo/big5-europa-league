from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from time import sleep
from sys import exit
from pyautogui import alert
from os import popen as cmd

url = "https://fbref.com/pt/comps/Big5/Maiores-5-Ligas-Europeias-Estatisticas"
big5_list1 = []
big5_list2 = []
file_name = "result"

option = Options()
#option.add_argument("--headless")
option.add_argument('--disable-notifications')
browser = webdriver.Chrome(options=option)
browser.implicitly_wait(60)
browser.maximize_window()

browser.get(url)

page = browser.find_element(By.CSS_SELECTOR, 'body')
page.send_keys(Keys.PAGE_DOWN)

counter = 1
for i in range(20):
    pos = browser.find_element(By.XPATH, f'//*[@id="big5_table"]/tbody/tr[{counter}]/td[3]') 
    status = browser.find_element(By.XPATH, f'//*[@id="big5_table"]/tbody/tr[{counter}]/td[17]/div/div[5]')
    
    if ('1' in pos.text):
        club1 = browser.find_element(By.XPATH, f'//*[@id="big5_table"]/tbody/tr[{counter}]/td[1]') 
        big5_list1.append(club1.text)
        
    if '2' in pos.text:
        club2 = browser.find_element(By.XPATH, f'//*[@id="big5_table"]/tbody/tr[{counter}]/td[1]')
        big5_list2.append(club2.text)
    counter += 1

big_list_top_10 = big5_list1 + big5_list2
print(big_list_top_10)

for i in range(len(big_list_top_10)):
    browser.get( "https://www.sofascore.com/" )
    
    # click search
    search = browser.find_element(By.CSS_SELECTOR, '#__next > header > div.sc-2bdca2a8-0.sc-2bdca2a8-1.fywVif.jJUevR > div > div:nth-child(2) > div > form > input')
    search.click()

    # write search
    searchBar = browser.find_element(By.XPATH, '//*[@id="__next"]/header/div[1]/div/div[2]/div/form/input')
    searchBar.send_keys(big_list_top_10[0])

    # click club
    click_club = browser.find_element(By.CSS_SELECTOR, '#__next > header > div.sc-2bdca2a8-0.sc-2bdca2a8-1.fywVif.jJUevR > div > div:nth-child(2) > div > div > div > div:nth-child(1) > div:nth-child(1) > a > div > div > span')
    click_club.click()

    # select rivals
    rivals = browser.find_element(By.CSS_SELECTOR, '#__next > main > div > div.sc-e1b60555-0.hBrWcV > div > div.sc-e5255230-0.hLaBJu > div:nth-child(3) > div > div > div.sc-e5255230-0.hLaBJx.widget-wrapper > div > div:nth-child(1) > div > div.sc-91853a61-1.ijwGxS > a').text
    date = browser.find_element(By.CSS_SELECTOR, '#__next > main > div > div.sc-e1b60555-0.hBrWcV > div > div.sc-e5255230-0.hLaBJu > div:nth-child(3) > div > div > div.sc-e5255230-0.hLaBJx.widget-wrapper > div > div:nth-child(1) > div > div.sc-91853a61-1.ijwGxS > div.sc-cd4cfbdc-0.sc-b723fb41-0.hDkGff.jZkdkT > div.sc-492bf320-0.sc-b723fb41-3.hoXqpI.UDEqg.u-tC > span').text
    
    # remove clube da lista
    big_list_top_10.remove(big_list_top_10[0])

    # convert temp list to string
    list_to_string = ','.join(big_list_top_10).strip('[]')

    # verify rival are not list
    if rivals not in list_to_string:
        try:
            with open(f"{file_name}.txt", "a") as result:
                result.write(f"{rivals} - {date} \n")
        except Exception as e:
            alert("Erro ao acessar arquivo \n", e ) 
            exit()
    
    print(f"{big_list_top_10} possui {len(big_list_top_10)} times para ser analisados" )
    
cmd(f"start {file_name}.txt")
exit()

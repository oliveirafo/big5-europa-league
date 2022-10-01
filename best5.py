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

# -- URL DO PRIMEIRO SITE PESQUISADO
url = "https://fbref.com/pt/comps/Big5/Maiores-5-Ligas-Europeias-Estatisticas"

# -- LISTAS PARA ARMAZENAMENTO DE DADOS
big5_list1 = []
big5_list2 = []
big5_table_ppj1 = []
big5_table_ppj2 = []

# -- NOME DO ARQUIVO DE TEXTO
file_name = "result"

# -- CONTADOR DE JOGOS EM CASA
counter_home = 0

# -- AGUARDA A PAGINA SER CA
def pageDown():
    page = browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)

# -- PROCURA ELEMENTO POR SELETOR CSS
def search_css_selector(selector):
    results = browser.find_element(By.CSS_SELECTOR, selector)
    return results

# -- PROCURA ELEMENTO POR XPATH
def search_xpath(xpath):
    results = browser.find_element( By.XPATH, xpath )
    return results

# -- INSTANCIAS E INICIALIZADOR DE NAVEGADOR
option = Options()
option.add_argument('--disable-notifications')
browser = webdriver.Chrome(options=option)
browser.implicitly_wait(300)
browser.maximize_window()
browser.get(url)

# CONTADOR DE EVENTOS DO FOR PARA BUSCAR OS 10 MELHORES CLUBES
counter = 1
print('Buscando clubes da lista')
for i in range(20):
    
    pos = search_xpath(f'//*[@id="big5_table"]/tbody/tr[{counter}]/td[3]')
    status = search_xpath(f'//*[@id="big5_table"]/tbody/tr[{counter}]/td[17]/div/div[5]')
    
    if '1' in pos.text:
        club1 = search_xpath(f'//*[@id="big5_table"]/tbody/tr[{counter}]/td[1]') 
        big5_list1.append(club1.text)
        ppj1 = search_xpath(f'//*[@id="big5_table"]/tbody/tr[{counter}]/td[12]')
        big5_table_ppj1.append(ppj1.text)
        
    elif '2' in pos.text:
        club2 = search_xpath(f'//*[@id="big5_table"]/tbody/tr[{counter}]/td[1]')
        big5_list2.append(club2.text)
        ppj2 = search_xpath(f'//*[@id="big5_table"]/tbody/tr[{counter}]/td[12]')
        big5_table_ppj2.append(ppj2.text)
        
    counter += 1

big_list_top_10 = big5_list1 + big5_list2
ppj_top_10 = big5_table_ppj1 + big5_table_ppj2

print(f"{big_list_top_10}")
print(f"{ppj_top_10}")

for i in range(len(big_list_top_10)):
    
    # -- INICIALIZA VARIÁVEIS
    date = ''
    team = big_list_top_10[0]
    home_away = []
    ppj_team = 0.0
    list_to_string = ''
    
    # -- ACESSA SITE SOFASCORE
    browser.get( "https://www.sofascore.com/" )
    
    
    # CLICA NA BARRA DE PESQUISA
    search = search_css_selector( '#__next > header > div.sc-2bdca2a8-0.sc-2bdca2a8-1.fywVif.jJUevR > div > div:nth-child(2) > div > form > input' )
    search.click()
    search.clear()
    
    # -- ESCREVE NA BARRA DE PESQUISA
    searchBar = search_css_selector('#__next > header > div.sc-2bdca2a8-0.sc-2bdca2a8-1.fywVif.jJUevR > div > div:nth-child(2) > div > form > input')
    searchBar.send_keys(big_list_top_10[0])

    sleep(1)

    # -- SELECIONANDO O CLUBE PESQUISADO
    click_club = search_css_selector('#__next > header > div.sc-2bdca2a8-0.sc-2bdca2a8-1.fywVif.jJUevR > div > div:nth-child(2) > div > div > div > div:nth-child(1) > div:nth-child(1) > a > div > div > span')
    click_club.click()

    # -- SELECIONANDO O CONFRONTO
    match = search_css_selector('#__next > main > div > div.sc-e1b60555-0.hBrWcV > div > div.sc-e5255230-0.hLaBJu > div:nth-child(3) > div > div > div.sc-e5255230-0.hLaBJx.widget-wrapper > div > div:nth-child(1) > div > div.sc-91853a61-1.ijwGxS > a')
    
    # -- VERIFICANDO A DATA DA PROXIMA PARTIDA
    date_remaing = search_css_selector('#__next > main > div > div.sc-e1b60555-0.hBrWcV > div > div.sc-e5255230-0.hLaBJu > div:nth-child(3) > div > div > div.sc-e5255230-0.hLaBJx.widget-wrapper > div > div:nth-child(1) > div > div.sc-91853a61-1.ijwGxS > div.sc-cd4cfbdc-0.sc-b723fb41-0.hDkGff.jZkdkT > div.sc-492bf320-0.sc-b723fb41-3.hoXqpI.UDEqg.u-tC > span')
    
    if 'day' in str(date_remaing.text):
        date = date_remaing.text
    elif 'morrow' in str(date_remaing.text):
        date = 'Amanhã'
    else:
        date = f'O jogo será daqui a {date_remaing.text} horas'
    
    home_away = match.text.strip().split('-')
    
    if str(team) in str(home_away[0]) :
        home = 'Dentro de casa'
        counter_home += 1
    else:
        home = 'Fora de casa'
    
    # -- GUARDA O VALOR PONTOS POR JOGO (APROVEITAMENTO)
    ppj_team = float(ppj_top_10[0].replace(',','.'))
    
    # -- REMOVE O CLUBE PESQUISADO DA LISTA
    big_list_top_10.remove(big_list_top_10[0])
    
    # -- REMOVE O VALOR PONTOS POR JOGO DA LISTA PPJ
    ppj_top_10.remove(ppj_top_10[0])

    # -- CONVERTE LISTA PARA STRING
    list_to_string = ','.join(big_list_top_10).strip('[]')
    
    # -- VERIFICA SE O OPONENTE NÃO ESTÁ NA LISTA DE CONFRONTO
    if match.text not in list_to_string:
        try:
            with open(f"{file_name}.txt", "a") as file:
                file.write(f'-> {match.text} \n-> {date} \n-> Jogando: {home} \n-> {team} aproveitamento: {round(ppj_team / 3 * 100, 2)}% \n\n')
                file.write("-----------------------------------------------\n\n")
        except Exception as e:
            alert("Erro ao acessar arquivo")
            print(e)
            exit()
    
    print(f"Pesquisando {len(big_list_top_10)} clubes restantes -> {big_list_top_10}" )
    
with open(f'{file_name}.txt', 'a') as file:
    file.write(f'-> Total de jogos dentro de casa: {counter_home} \n')

# -- ABRE ARQUIVO DE TEXTO APÓS GRAVAR TODOS OS DADOS
cmd(f"start {file_name}.txt")
exit()

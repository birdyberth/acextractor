from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import os
import time
import math

if __name__ == "__main__":
    #listcom = parsexml('ytcomments/ytcomments1nov2017.xml')
    #out = comsorter(listcom)
    #htmlout(out)
    
    profile = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(firefox_profile=profile)
    wait = WebDriverWait(driver, 3600)
    driver.get("https://www.youtube.com")
    continuer = input('Continue-tu? (o/n)')
    while continuer != 'n':
        dirName = os.getcwd()
        fileadress = "file://" + dirName + "/commentaires_tries.html"
        driver.get(fileadress)
        textofind = input('Commentaire à trouver :')
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'ytp-play-button')))
        time.sleep(4)
        element.click() #met la video en pause
        driver.execute_script("window.scrollTo(0, 200);") #descend pour activer le chargement des commentaires
        time.sleep(3);
        no = driver.find_elements_by_css_selector('yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer')
        if len(no) > 0: #si les commentaires sont actives
            no = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer'))).text #a changer mais pour l'instant cette commande fonctionne bien pour extraire le texte de la string des commentaires
            nbcom = no[0]
            i = 1
            number = 0
            while no[i] != ' ':
                if no[i] != ',':
                    nbcom = nbcom + no[i]
                i = i + 1

            number = int(math.ceil(float(nbcom)/20)) #convertit la string en nombre (il y a 20 commentaires visibles par loading)

            if number > 0: #s'il y a des commentaires
                #loade tous les commentaires
                lastscrollposition = 0
                lastlastscrollposition = 0
                for i in range(1, number):
                    driver.execute_script("window.scrollTo(0, 1000000000);") #il y a un bug dans firefox qui empeche d'utiliser le scroll to bottom
                    source = driver.page_source
                    if textofind in source:
                        break
                    scrollposition = driver.execute_script("return window.pageYOffset;")
                    if scrollposition == lastlastscrollposition:
                        break
                    lastlastscrollposition = lastscrollposition
                    lastscrollposition = scrollposition
                    time.sleep(2) 
        continuer = input('Continue-tu? (o/n)')

from requestium import Session, Keys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
from os.path import join
import platform
import json
import hashlib
import hmac
import time
import six.moves.urllib as urllib
from tqdm import tqdm
from API import API


def findPathForDriver():
    lookfor = "chromedriver.exe" if platform.system() == "Windows" else "chromedriver"
    placeWhereToStart = "C:\\" if platform.system() == "Windows" else "/"
    for root, dirs, files in os.walk(placeWhereToStart):
        if lookfor in files:
            return join(root, lookfor)
            

def generate_device_id(seed):
    volatile_seed = "12345"
    m = hashlib.md5()
    m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
    return 'android-' + m.hexdigest()[:16]
 
def generate_UUID(uuid_type):
    import uuid
    generated_uuid = str(uuid.uuid4())
    if uuid_type:
        return generated_uuid
    else:
        return generated_uuid.replace('-', '')
 
def get_seed(*args):
    m = hashlib.md5()
    m.update(b''.join([arg.encode('utf-8') for arg in args]))
    return m.hexdigest()

def login():
    global api
    api.s.driver.get("https://www.instagram.com/accounts/login")
    time.sleep(2)
    api.s.driver.find_element_by_xpath("//*[@name='username']").send_keys("insert username")
    api.s.driver.find_element_by_xpath("//*[@name='password']").send_keys("insert password")
    api.s.driver.find_element_by_xpath("//span/button").click()
    time.sleep(2)
    print("LOGIN EFFETTUATO CON SUCCESSO. AVVIO DEL LOGGER....")


def scrapeAccountName():
    global api
    return api.s.driver.find_element_by_xpath("//*[@class='_ienqf']").text.split('\n')[0]

def scrapeFollowersFromAnAccount(mode="followers"):
    """Temporary - Will be more generic"""
    global api
    api.s.driver.get("https://www.instagram.com/petrarcarugby")
    usernameToLook = scrapeAccountName() #Perché l'idea è che, cercando per hashtag, voglia fare lo scraping di un utente qualsiasi
    api.s.transfer_driver_cookies_to_session()
    usernameToLook = api.castUsernameToUserID(usernameToLook) #Idem del commento precedente
    username = "narutosama123"
    password = "gundam123"
    device_id = generate_device_id(get_seed(username, password))
    uuid = generate_UUID(True)
    rank_token = "{}_{}".format(usernameToLook, uuid)
    return api.getUserFollowers(usernameToLook, rank_token, selection=mode)

def scrapeFollowingFromAnAccount():
    """Temporary - will be more generic"""
    global api


def executeLikesOnPhotos(quantity):
    """Da generalizzare, per ora mette like solo sulla griglia globale"""
    global api
    x = 0 
    time.sleep(2)
    element = api.s.driver.find_element_by_xpath("//*[contains(@href, '/?tagged=rugby')]")
    element.click()
    while x != int(quantity):
        #elements = context.webdriver.find_elements_by_xpath("//*[@class='_mck9w _gvoze _tn0ps']")
        time.sleep(2)
        try:
            api.s.driver.find_element_by_css_selector(".coreSpriteHeartOpen").click()
            api.logger.info("Inserito like alla foto con successo")
            followUser()
            #Inserire funzione di follow qui
        except Exception:
            api.logger.error("Il like sulla foto non è stato inserito. Forse era già presente? Proseguo...")
            ActionChains(api.s.driver).send_keys(Keys.RIGHT).perform()
            continue
        x+=1
        ActionChains(api.s.driver).send_keys(Keys.RIGHT).perform()
        time.sleep(2)
 
def followUser(userToFollow = None):
    global api
    #import inspect
    #userToFollow = inspect.stack()[1][3]
    if userToFollow is None:
        userToFollow = api.s.driver.find_element_by_xpath("//*[contains(@class,'notranslate')]").text
    api.s.driver.execute_script('''window.open("about:blank", "_blank");''')
    api.logger.info("Apro una nuova finestra per seguire l'utente")
    api.s.driver.switch_to.window(api.s.driver.window_handles[-1])
    api.logger.info("Switchato correttamente il focus alla nuova finestra. Carico la pagina...")
    api.s.driver.get("https://www.instagram.com/"+userToFollow)
    time.sleep(1)
    try:
        api.s.driver.find_element_by_xpath("//*[contains(text(), 'Follow')]").click()
        time.sleep(1.5)
        api.logger.info("Utente " + userToFollow + " seguito con successo. Chiusura in corso di questo tab e switch al precedente")
        api.s.driver.execute_script("close();")
        api.s.driver.switch_to.window(api.s.driver.window_handles[-1])
    except Exception:
        api.logger.warning("Impossibile seguire " +userToFollow + ". Forse si sta già seguendo quest'utenza?")

def insertComment():
    """Should add a way to insert more 'not-bot-like' comments"""
    global api
    api.s.driver.find_element_by_xpath("//*[@class='_bilrf']").send_keys("💪🏻")
    api.s.driver.find_element_by_xpath("//*[@class='_bilrf']").send_keys(Keys.ENTER)

def testStories():
    global api
    api.s.transfer_driver_cookies_to_session()
    toSee = api.seeStories()
    with open("savedJson.txt", "w") as f:
        import json
        f.write(json.dumps(toSee, indent=2))
    print("Fatto")


def findConnections(userToLookForConnections):
    """Basta semplicemente prendere l'user da input e vedere se ha giocato per qualche squadra"""
    import json
    with open("filter.json", "r") as opened:
        filtering = json.load(opened) #Filtro che contiene tutti i giocatori di eccellenza dal 2017 al 2011. Type: DICT
    for teamName, squadList in filtering.items():
        if userToLookForConnections in squadList:
            print("ciao")
            #crea arco
    return None
          


if __name__ == "__main__":
    """ Come testare la aggiunta di nodi: apro i following di un account che ho (rugbyrovigodelta), 
    Per ogni follower x nel file: 
        G.findConnections(x)
    """
    path = findPathForDriver()
    api = API(path)
    print("BENVENUTO SU INSTASCRIPT.")
    login()
    #testStories()
    testing = scrapeFollowersFromAnAccount(mode="followers")
    api.saveScrapedFollowers()
    #testing = scrapeFollowersFromAnAccount(mode="following")
    #api.saveScrapedFollowing()
    #print(testing)
    #api.s.transfer_session_cookies_to_driver()
    #time.sleep(2)
    #api.s.driver.get("https://www.instagram.com/explore/tags/rugby")
    #executeLikesOnPhotos(3)
    #api.getUsernameFromID(402819190)
    #print(api.users)

    ##END FOR NOW

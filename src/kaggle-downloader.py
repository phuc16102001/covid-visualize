from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

username = "phuc16102001"
password = "@Phuc16102001"
email = f"{username}@gmail.com"
driverPath = "P:\chrome-driver\chromedriver.exe"

baseURL = "https://www.kaggle.com"
loginPath = f"{baseURL}/account/login"
homePath = f"{baseURL}"
notebookPath = f"{baseURL}/code/{username}/data-crawl-covid-worldometer"
codePath = f"{baseURL}/{username}/code"

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def loadDriver(url, timeout = 3):
    global driver

    driver.get(url)
    driver.implicitly_wait(timeout)
    driver.fullscreen_window()

def goToVersion():
    loadDriver(notebookPath)

    btnDot = driver.find_element(by=By.XPATH, value = "/html/body/main/div[1]/div/div[5]/div[2]/div[3]/div/div[1]/div/div[2]/button")
    btnDot.click()
    sleep(2)

    btnVersion = driver.find_element(by=By.XPATH, value = "/html/body/main/div[1]/div/div[1]/div[2]/ul/li[3]/div/p")
    btnVersion.click()
    sleep(2)

def downloadForVersion(url):
    loadDriver(url)

    btnData = driver.find_element(by=By.XPATH, value="/html/body/main/div[1]/div/div[5]/div[2]/div[5]/div[1]/div/div/div/button[2]")
    btnData.click()
    sleep(2)
    
    btnDot = driver.find_element(by=By.XPATH, value="/html/body/main/div[1]/div/div[5]/div[2]/div[6]/div[2]/div[2]/div/div[2]/div/div[2]/button")
    btnDot.click()
    sleep(2)

    popupBox = driver.find_element(by=By.CLASS_NAME, value="mdc-menu-surface--open")
    btnDownload = popupBox.find_element(by = By.XPATH, value="./ul/li[1]")
    btnDownload.click()
    sleep(2)

def login():
    loadDriver(loginPath)

    btnLoginEmail = driver.find_element(by=By.XPATH,value="/html/body/main/div[1]/div/div[2]/form/div[2]/div/div[2]/a/li/div")
    btnLoginEmail.click()

    inpUsername = driver.find_element(by=By.XPATH, value="/html/body/main/div[1]/div/div[2]/form/div[2]/div[1]/div/label/input")
    inpPassword = driver.find_element(by=By.XPATH,value="/html/body/main/div[1]/div/div[2]/form/div[2]/div[2]/div/label/input")
    btnLogin = driver.find_element(by=By.XPATH,value="/html/body/main/div[1]/div/div[2]/form/div[2]/div[3]/button")
    sleep(2)

    inpUsername.send_keys(email)
    inpPassword.send_keys(password)
    btnLogin.click()
    sleep(2)

def main():
    login()
    goToVersion()
    
    lsVersion = driver.find_elements(by=By.XPATH, value="/html/body/main/div[1]/div/div[1]/div/ul/a")
    lsVersionId = []
    for version in lsVersion:
        url = version.get_attribute('href')
        
        if (not('scriptVersionId' in url)):
            continue
        versionId = url[url.find('=')+1:]
        if (versionId in lsVersion):
            continue
        print(f"Hit...{versionId}")
        lsVersionId.append(versionId)

    print(f"Get in total {len(lsVersionId)} versions...")

    fromVersion = int(input("From version number: "))
    for idx in range(fromVersion, len(lsVersionId)):
        versionId = lsVersionId[idx]
        print(f"Crawl version {versionId}")
        downloadForVersion(f"{notebookPath}?scriptVersionId={versionId}")
    driver.quit()

if __name__=="__main__":
    main()
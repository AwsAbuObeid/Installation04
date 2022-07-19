from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW


path = "D:\program files\chromedriver.exe"
service = Service(path)
service.creationflags = CREATE_NO_WINDOW

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome('D:\program files\chromedriver.exe', options=options)

driver.get("https://statoshi.info/?orgId=1")
sleep(3)
content = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
index = content.find("graph-legend-value current")
index = content.find("graph-legend-value current", index + 28)
TPS = content[index + 28:index + 32]
driver.quit()
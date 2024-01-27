__maintainer__ = "Süli Tamara"
__version__ = "1.7"
__date__ = "2022.01.22."

import os
import plyer.platforms.win.notification
from plyer import notification
import dotenv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from subprocess import CREATE_NO_WINDOW, Popen

dotenv.load_dotenv()

### OPEN BROWSER ###

options = EdgeOptions()
options.add_argument('--headless')
service = Service(EdgeChromiumDriverManager().install())
service.creationflags = CREATE_NO_WINDOW
driver = Edge(service=service, options=options)
driver.headless = True
driver.get(r"https://teveclub.hu/")

### LOGIN ###

input_user = driver.find_element(By.NAME, 'tevenev')
input_user.send_keys(os.getenv("USER"))

input_pwd = driver.find_element(By.NAME, 'pass')
input_pwd.send_keys(os.getenv("PWD"))

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[src='/img_des/login_submit_46.gif'][type='image']"))).click()

if driver.current_url == "https://teveclub.hu/error.pet?code=wronglogin":
    notification.notify("Automateve - Hiba", "Hibás felhasználónév vagy jelszó!")
    quit()

### ETETÉS (1 étel és ital) ###

try:
    driver.find_element(By.CSS_SELECTOR, "input[name='etet'][type='submit']").click()
except NoSuchElementException:
    pass

### TANÍTÁS ###

driver.find_element(By.CSS_SELECTOR, '[alt="Tanítom a tevémet!"]').click()

try:
    driver.find_element(By.NAME, "tudomany")
    notification.notify("Automateve - Info", "Ideje ránézni a kis kedvencedre, megint tanult valami újat! :D")
    quit()

except NoSuchElementException:
    try:
        driver.find_element(By.NAME, "learn").click()
    except NoSuchElementException:
        notification.notify("Automateve - Info", "Ajaj, ma már tanult " + os.getenv("USER") + "! :(")

Popen("powershell -ExecutionPolicy bypass -File remove_us_input.ps1", shell=True)

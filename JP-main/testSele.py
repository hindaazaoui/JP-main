from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_one_of_xpaths(wait, xpaths):
    for xp in xpaths:
        try:
            el = wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
            el.click()
            return True
        except Exception:
            continue
    return False

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # décommenter si vous voulez tourner sans UI

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get("https://www.linkedin.com")
        wait = WebDriverWait(driver, 15)

        # cliquer sur "Refuser" pour les cookies (essaye plusieurs variantes)
        cookie_xpaths = [
            "//button[normalize-space(.)='Refuser']",
            "//button[contains(., 'Refuser')]",
            "//button[normalize-space(.)='Refuser les cookies']",
            "//button[contains(., 'Refuser les cookies')]",
            "//button[contains(., 'Decline')]"
        ]
        clicked = click_one_of_xpaths(wait, cookie_xpaths)
        # petite pause pour que l'UI se stabilise
        time.sleep(1)

        # Cliquer sur "S’identifier avec un e‑mail" d'après son xpath
        link = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section[1]/div/div/a")))
        link.click()
        time.sleep(2)  # attendre que la page se charge

        # ...existing code...
        time.sleep(2)  # attendre que la page se charge

        # Attendre et remplir le champ username
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.clear()
        username_field.send_keys("hind.aazaoui.pro@gmail.com")  # remplacer par votre email

        # Attendre et remplir le champ password
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.clear()
        password_field.send_keys("youpi123Ha")  # remplacer par votre mot de passe

        # Cliquer sur le bouton de connexion
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_button.click()


        # attendre quelques secondes pour voir l'effet
# ...existing code...

        # attendre quelques secondes pour voir l'effet
        time.sleep(5)

        # driver.get("https://www.google.com")
        # wait = WebDriverWait(driver, 15)
        # search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
        # search_box.clear()
        # search_box.send_keys("")
        # search_box.send_keys(Keys.ENTER)
        # # attendre quelques secondes pour voir les résultats
        # time.sleep(5)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
    
    

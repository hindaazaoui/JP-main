import json
import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from testSele import click_one_of_xpaths

# filepath: c:\Users\yeahh\Desktop\JP\testSele.py

personnes = [


        {"nom": "PROUST", "prenom": "Arthaud"},
        {"nom": "REBIERRE", "prenom": "Maxime"},
        {"nom": "REULIER", "prenom": "Mathéo"},
        {"nom": "REYNIER", "prenom": "Paul"},
        {"nom": "ROUX", "prenom": "Lyam"},
        {"nom": "SEDDIKI", "prenom": "Safiya"},
        {"nom": "SEZER", "prenom": "Florian"},
        {"nom": "SICARD-RAZAKA", "prenom": "Auriane-Mirana"},
        {"nom": "SIMONET", "prenom": "Olivia"},
        {"nom": "SUIRE", "prenom": "Peyo"},
        {"nom": "TELUSMA", "prenom": "Nehémia"},
        {"nom": "THIBAULT", "prenom": "Maxime"},
        {"nom": "VIVES", "prenom": "Clément"},
        {"nom": "WEGERA", "prenom": "Quentin"}
    ]

# ...existing code...

def traiter_profil(driver, wait, nom, prenom):
    """
    Traite un profil LinkedIn spécifique.
    Retourne un dictionnaire avec les informations extraites.
    """

     # encoder les espaces en %09
    nom_enc = nom.replace(' ', '%09')
    prenom_enc = prenom.replace(' ', '%09')

    # Construire l'URL de recherche en utilisant les valeurs encodées
    search_url = f"https://www.linkedin.com/search/results/all/?keywords={nom_enc}%09{prenom_enc}&origin=TYPEAHEAD_ESCAPE_HATCH"
    driver.get(search_url)
    
    print(f"Recherche de {nom} {prenom}...")
    time.sleep(2)  # attendre que la page se charge

    # Cliquer sur le premier profil
    first_profile = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//*[.//button[.//span[contains(normalize-space(.),'Message')]]]")))
    first_profile.click()

    # Extraire les informations d'expérience
    experience = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(., 'Expérience')]/following-sibling::div[1]")))
    
    lines = experience.text.split('\n')
    if len(lines) >= 7:
        third_line = lines[2]
        localisation = lines[6]
        entreprise = third_line.split('·')[0].strip()
        contrat = third_line.split('·')[1].strip()

        # Retourner les informations extraites
        return {
            "nom": nom,
            "prenom": prenom,
            "entreprise": entreprise,
            "contrat": contrat,
            "localisation": localisation
        }

    else : 
        # Retourner les informations vides
        return {
            "nom": "",
            "prenom": "",
            "entreprise": "",
            "contrat": "",
            "localisation": ""
        }

def save_cookies(driver, filename):
    with open(filename, 'w') as file:
        json.dump(driver.get_cookies(), file)

def load_cookies(driver, filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1024,768")
    options.add_argument("--window-position=0,0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:

        # CONNEXION
        ##############################
        driver.get("https://www.linkedin.com")
        # driver.get("https://www.linkedin.com/search/results/all/?keywords=ABADIE%09Samuel&origin=TYPEAHEAD_ESCAPE_HATCH")
        wait = WebDriverWait(driver, 15)

        # # cliquer sur "Refuser" pour les cookies (essaye plusieurs variantes)
        # cookie_xpaths = [
        #     "//button[normalize-space(.)='Refuser']",
        #     "//button[contains(., 'Refuser')]",
        #     "//button[normalize-space(.)='Refuser les cookies']",
        #     "//button[contains(., 'Refuser les cookies')]",
        #     "//button[contains(., 'Decline')]"
        # ]
        # clicked = click_one_of_xpaths(wait, cookie_xpaths)
        # # petite pause pour que l'UI se stabilise
        # time.sleep(1)

        # Charger les cookies si le fichier existe
        load_cookies(driver, 'cookies.json')
        driver.refresh()  # Rafraîchir la page pour appliquer les cookies

        # Test si on est connecté
        if "feed" not in driver.current_url:  # Vérifiez si l'URL de la page d'accueil LinkedIn est chargée

            # Si non connecté, procéder à la connexion
            print("Not logged in, proceeding to login.")

            # Cliquer sur "S’identifier avec un e‑mail" d'après son xpath
            link = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section[1]/div/div/a")))
            link.click()
            time.sleep(2)  # attendre que la page se charge

            # Remplir le champ username
            username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
            username_field.clear()
            username_field.send_keys("karofe8446@fergetic.com")  

            # Remplir le champ password
            password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
            password_field.clear()
            password_field.send_keys("testlinkedindata") 
            # (+254700927362)

            # Cliquer sur le bouton de connexion
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
            login_button.click()

            # Attendre que la connexion soit effectuée
            wait.until(EC.url_contains("feed")) 

            # Sauvegarder les cookies après la connexion
            save_cookies(driver, 'cookies.json')
            print("Login successful and cookies saved.")
        else:
            print("Already logged in.")
        


        try:
            # Ouvrir le CSV en écriture et écrire l'en-tête
            with open('result.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['nom','prenom','entreprise','contrat','localisation'])


                # Pour chaque personne dans le tableau
                for personne in personnes:
                    print(f"{personne['nom']},{personne['prenom']}", end='')
                    
                    info = traiter_profil(driver, wait, personne['nom'], personne['prenom'])
                    
                    # Afficher les résultats
                    print("\nInformations extraites:")
                    print(f"Entreprise: {info['entreprise']}")
                    print(f"Contrat: {info['contrat']}")
                    print(f"Localisation: {info['localisation']}")
                    print(f"{info.get('entreprise','')},{info.get('contrat','')},{info.get('localisation','')}")

                    
                    # Écrire une seule ligne CSV pour cette personne
                    writer.writerow([
                        personne['nom'],
                        personne['prenom'],
                        info.get('entreprise', ''),
                        info.get('contrat', ''),
                        info.get('localisation', '')
                    ])
                    csvfile.flush()  # assurer l'écriture immédiate
                    
                    # Ajouter une pause entre chaque recherche pour éviter les limitations
                    time.sleep(5)
                    
        finally:
            driver.quit()
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

    
import time
import requests
from selenium import webdriver
import chromedriver_autoinstaller

# Installez automatiquement la version compatible du pilote Chrome
chromedriver_autoinstaller.install()


PSEUDO = "Le Mans"

HEADERS = {
    "accept": "*/*",
    "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest"
}

MAGIC_ANSWER_ID = 385

# Définition de la fonction updateDuJeu
def sendRequest(url: str, headers: dict, data: dict) -> requests.Response:
    """Envoie une requête POST et retourne la réponse"""
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response
    exit("Erreur lors de la requête")
    


def initGame() -> int:
    """Initialise le jeu et retourne l'identifiant du joueur"""
    url = "https://escapeforge.fr/ajax/start_game.php"

    data = {
        "pseudo": PSEUDO,
        "idGame": "26"
    }

    response = sendRequest(url, HEADERS, data)
    return int(response.text)



def getGameStatus(user_id: int) -> requests.Response:
    """Récupère le statut du jeu et retourne un dictionnaire"""
    url = "https://escapeforge.fr/ajax/get_current_step.php"

    data = {
        "idJoueurPartie": user_id,
        "idGame": "26"
    }

    response = sendRequest(url, HEADERS, data)
    return response

def sendNextStep(user_id: int, nextStepId: int) -> requests.Response:
    """Envoie un setnextstep et retourne la réponse"""
    url = "https://escapeforge.fr/ajax/set_next_step.php"

    data = {
        "idJoueurPartie": user_id,
        "idGame": "26",
        "nextStepId": nextStepId
    }

    response = sendRequest(url, HEADERS, data)
    return response

def sendAnswer(user_id: int) -> requests.Response:
    return sendNextStep(user_id, MAGIC_ANSWER_ID)

def sendAction(user_id: int) -> requests.Response:
    return sendNextStep(user_id, "")


def getClassement(user_id: int) -> requests.Response:
    """Accède à la page de classement et retourne la réponse"""
    url = "https://escapeforge.fr/classement.php"

    data = {
        "idGame": "26",
        "idJoueurPartie": user_id
    }

    response = sendRequest(url, HEADERS, data)
    return response

### Début du script ###
timingToWin = -1
while timingToWin <= 15:
    timingToWin = int(input("Entrez le délai pour win (en secondes) > 15: "))

# Initialisez le navigateur Selenium
driver = webdriver.Chrome()

# Accédez à la page d'accueil
driver.get("https://escapeforge.fr/initGame.php?idGame=26")


# Initialisation du jeu
user_id = initGame()

print(f"Identifiant du joueur: {user_id}")

getGameStatus(user_id)

# Envoi de la réponse
sendAnswer(user_id).text


for i in range(timingToWin):
    print(f"Attente de {timingToWin-i} secondes avant le score")
    time.sleep(1)

# Récupération du statut du jeu
print(getGameStatus(user_id).text)
print("-"*50)


# Renvoie d'un setnextstep
sendAction(user_id)

# Récupération du statut du jeu
getGameStatus(user_id).text
print("-"*50)

classement_response = getClassement(user_id)

driver.get("data:text/html;charset=utf-8," + classement_response.text)

# Ajout d'un délai pour afficher la réponse
time.sleep(60)

# Fermez le navigateur
driver.close()
exit(0)


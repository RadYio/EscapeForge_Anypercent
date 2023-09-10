import time
import requests
from selenium import webdriver
import chromedriver_autoinstaller

# Automatically install the compatible Chrome driver version
chromedriver_autoinstaller.install()

# Your pseudo (user name)
PSEUDO = "Le Mans"

# Headers for HTTP requests
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

# The magic answer ID
MAGIC_ANSWER_ID = 385

# Function to send an HTTP POST request and return the response
def sendRequest(url: str, headers: dict, data: dict) -> requests.Response:
    """Send an HTTP POST request and return the response"""
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response
    exit("Error during the request")

# Function to initialize the game and return the player's ID
def initGame() -> int:
    """Initialize the game and return the player's ID"""
    url = "https://escapeforge.fr/ajax/start_game.php"

    data = {
        "pseudo": PSEUDO,
        "idGame": "26"
    }

    response = sendRequest(url, HEADERS, data)
    return int(response.text)

# Function to get the game status and return it as a response
def getGameStatus(user_id: int) -> requests.Response:
    """Get the game status and return it as a response"""
    url = "https://escapeforge.fr/ajax/get_current_step.php"

    data = {
        "idJoueurPartie": user_id,
        "idGame": "26"
    }

    response = sendRequest(url, HEADERS, data)
    return response

# Function to send the next step and return the response
def sendNextStep(user_id: int, nextStepId: int) -> requests.Response:
    """Send the next step and return the response"""
    url = "https://escapeforge.fr/ajax/set_next_step.php"

    data = {
        "idJoueurPartie": user_id,
        "idGame": "26",
        "nextStepId": nextStepId
    }

    response = sendRequest(url, HEADERS, data)
    return response

# Function to send an answer and return the response
def sendAnswer(user_id: int) -> requests.Response:
    """Send an answer and return the response"""
    return sendNextStep(user_id, MAGIC_ANSWER_ID)

# Function to send an action and return the response
def sendAction(user_id: int) -> requests.Response:
    """Send an action and return the response"""
    return sendNextStep(user_id, "")

# Function to get the ranking and return the response
def getClassement(user_id: int) -> requests.Response:
    """Access the ranking page and return the response"""
    url = "https://escapeforge.fr/classement.php"

    data = {
        "idGame": "26",
        "idJoueurPartie": user_id
    }

    response = sendRequest(url, HEADERS, data)
    return response

### Start of the script ###
timingToWin = -1
while timingToWin <= 15:
    timingToWin = int(input("Enter the winning delay (in seconds) > 15: "))

# Initialize the Selenium browser
driver = webdriver.Chrome()

# Go to the homepage
driver.get("https://escapeforge.fr/initGame.php?idGame=26")

# Initialize the game
user_id = initGame()

print(f"Player ID: {user_id}")

getGameStatus(user_id)

# Send the answer
sendAnswer(user_id).text

for i in range(timingToWin):
    print(f"Waiting for {timingToWin-i} seconds before scoring")
    time.sleep(1)

# Get the game status
getGameStatus(user_id)

# Send an action
sendAction(user_id)

# Get the game status
getGameStatus(user_id)

# Get the ranking response
classement_response = getClassement(user_id)

# Display the ranking in the browser
driver.get("data:text/html;charset=utf-8," + classement_response.text)

# Add a delay to display the response
time.sleep(60)

# Close the browser
driver.close()
exit(0)

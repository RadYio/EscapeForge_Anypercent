import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import random as rd

# Automatically install the compatible Chrome driver version
chromedriver_autoinstaller.install()

# Your pseudo (user name)
PSEUDO = "Angers"

# Maximum timing to win (in seconds)
TIMING_TO_WIN_MAX = 14
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
timingToWin = 14
while timingToWin < TIMING_TO_WIN_MAX:
    timingToWin = int(input("Enter the winning delay (in seconds) >= " + str(TIMING_TO_WIN_MAX) + ": "))

def generateAWin() -> None:

    # Create Chrome options to disable debug message
    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # Initialize the Selenium browser
    driver = webdriver.Chrome(options=chrome_options)

    # Go to the homepage
    driver.get("https://escapeforge.fr/initGame.php?idGame=26")

    # Initialize the game
    user_id = initGame()

    getGameStatus(user_id)

    # Send the answer
    sendAnswer(user_id).text

    # Wait for the winning delay
    time.sleep(timingToWin)

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

    # HTML parsing with BeautifulSoup
    soup = BeautifulSoup(classement_response.text, 'html.parser')

    # Select the part you want to extract using CSS selector
    result = soup.select_one('.card-footer .text-light')

    # Display the result
    if result:
        print("user_id: " + str(user_id) + " just won in " + result.get_text())

    # Add a delay to display the response
    time.sleep(3)

    # Close the browser
    driver.close()

# Start a thread pool with a maximum of 4 threads
max_threads = 4
with ThreadPoolExecutor(max_threads) as executor:
    
    for _ in range(int(rd.uniform(15, 25))):
        time.sleep(rd.uniform(1, 5))
        executor.submit(generateAWin)

exit(0)

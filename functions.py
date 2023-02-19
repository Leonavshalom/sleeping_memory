import requests
import json
import logging
import base64
import requests
from urllib.parse import urlencode
import base64
import webbrowser
from base64 import urlsafe_b64encode



# Load the credentials
with open("credentials.json") as f:
    config = json.load(f)
spotify_cred = config["spotify"][0]



# Encode the credentials
def encode_credentials():
    client_secret = spotify_cred["client_secret"]
    client_id = spotify_cred["client_id"]
    message = f"{client_id}:{client_secret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    encoded_credentials = base64Bytes.decode('ascii')
    return encoded_credentials


# Define the logger
def setup_logger(logger_name, log_file="/tmp/sleeping_memory.log", level=logging.INFO):
    # create a logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    
    # create a file handler
    handler = logging.FileHandler(log_file)
    handler.setLevel(level)
    
    # create a logging format
    formatter = logging.Formatter('%(asctime)s | [%(levelname)s] | %(message)s',
                                  datefmt='%b %d %H:%M:%S')
    handler.setFormatter(formatter)
    
    # add the handlers to the logger
    logger.addHandler(handler)
    
    return logger


# Get recent Spotify tracks
def get_spotify_recent():
    logger = setup_logger(logger_name="get_spotify_recent")

    # Get the token
    try:
        token = get_spotify_token()
    except Exception as e:
        logger.error("Spotify token request failed with exception: {exception}".format(exception=e))
        print("Spotify token request failed with exception: {exception}".format(exception=e))
        return None
    
    # Define the endpoint
    url = "https://api.spotify.com/v1/me/player/recently-played"
    # Define the headers
    headers = {
    "Authorization": f"Bearer {token}"
    }

    # Define the parameters
    params = { 
        "limit": 50
    }
    # print(json.dumps(headers,indent=4))
    # print(json.dumps(params,indent=4))

    # Make the request
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Spotify playlist request failed with status code: {code}".format(code=response.status_code))
            print("Spotify playlist request failed with status code: {code}".format(code=response.status_code))
            print(response.json())
            return None
    except Exception as e:
        logger.error("Spotify request failed with exception: {exception}".format(exception=e))
        print("Spotify request failed with exception: {exception}".format(exception=e))
        return None


# Get Spotify token
def user_authorization():
    client_id = spotify_cred["client_id"]
    redirect_uri = "https%3A%2F%2Flocalhost%3A8080%2Fcallback"
    scope = "user-read-recently-played user-library-read"
    webbrowser.open(f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}")
    print("Access granted. Please copy the code from the URL and paste it here.")


# Get Spotify token
def get_spotify_token():
    logger = setup_logger(logger_name="get_spotify_token")


    encoded_credentials = encode_credentials()
    token_headers = {
        "Authorization": "Basic {}".format(encoded_credentials)
    }

    token_data = {
        "grant_type": "client_credentials",
        "code" : "",
        "redirect_uri": "https://localhost:8080/callback"
    }

    user_authorization()
    code = input("Enter the code: ")
    token_data["code"] = code

    print(json.dumps(token_headers,indent=4))
    print(json.dumps(token_data,indent=4))
    response = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)

    # print(response.json()["access_token"])
    if response.status_code == 200:
        print("Success! Token: {token}".format(token=response.json()["access_token"]))
        return response.json()["access_token"]
    else:
        logger.error("Spotify token request failed with status code: {code}".format(code=response.status_code))
        print("Spotify token request failed with status code: {code}".format(code=response.status_code))
        print(response.json())
        return None

# def get_refresh_spotify_token():
#     data = {
#         "grant_type": "refresh_token",
#         "refresh_token": spotify_cred["token"]
#     }

#     headers = {
#         "Authorization": "Basic " + encoded_credentials,
#         "Content-Type": "application/x-www-form-urlencoded"
#     }

#     data["refresh_token"] = get_spotify_token()

#     response = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)

#     if response.status_code == 200:
#         print(response.json()["access_token"])
#     else:
#         print(response.status_code)
#         print(response.json())
    
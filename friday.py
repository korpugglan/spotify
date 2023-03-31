#!/usr/bin/env python3
# Merge multiple Spotify playlists into a single one using the Spotify API

# TODO: Get song list(s) from playlist(s)
# TODO: Combine song lists
# TODO: Remove duplicate songs
# TODO: Add missing to target playlist
# TODO: Remove missing from target playlist
# TODO: Make login nicer: https://www.camiloterevinto.com/post/oauth-pkce-flow-from-python-desktop
# TODO: Fix error catching on retrieving auth code

# Import packages
import base64
import hashlib
import json
import os
import random
import re
import requests
import requests_oauthlib as oauthlib
import string
import sys
import uuid


# Define functions
def load_credentials_from_jsonld(cred_json_name="credentials.jsonld"):
    """Loads credentials from json into a dictionary
        Args:
            cred_json_name (str): Relative path to jsonld file to load
        Returns:
            dictionary (dict): A dictionary with the contents of the json
    """
    with open(cred_json_name) as x:
        dictionary = json.load(x)

    return dictionary


def print_line(print_chars="-", repetition=100):
    """Prints an amount of strings in a row.
        Args:
            print_chars (str): The string to print repeatedly.
            repetition (int): The amount of times the string is printed.
        Returns:
            None
    """
    print(print_chars * repetition)
    return


# Define global variables
api_dict = {"auth_url": "https://accounts.spotify.com/authorize",
            "token_url": "https://accounts.spotify.com/api/token",
            "redirect_uri": "http://localhost:6942"
            }


if __name__ == "__main__":
    print_line()
    print("LOADING CREDENTIALS")
    # Load credentials from jsonld file
    cred_dict = load_credentials_from_jsonld()

    print("CREATING PKCE CODES")
    # Create an initial state token (which should not matter?)
    init_state = uuid.uuid4().hex
    # Create random code verifier with length 128
    rand = random.SystemRandom()
    code_verifier = ''.join(rand.choices(string.ascii_letters + string.digits, k=128))
    # Create a code challenge from the code verifier
    code_sha_256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    b64 = base64.urlsafe_b64encode(code_sha_256)
    code_challenge = b64.decode('utf-8').replace('=', '')
    print_line()

    print("RETRIEVING AUTHORIZATION CODE THROUGH MANUAL LOGIN")
    # Set up payload for request
    auth_payload = {"client_id": cred_dict["client_id"],
                    "response_type": "code",
                    "redirect_uri": api_dict["redirect_uri"],
                    "state": init_state,
                    # "scope": "https://developer.spotify.com/documentation/general/guides/authorization/scopes/",
                    # "show_dialog": "false",
                    "code_challenge_method": "S256",
                    "code_challenge": code_challenge
                    }
    # Get a url to log in through on the first call
    auth_response = requests.get(api_dict["auth_url"], params=auth_payload)
    auth_code_response = input(f"Please go to\n{auth_response.url}\nand copy the url here: ")
    # If the response contains a code, save it as well as the state
    if re.match(api_dict["redirect_uri"] + r"/\?code=.*$", auth_code_response):
        (auth_code, state) = re.match(api_dict["redirect_uri"] + r"/\?code=(.*)&state=(.*)$",
                                      auth_code_response).group(1, 2)
        print(f"Auth code: {auth_code}")
        print(f"State: {state}")
    # If the response contains an error, print it and exit script
    elif re.match(api_dict["redirect_uri"] + r"/\?error=.*$", auth_code_response):
        auth_repsonse_error = re.match(api_dict["redirect_uri"] + r"/\?error=(.*)&state=(.*)$",
                                       auth_code_response).group(1)
        print(f"An error occurred: {auth_repsonse_error}")
        sys.exit()
    # Else just quit the script
    else:
        print(f"An unknown error occurred, please check your callback url and code!")
        sys.exit()
    print_line()

    print("RETRIEVING AUTHORIZATION TOKEN USING THE CODE")
    # Set up headers for the token request
    basic_auth_header_bytes = base64.b64encode(bytes(f"{cred_dict['client_id']}:{cred_dict['client_secret']}", "utf-8"))
    basic_auth_header_str = basic_auth_header_bytes.decode("utf-8")
    token_headers = {"Authorization": f"Basic {basic_auth_header_str}",
                     "Content-Type": "application/x-www-form-urlencoded"
                     }
    # Add the token request payload
    token_payload = {"grant_type": "authorization_code",
                     "code": auth_code,
                     "redirect_uri": api_dict["redirect_uri"],
                     "client_id": cred_dict["client_id"],
                     "code_verifier": code_verifier
                     }
    # Get the token itself
    token_response = requests.post(api_dict["token_url"], headers=token_headers, params=token_payload)
    print(token_response.content)

    print_line("=")
    print("Ciao bella, ciao")
    print_line("=")

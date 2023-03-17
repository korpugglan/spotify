#!/usr/bin/env python3
# Merge multiple Spotify playlists into a single one using the Spotify API

# TODO: Get song list(s) from playlist(s)
# TODO: Combine song lists
# TODO: Add missing to target playlist
# TODO: Remove missing from target playlist

# Import packages
import base64
import hashlib
import json
import requests
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
api_dict = {"base_url": "https://api.spotify.com/v1",
            "auth_url": "https://accounts.spotify.com/authorize",
            "redirect_uri": "http://localhost:8080",
            # "redirect_uri": "https://open.spotify.com/collection/playlists",
            "endpoints": {
                "auth": "/authorization"
                }
            }


if __name__ == "__main__":
    print_line()
    print("LOADING CREDENTIALS")
    cred_dict = load_credentials_from_jsonld()
    # print(cred_dict)

    print("RUNNING USER AUTHORIZATION")
    # https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
    # print(api_dict)
    rfc_state = uuid.uuid4().hex
    code_verifier = base64.urlsafe_b64encode(uuid.uuid4().hex.encode("utf-8"))
    challenge_bytes = hashlib.sha256(code_verifier).digest()
    code_challenge = base64.urlsafe_b64encode(challenge_bytes).rstrip(b'=')

    #TODO: investigate meaning of redirect_uri=YOUR_CALLBACK
    payload = {"client_id": cred_dict["client_id"],
               "response_time": "code",
               "redirect_uri": api_dict["redirect_uri"],
               "state": rfc_state,
               # "scope": "https://developer.spotify.com/documentation/general/guides/authorization/scopes/",
               # "show_dialog": "false",
               "code_challenge_method": "S256",
               "code_challenge": code_challenge
               }

    # auth_response = requests.get(api_dict["base_url"] + api_dict["endpoints"]["auth"], params=payload)
    auth_response = requests.get(api_dict["auth_url"], params=payload)

    print_line()
    print(auth_response)

    print_line("=")
    print("Ciao bella, ciao")
    print_line("=")
    # sys.exit()

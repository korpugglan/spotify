# Dump for parts of code to reuse later on

# https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
# https://stackoverflow.com/questions/65435932/spotify-api-authorization-code-flow-with-python
# https://help.aweber.com/hc/en-us/articles/360036524474-How-do-I-use-Proof-Key-for-Code-Exchange-PKCE-
# https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html

import base64
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import requests_oauthlib as oauthlib
import sys
import uuid

api_dict = {"base_url": "https://api.spotify.com/v1",
            "auth_url": "https://accounts.spotify.com/authorize",
            "redirect_uri": "http://localhost:8080",
            "endpoints": {
                "auth": "/authorization"
                }
            }

# https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
# print(api_dict)
rfc_state = uuid.uuid4().hex
code_verifier = base64.urlsafe_b64encode(uuid.uuid4().hex.encode("utf-8"))
challenge_bytes = hashlib.sha256(code_verifier).digest()
code_challenge = base64.urlsafe_b64encode(challenge_bytes).rstrip(b'=')

# payload = {"client_id": cred_dict["client_id"],
#            "response_type": "code",
#            "redirect_uri": api_dict["redirect_uri"],
#            "state": rfc_state,
#            # "scope": "https://developer.spotify.com/documentation/general/guides/authorization/scopes/",
#            # "show_dialog": "false",
#            "code_challenge_method": "S256",
#            "code_challenge": code_challenge
#            }
#
# auth_response = requests.get(api_dict["auth_url"], params=payload)


# local_server = HTTPServer(("localhost", 8080), BaseHTTPRequestHandler)

oauth = oauthlib.OAuth2Session(cred_dict["client_id"], redirect_uri=api_dict["redirect_uri"])  # , scope=scope)
auth_url, state = oauth.authorization_url(api_dict["auth_url"])
print(f"Please go to {auth_url} and authorize access.")
auth_response = input("Enter the full callback URL: ")
print(auth_response)

# local_server.server_close()
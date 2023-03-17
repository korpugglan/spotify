#!/usr/bin/env python3
# Merge multiple Spotify playlists into a single one using the Spotify API

# TODO: Get song list(s) from playlist(s)
# TODO: Combine song lists
# TODO: Add missing to target playlist
# TODO: Remove missing from target playlist

# Import packages
import requests
import sys


# Define functions
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
base_url = "https://api.spotify.com/v1"


if __name__ == "__main__":
    print_line("\n")
    print_line("RUNNING USER AUTHORIZATION")
    auth_req = requests.get(base_url + "/authorize", )

    print_line("=")
    print("Ciao bella, ciao")
    print_line("=")
    sys.exit()

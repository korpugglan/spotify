#!/usr/bin/env python3
# Merge multiple Spotify playlists into a single one

# Import packages
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


if __name__ == "__main__":
    print_line("=")
    print("Ciao bella, ciao")
    print_line("=")
    sys.exit()

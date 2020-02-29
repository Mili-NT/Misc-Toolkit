#!/usr/bin/python3
from sys import argv
from os import system

def main(x):
    system(f"git clone https://www.github.com/{x}.git")
print(len(argv))
main(argv[1]) if __name__ == "__main__" and (1 < len(argv) < 3) else print(f"Usage: {argv[0]} <profile/repo>")

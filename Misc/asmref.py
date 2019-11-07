#!/usr/bin/python3
import sys
import lxml
import requests
from os import remove
from bs4 import BeautifulSoup
'''
-- Structure --
Data:
{pri_opcd:(mnem, note)}
{primary_opcode:(mnemonic, description)}
'''
#
# Functions
#
def connect(url):
    try:
        page = requests.get(url)
        return page
    except Exception:
        return 0
def fetch_values():
    values = {}
    refguide = connect("http://ref.x86asm.net/x86reference.xml")
    refsoup = BeautifulSoup(refguide.text, 'lxml')
    primary_opcodes = refsoup.find_all('pri_opcd')
    for obj in primary_opcodes:
        split_one = str(obj).split('value="')[1]
        pri_opcd = split_one.split('"')[0]
        toople = (obj.find('mnem'), obj.find('note'))
        values[pri_opcd] = toople
    return values
def unpack_and_display(values):
    with open(sys.path[0] + "/unsanit_values.txt", 'w+') as tmpfile:
        tmpfile.write("# x86 Opcode Reference Guide\n")
        tmpfile.write("--*ref.x86asm.net*--\n\n")
        for k in values.keys():
            tmpfile.write(f"## {k}: {(values[k])[0]}\n")
            tmpfile.write(f"*{(values[k])[1]}*")

#
# Program
#
def main():
    values = fetch_values()
    unpack_and_display(values)
if __name__ == "__main__":
    main()

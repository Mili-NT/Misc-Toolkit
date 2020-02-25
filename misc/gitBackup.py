#!/usr/bin/python3
import os
import requests
from random import choice
from datetime import date
from bs4 import BeautifulSoup

# Profile to backup:
profileLink = "" #TODO: Replace value
backupDir = "" #TODO: Replace value
# Functions:
def randomHeaders():
    user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    ]
    return { 'User-Agent': choice(user_agents), 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' }
def connect(url):
    try:
        page = requests.get(url, headers=randomHeaders())
        return page
    except Exception as e:
        print(f"{e}")
def get_repos(profileLink):
    if profileLink.endswith('/'):
        profileLink = profileLink[:len(profileLink) - 1]
    repos = (profileLink + '?tab=repositories').replace(' ', '')
    profilepage = connect(repos)
    soup = BeautifulSoup(profilepage.text, 'html.parser')
    hrefs = soup.findAll('a', href=True, itemprop="name codeRepository")
    repolist = [f"https://github.com{str(h['href'])}.git" for h in hrefs]
    return repolist
def backup(repolist):
    currentBackup = f"git-{date.today().strftime('%b-%d')}"
    if os.path.isdir(backupDir) is False:
        os.mkdir(backupDir)
    fullpath = f"{backupDir}/{currentBackup}"
    os.mkdir(fullpath)
    for repo in repolist:
        os.system(f"git -C {fullpath} clone {repo}")
    os.system(f"tar -czvf {currentBackup}.tar.gz {fullpath} && rm -R {fullpath}")
def main():
   repolist = get_repos(profileLink)
   backup(repolist)
if __name__ == "__main__":
    main()

import os
import sys
import time
import uuid
from colorama import Fore
from tqdm import tqdm
import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup


try:
    url = "{}".format(input("> Enter url: "))
    while not url:
        print(">" + Fore.RED + " Not entered" + Fore.RESET)
        url = "{}".format(input("> Enter url: "))
except KeyboardInterrupt:
    print("\n>" + Fore.GREEN + " Program interrupted")
    sys.exit()


def getHTML():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    time.sleep(1)
    try:
        if res.status_code == 200:
            return res.content
    except:
        print(">" + Fore.RED + " Received a status code other than 200:{}".format(res.status_code))
        sys.exit()


def imgDownload():
    try:
        soup = BeautifulSoup(getHTML(), "lxml")
    except:
        soup = BeautifulSoup(getHTML(), "html5lib")

    for link in tqdm(soup.find_all("img")):
        img_src = link.get("src")
        if img_src.endswith(".jpg"):
            yield urljoin(url, img_src)
        elif img_src.endswith(".png"):
            yield urljoin(url, img_src)
        time.sleep(1)

    print(">" + Fore.LIGHTGREEN_EX + " Download Complete")


def save():
    print("> Interrupt the program with Ctrl + C")
    print("> Downloading...")
    for img_file in imgDownload():
        req = requests.get(img_file)
        img_file = str(uuid.uuid4()) + ".jpg"
        try:
            if not os.path.exists("./img/"):
                os.mkdir("img")
            with open("./img/" + img_file, "wb") as f:
                f.write(req.content)
        except:
            print(">" + Fore.RED + " Failed to save")
            sys.exit()


def main():
    try:
        save()
    except KeyboardInterrupt:
        print("\n>" + Fore.GREEN + " Program interrupted ")
        sys.exit()

if __name__ == '__main__':
    main()
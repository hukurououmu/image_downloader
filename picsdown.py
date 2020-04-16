import os
import time
import uuid
from logging import getLogger

from tqdm import tqdm
import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/75.0"
        self.url = input("> Enter url: ")
        self.img_format = input("> Enter format(jpg or png or gif): ")


    def get_html(self, url, headers=None):
        logger = getLogger("get_html()")
        try:
            time.sleep(3)
            resp = requests.get(url, headers=headers)
            try:
                soup = BeautifulSoup(resp.text, "lxml")
            except:
                soup = BeautifulSoup(resp.text, "html5lib")
            if resp.status_code == 200:
                return soup
            else:
                raise Exception("Status code error")
        except Exception as e:
            logger.warning(e)
            return None


    def img_download(self):
        logger = getLogger("img_download()")
        try:
            headers = {"User-Agent": self.user_agent}
            soup = self.get_html(self.url, headers)
            if soup != None:
                for link in tqdm(soup.find_all("img"), desc="> Downloading..."):
                    time.sleep(3)
                    img_src = link.get("src")

                    if img_src.endswith(".jpg"):
                        yield urljoin(self.url, img_src)

                    elif img_src.endswith(".png"):
                        yield urljoin(self.url, img_src)
                    
                    elif img_src.endswith(".gif"):
                        yield urljoin(self.url, img_src)
                print("> Complete")
            else:
                raise Exception("No data")
        except Exception as e:
            logger.warning(e)
            return None


    def save_data(self):
        logger = getLogger("save_data()")
        try:
            for img_file in self.img_download():
                resp = requests.get(img_file)
                img_file = str(uuid.uuid4()) + "." + self.img_format
                try:
                    if not os.path.exists("./img/"):
                        os.mkdir("img")
                    with open("./img/" + img_file, "wb") as f:
                        f.write(resp.content)
                except Exception as e:
                    raise e
        except Exception as e:
            logger.warning(e)
            return None




def main():
    try:
        scraper = Scraper()
        scraper.save_data()
    except Exception as e:
        print("> エラーになりました")
        raise e

if __name__ == "__main__":
    main()

from bs4 import BeautifulSoup
import json
import httpx
import logging
import os
import random
import pandas as pd
import time
import typing

from task2.config import settings

logger = logging.getLogger("streamLogger")


def gather_names(session: httpx.Client, url: str):
    """Sync data scrapper: gather all russian animal names from source url and childs"""
    next_url = url
    all_names = []

    while True:
        try:
            r = session.get(next_url, headers=settings.headers)
            time.sleep(random.randrange(2, 5))

            if r.status_code != 200:
                raise ConnectionError("Failed load the source page")
            
            soup = BeautifulSoup(r.text, "lxml")
            
            try:
                next_url = settings.domain + soup.find("a", string="Следующая страница")["href"]
            except Exception as e:
                  raise Exception(f"Failed load next url with exception: {e}") from e
            
            blocks = soup.find_all("div", class_="mw-category mw-category-columns")
            
            if not blocks:
                raise Exception("Failed get main block with names")

            main_block = blocks[-1]

            names = [li.text for li in main_block.find_all("li")]
            last_name = names[-1]

            logger.info(f"Gather another chunk of names: [{len(names)}]. Last name: [{last_name}]")
            
            all_names.extend(names)

            if last_name[0].lower() not in settings.rus_chars:
                logger.info("We have got all russian animal names. Stoping...")
                logger.info("Save already gathered names")
            
                data = {next_url: all_names}
                make_backup(data)
        
                break

            if random.random() > 0.90:
                logger.info("Random sleep escaping parser detecting")
                time.sleep(random.randrange(10, 16))
        
        except Exception as e:
            logger.error(f"Something went wrong with: {e}")
            logger.info("Save already gathered names")
            
            data = {next_url: all_names}
            make_backup(data)
            break


def generate_csv(content: typing.Dict):
    logger.info("Started csv generating...")

    path = os.path.join(settings.DATA_DIR, "beasts.csv")

    df = pd.DataFrame(list(content.items()), columns=["Word", "Count"])
    df.to_csv(path, index=False, encoding='utf-8')


def make_backup(content: typing.Dict):
    path = os.path.join(settings.DATA_DIR, "names_backup.json")

    try:
        with open(path, "w", encoding="utf-8") as json_file:
            json.dump(content, json_file, indent=4, ensure_ascii=False)
        logger.info("Succesful backup...")
    except Exception as e:
        logger.error(f"Failed to create backupfile with error: [{e}]...")


def sort_names() -> None:
    path = os.path.join(settings.DATA_DIR, "names_backup.json")
    
    with open(path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        key = list(data.keys())[0]
        names = data[key]
    
    word_count = {char.upper(): 0 for char in settings.rus_chars}

    for word in names:
        if word and word.lower()[0] in settings.rus_chars:
            word_count[word[0]] += 1

    return word_count


def perform_scraper() -> None:
    logger.info("Start scrapping...")

    session = httpx.Client()
    gather_names(session=session, url=settings.start_url)
    names = sort_names()
    generate_csv(names)

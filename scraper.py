import sys
import re
import logging
import argparse
import requests_html

logging.basicConfig(level=logging.CRITICAL)


class TreccaniScraper:

    BASE_URL = "https://www.treccani.it/vocabolario"

    def __init__(self, word):
        self.sesh = requests_html.HTMLSession()
        self.word = word
        self.SEARCH_URL = f"{self.BASE_URL}/ricerca/{self.word}/"
        logging.debug("Instantiated the object")
    
    def get_possibilities(self):
        p = self.sesh.get(self.SEARCH_URL)
        css_selector = f"a[href*=\/vocabolario\/{self.word}]"
        word_meanings = set()
        for i in p.html.find(css_selector):
            href = i.attrs['href'].strip('/').split('/')[-1]
            if "%28" not in href and "%29" not in href:
                word_meanings.add(href)
        self.word_meanings = word_meanings
        logging.debug("Found %s pages. Looking for defintions...", len(word_meanings))
        return word_meanings

    def get_definitions(self):
        text = set()
        for i in self.word_meanings:
            meaning = i
            MEANING_URL = f"{self.BASE_URL}/{meaning}/"
            page = self.sesh.get(MEANING_URL)
            selector = f"div.text.spiega > p"
            for i in page.html.find(selector):
                text.add(i.text)
        return text
    
    def find_definitions(self, text):
        pattern = re.compile(r"–\s(?:1\.\s)?(.*?)[:;]")
        results = pattern.findall(text)
        return results

# -------------------------------------------------------------------------------------------------------------
def main():
    user_input = sys.argv[1]
    logging.info("Looking for '%s'", user_input)
    scraper = TreccaniScraper(user_input)
    scraper.get_possibilities()
    definitions_txt = scraper.get_definitions()
    for text in definitions_txt:
        print("\n".join(scraper.find_definitions(text)))

main()
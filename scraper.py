import sys
import re
import rich
import logging
import argparse
import requests_html
from rich.console import Console

logging.basicConfig(level=logging.CRITICAL)

rich_console = Console()


class TreccaniScraper:

    BASE_URL = "https://www.treccani.it/vocabolario"

    def __init__(self, word):
        '''
        Each instance is assigned an HTML session and a word
        both of these form the request url
        '''
        self.sesh = requests_html.HTMLSession()
        self.word = word
        self.definitions = []
        self.SEARCH_URL = f"{self.BASE_URL}/ricerca/{self.word}/"
        logging.debug(f" Instantiated the object, word is: {word}")

    def find_pages(self) -> list:
        '''
        Each word can have multiple pages on Treccani:
        this method collects all pages which contain significant meanings
        '''
        p = self.sesh.get(self.SEARCH_URL)
        css_selector = f"a[href*=\/vocabolario\/{self.word}]"
        word_meanings = list()
        for i in p.html.find(css_selector):
            logging.debug(f" found new page address in this element: {i}")
            href = i.attrs['href'].strip('/').split('/')[-1]
            if "%28" not in href and "%29" not in href: # avoid parenthesised urls (usually for non-vocabulary results)
                if href not in word_meanings:
                    word_meanings.append(href)
        self.word_meanings = word_meanings
        logging.debug(f" Found {len(word_meanings)} pages. Looking for defintions...")
        return word_meanings

    def scrape_definitions(self) -> list:
        '''
        This method scrapes the paragraphs containing definitions from a list 
        of partial URLs like {"word1", "word2"}
        '''
        text = list()
        for meaning in self.word_meanings:
            logging.debug(f" New page to scrape: {meaning}")
            MEANING_URL = f"{self.BASE_URL}/{meaning}/"
            page = self.sesh.get(MEANING_URL)
            
            # Find paragraph(s) with the word's definitions 
            selector = f"div.text.spiega > p"
            for i in page.html.find(selector):
                logging.debug(f" Div-text found in the page")
                txt = i.text
                digit_pattern = re.compile(r"(?:\s(\d)\.\s[a-z]\.\s)|(?:\s(\d)\.\s)|(?:\.\s(–))") # digit + letter or only digit
                letter_pattern = re.compile(r"(?<!\s[a-z])[:.]\s([a-z])\.\s(?![a-z]\.)") # only letter pattern preceded by : or . not repeated before/after  
                txt = re.sub(digit_pattern, r"&&m&&", txt)  # meanings become this string
                txt = re.sub(letter_pattern, r"££s££", txt) # sub-meanings become this string
                text.append(txt)
        logging.debug(f" Found {len(text)} paragraphs.")
        self.raw_text = text
        return text

    def split_text_definition(self, text):
        '''
        This method does the heavy lifting of separating the useful text from
        the raw scraped definition: as of now it only takes the first sentence
        of each 'meaning' and puts it in the definitions list'''
        pattern = re.compile(r"\s?&&.*?&&|££.*?££") # &&x&& OR ££x££ 
        def_list = re.split(pattern, text)
        logging.debug(f" list of split text {def_list}")
        for i in def_list[1:3]:
            if i != "":
                logging.debug(f" looking for definition in {i}")
                stops = re.compile(r"[;:.(-](?!,)")
                l = re.split(stops, i)
                # in case the sentence was split on . and the search word was the same letter, add the remaining of the word
                if len(l[0].split(" ")[-1]) == 1 and self.word[0] == l[0].split(" ")[-1]:
                    l[0] += self.word[1:]
                self.definitions.append(l[0])
        return

    def scrape(self) -> list: # main function, calls the intermediate methods and returns the result
        self.find_pages()
        self.scrape_definitions()
        for text in self.raw_text:
            self.split_text_definition(text)
        return self.definitions


# -------------------------------------------------------------------------------------------------------------


def main():
    user_input = sys.argv[1]
    logging.info(f"Looking for '{user_input}'")
    rich_console.print(f"\n[cyan bold underline]Searching for word '{user_input}...'\n")
    scraper = TreccaniScraper(user_input)
    scraper.scrape()
    logging.debug(f" definitions: \n{scraper.definitions}")
    for definition in scraper.definitions:
        rich_console.rule(scraper.word.title())
        rich_console.print(definition)
        

main()


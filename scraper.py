import sys
import re
import argparse
import requests_html


class TreccaniScraper:

    BASE_URL = "https://www.treccani.it/vocabolario"

    def __init__(self, word):
        self.sesh = requests_html.HTMLSession()
        self.word = word
        self.SEARCH_URL = f"{self.BASE_URL}/ricerca/{self.word}/"
    
    def get_possibilities(self):
        p = self.sesh.get(self.SEARCH_URL)
        css_selector = f"a[href*=\/vocabolario\/{self.word}]"
        word_meanings = set()
        for i in p.html.find(css_selector):
            href = i.attrs['href'].strip('/').split('/')[-1]
            if "%28" not in href and "%29" not in href:
                word_meanings.add(href)
        self.word_meanings = word_meanings
        return word_meanings

    def get_definitions(self):
        text = set()
        for i in self.word_meanings:
            meaning = i
            MEANING_URL = f"{self.BASE_URL}/{meaning}/"
            print(f"Meaning URL = {MEANING_URL}")
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
user_input = sys.argv[1]
scraper = TreccaniScraper(user_input)
print(f"received user input: fetching Treccani page '{user_input}'...")
words_set = scraper.get_possibilities()
definitions_txt = scraper.get_definitions()
for text in definitions_txt:
    print(scraper.find_definitions(text))



# if __name__ == '__main__':
# parser = argparse.ArgumentParser(
#     formatter_class=argparse.RawDescriptionHelpFormatter,
#     description=textwrap.dedent("\n\
#     This is a scraper for the Italian renowned Enciclopedia Treccani\n\
#     USAGE:\n\
#     python3 tr3ccani_scraper.py <word>\n\
#     "))
# parser.add_argument('-w', nargs='+')
# parser.add_argument('-e','--enciclopedia', help='Look in Encyclopaedia', default=False)
# parser.add_argument('-v','--vocabulary', help='Look in Vocabulary', default=True)
# arguments = parser.parse_args()
# print(arguments.vocabulary)
# print ("Encyclo: %s" % arguments.enciclopedia )
# print ("Vocab: %s" % arguments.vocabulary )
# main(arguments)
# **Tr3ccani-scraper**  

If you've you ever thought "*I wonder what the definition of 'pasta' is in Italian*", this CLI is for you!  

The **Treccani Encyclopaedia** is a renowned and revered source of knowledge for any respectable italian🇮🇹.

Since they do not provide any APIs exposing their precious dictionary, I thought i could apply my limited knowledge of web-scraping and regular expressions to a good use.  

Unfortunately I don't really have time to maintain the project, but since I plan to use it as a command-line resource I will probably make it better over time.  
Anyway, if you decide to use it and have suggestions for the regex used or the overall process, feel free to submit a pull request: I'll make my best to review it and merge.  

## _Usage:_

The package is written in Python 3.9, but I guess anything above Python 3.6 is supported.

First of all, clone the repository to a local folder on your machine.

```shell
cd <your desired folder>
git clone https://github.com/fcagnola/tr3ccani-scraper.git
```

To scrape the web I used the fantastic requests-html package, which you'll need to install for this to work:

```shell
pip3 install --upgrade requests_html
```

Finally, to get the definition(s) of a word, type

```shell
cd <folder where you cloned the repository>
python3 scraper.py <word>
```

The utility will run and print on the command line one result per line. As of now I only managed to get the first "use" for each page, but I do support multiple pages (each word can have multiple different meanings -> multiple pages, and multiple uses for that meaning).

I'm working on making it available as a python package in order to be able to use it in other scripts.

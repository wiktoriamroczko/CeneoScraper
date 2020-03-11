#import bibliotek
import requests
from bs4 import BeautifulSoup

#adres URL przykładowej strony z opiniami
#URL = "https://www.ceneo.pl/59016320#tab=reviews"
URL = "https://www.ceneo.pl/76891701#tab=reviews"

#pobranie kou html strony z podanego URL
page_respons = requests.get(URL)
page_tree = BeautifulSoup(page_respons.text, 'html.parser')

#wydobycie z koodu html strony fragmentów odpowiadającycm poszczególnym opiniom
opinions = page_tree.find_all("li", "review-box")

#wydobycie składowych dla pojedynczej opinii
opinion = opinions.pop()

opinion_id = opinion["data-entry-id"]
author = opinion.find("div", "reviewer-name-line").string
recommendation = opinion.find("div", "product-review-summary").find("em").string
stars = opinion.find("span", "review-score-count").string
purchased = opinion.find("div", "product-review-pz").string
useful = opinion.find("button", "vote-yes").find("span").string
useless = opinion.find("button", "vote-no").find("span").string
content = opinion.find("p", "product-review-body").get_text()

# - identyfikator: li.review-box["data-entry-id"]
# - data wystawienia: span.review-time > time["datetime"] - pierwszy element listy
# - data zakupu: span.review-time > time["datetime"] - drugi element listy
# - treść: p.product-review-body
# - wady: div.cons-cell > ul
# - zalety: div.pros-cell > ul
# zrobbic date wady i zalety i zeby wszystkie opinie sie pobieraly i byly zapisywane
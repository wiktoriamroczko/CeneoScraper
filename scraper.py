#import bibliotek
import pprint
import requests
from bs4 import BeautifulSoup
import json

#funkcja do ekstrakcji składowych opinii
def extract_feature(opinion, tag, tag_class, child=None):
    try:
        if child:
            return opinion.find(tag, tag_class).find(child).string
        else:
            return opinion.find(tag, tag_class).get_text().strip()
    except AttributeError:
        return None

tags = {
        "recommendation":["div", "product-review-summary", "em"],
        "stars":["span", "review-score-count"],
        "content":["p","product-review-body"],
        "author":["div", "reviewer-name-line"],
        "pros":["div", "pros-cell", "ul"],
        "cons":["div", "cons-cell", "ul"],
        "useless":["button","vote-no", "span"],
        "useful":["button","vote-yes", "span"],
        "purchased":["div", "product-review-pz", "em"]
} 

#funkcja do usuwania znaków formatujących
def remove_whitespaces(string):
    try:
        return string.replace("/n", ", ").replace("/r", ", ")
    except AttributeError:
        pass

#adres URL przykładowej strony z opiniami
url_prefix = "https://www.ceneo.pl"
product_id = input("Podaj kod produktu: ")
url_postfix = "#tab=reviews"
URL = url_prefix + "/"+ product_id + url_postfix

#pusta lista na wszystkie opinie o produkcie
opinions_list = []

while URL:
    #pobranie kou html strony z podanego URL
    page_respons = requests.get(URL)
    page_tree = BeautifulSoup(page_respons.text, 'html.parser')

    #wydobycie z koodu html strony fragmentów odpowiadającycm poszczególnym opiniom
    opinions = page_tree.find_all("li", "js_product-review")

    #wydobycie składowych dla pojedynczej opinii
    for opinion in opinions:
        features = {key:extract_feature(opinion, *args)
                    for key, args in tags.items()} 

        features["purchased"]=(features["purchased"]=="Opinia potwierdzona zakupem")
        features["opinion_id"]= int(opinion["data-entry-id"])
        features["useful"]=int(features["useful"])
        features["useless"]=int(features["useless"])
        features["content"]=remove_whitespaces(features["content"])
        features["pros"]=remove_whitespaces(features["pros"])
        features["cons"]=remove_whitespaces(features["cons"])
        dates = opinion.find("span", "review-time").find_all("time")
        features["review_date"] = dates.pop(0)["datetime"]
        try:
            features["purchase_date"] = dates.pop(0)["datetime"]
        except IndexError:
            features["purchase_date"] = None
        
    opinions_list.append(features)

    try:
        URL = url_prefix + page_tree.find("a", "pagination__next")["href"]
    except TypeError:
        URL = None 
    print(URL)

with open("./opinions_json/"+product_id+'.json', "w", encoding = "utf-8") as fp:
    json.dump(opinions_list, fp, ensure_ascii=False, indent=4, separators=(',', ': '))

print(len(opinions_list))
#pprint.pprint(opinions_list)
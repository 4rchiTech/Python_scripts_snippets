import os
import requests
import random
import re
from math import *
import csv
from bs4 import BeautifulSoup
import urllib.request
import logging
import unidecode

######## Constantes ################

NB_PDTS_PAR_PAGE = 20

CHEMIN_MODULE_DATA = r"C:\\Users\crypt\Desktop\openclassroom\module_2\data"
CHEMIN_LOG = "C:\\Users\crypt\Desktop\openclassroom\module_2\journal_logging.log"
NAME_LOG = "journal_logging.log"

url_test_page_produit = (
    "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
)


#################################

# module logging ########################################################################

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s"
)

file_handler = logging.FileHandler(NAME_LOG)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Fonctions script ####################################################################


def ecriture_csv(categorie=None, input=None):
    nom_fichier_csv = f"\{categorie}.csv"
    path_type = CHEMIN_MODULE_DATA + nom_fichier_csv
    path_clean = path_type.replace(" ", "_")
    with open(path_clean, "a", newline="") as fichier:
        ecriture = csv.writer(fichier, delimiter=",")
        ecriture.writerow(input)


def GET_UA():
    uastrings = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",
    ]

    return random.choice(uastrings)


def scraper_page_produit(page_cible=None):

    logger.debug("--------------------------------------------------------")

    try:
        headers = {"User-Agent": GET_UA()}
        response = requests.get(page_cible, headers=headers)
        ct = response.headers["Content-Type"].lower().strip()

        if "text/html" in ct:
            content = response.content
            soup = BeautifulSoup(content, "html.parser")

            product_page_url = page_cible
            price_including_tax = soup.find_all("td")[3].text[1:]
            price_excluding_tax = soup.find_all("td")[2].text[1:]
            title = soup.h1.text
            universal_product_code_upc = soup.find_all("td")[0].text
            category = soup.find_all("a")[3].string
            product_description = soup.find_all("p")[-1].string

            nb_available = str(soup.find_all("p")[1])
            number_available = re.sub("\D", "", nb_available)

            url_image = soup.find_all("img")[0].get("src")
            image_url = f"http://books.toscrape.com{url_image[5:]}"

            review_rating = soup.find("p", {"class": "star-rating"})["class"][1]

            # enregistrement de l'image dans le dossier images - construction = category_nom_du_livre.jpg
            regex = re.compile("\W+")
            cast_title = regex.sub(" ", title).strip()
            cast2_title = unidecode.unidecode(cast_title).replace("'", " ")
            print(cast2_title)
            titre_cast = cast2_title.replace(" ", "_")
            print(titre_cast)
            path = f"images/{category}_{titre_cast}.jpg".lower()

            urllib.request.urlretrieve(
                image_url,
                path,
            )

            # création de la liste d'informations scrapées pour itération

            liste = [
                product_page_url,
                universal_product_code_upc,
                title,
                price_including_tax,
                price_excluding_tax,
                number_available,
                product_description,
                category,
                review_rating,
                image_url,
            ]

            # écriture dans le csv de la ligne produit

            ecriture_csv(categorie=category, input=liste)

            logger.debug("--------------------------------------------------------")

            return liste

    except Exception as e:
        logger.exception(e)

        logger.debug(
            page_cible, "--------------------------------------------------------"
        )


def scraper_menu():

    logger.debug("--------------------------------------------------------")

    headers = {"User-Agent": GET_UA()}
    response = requests.get("http://books.toscrape.com/", headers=headers)
    ct = response.headers["Content-Type"].lower().strip()

    if "text/html" in ct:
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        bloc_menu = soup.find("div", {"class": "side_categories"})
        liste_url_category = []
        for link in soup.find_all("a"):
            href = link.get("href")

            url_rebuild = f"http://books.toscrape.com/{href}"
            if "category" in url_rebuild:
                liste_url_category.append(url_rebuild)
        liste_url_category.pop(0)

        logger.debug("--------------------------------------------------------")

        return liste_url_category


def createur_arborescence_csv():

    logger.debug("--------------------------------------------------------")

    headers = {"User-Agent": GET_UA()}
    response = requests.get("http://books.toscrape.com/", headers=headers)
    ct = response.headers["Content-Type"].lower().strip()

    if "text/html" in ct:
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        bloc_menu = soup.find("div", {"class": "side_categories"})
        liste_nom_category = []

        for link in soup.find_all("a"):
            href = link.get("href")
            url_rebuild = f"http://books.toscrape.com/{href}"
            if "category" in url_rebuild:
                a_content = link.text.strip()
                liste_nom_category.append(a_content.lower())

        liste_nom_category.pop(0)

        for categorie in liste_nom_category:
            nom_fichier_csv = f"\{categorie}.csv"

            path_type = CHEMIN_MODULE_DATA + nom_fichier_csv
            path_clean = path_type.replace(" ", "_")
            with open(path_clean, "w") as fichier:
                csv.writer(fichier, delimiter=",")

        logger.debug("--------------------------------------------------------")

        return liste_nom_category


def scraper_pages_category(url_category=None):

    logger.debug("--------------------------------------------------------")

    headers = {"User-Agent": GET_UA()}
    response = requests.get(url_category, headers=headers)
    ct = response.headers["Content-Type"].lower().strip()

    if "text/html" in ct:
        try:
            liste_url_produits_totale = []
            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            nb_pages = ceil(int(soup.form.strong.text) / NB_PDTS_PAR_PAGE)
            section = soup.section
            """liste_numero_page = [i for i in range(nb_pages)]"""
            liste_numero_page = list(range(nb_pages))
            url_base_category = url_category[:-10]

            if (
                len(liste_numero_page) > 1
            ):  # Création d'une liste des urls des pages de la catégorie si nb pages > 1
                liste_url_page_category_cible = []
                for i in liste_numero_page:
                    url_page_rebuild = f"{url_base_category}page-{i+1}.html"
                    liste_url_page_category_cible.append(url_page_rebuild)

            # si la catégorie n'a qu'une page, scraper la page
            if len(liste_numero_page) == 1:
                for link in section.find_all("a"):
                    href = link.get("href")[9:]
                    url_rebuild = f"http://books.toscrape.com/catalogue/{href}"
                    if (
                        len(url_rebuild) > 30
                        and url_rebuild not in liste_url_produits_totale
                    ):
                        liste_url_produits_totale.append(url_rebuild)

            else:
                # si la catégorie a + d'une page, pour chaque url de page produit création de la liste des urls de la catégorie ciblée:
                for url in liste_url_page_category_cible:
                    headers = {"User-Agent": GET_UA()}
                    response = requests.get(url, headers=headers)
                    ct = response.headers["Content-Type"].lower().strip()
                    content = response.content
                    soup = BeautifulSoup(content, "html.parser")
                    section = soup.section
                    for link in section.find_all("a"):
                        # pour chaque url PRODUIT de la page, ajouter l'url a la liste des url de la catégorie cible
                        href = link.get("href")[9:]
                        url_rebuild = str(f"http://books.toscrape.com/catalogue/{href}")
                        if (
                            len(url_rebuild) > 30
                            and url_rebuild not in liste_url_produits_totale
                        ):
                            liste_url_produits_totale.append(url_rebuild)

            # retour de fonction, liste des urls de la catégorie ciblée

            logger.debug("--------------------------------------------------------")

            return liste_url_produits_totale

        except Exception as e:
            logger.exception(e)

            logger.debug("--------------------------------------------------------")

            return []


########### MAIN ###################################################################

if __name__ == "__main__":

    try:

        createur_arborescence_csv()

        for category in scraper_menu():
            for url_produit in scraper_pages_category(url_category=category):
                scraper_page_produit(page_cible=url_produit)

    except Exception as e:
        logger.exception(e)


######################################################################################

# UNE PAGE PRODUITS
"""scraper_pages_category(
    url_category="http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
)"""
# 8 PAGES PRODUITS
"""scraper_pages_category(
    "http://books.toscrape.com/catalogue/category/books/religion_12/index.html"
)
"""

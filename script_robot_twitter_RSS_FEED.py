import feedparser
import psycopg2
import logging
import time
import tweepy
import key_words

######################### CONSTANTES

liste_key_words = key_words.key_words

bearer_token = "XXXXXXXXXXXXX"

client = tweepy.Client(bearer_token=bearer_token)

# créer un tweet :
client_push = tweepy.Client(
    consumer_key="XXXXXXXXXX",
    consumer_secret="XXXXXXXXXXXXX",
    access_token="XXXXXXXXXXXXXXXXX",
    access_token_secret="XXXXXXXXXXXXXXXXXXXXXXX",
)

NAME_LOG = "journal_robot_twitter.log"

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

######################### BDD LIENS

url_finance_cnbc = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664"
url_technology_cnbc = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910"
url_worldwnews_cnbc = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100727362"

#######################  URL PARSER

cnbc_finance = feedparser.parse(
    "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664"
)

cnbc_technology = feedparser.parse(
    "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910"
)

cnbc_worldnews = feedparser.parse(
    "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910"
)


all_cnbc_finance = cnbc_finance.entries
all_cnbc_technology = cnbc_technology.entries
all_cnbc_worldnews = cnbc_worldnews.entries

liste_url_articles = [all_cnbc_finance, all_cnbc_technology, all_cnbc_worldnews]

contenu_feed_CNBC = [
    "links",
    "link",
    "id",
    "guidislink",
    "metadata_type",
    "metadata_id",
    "metadata_sponsored",
    "title",
    "title_detail",
    "summary",
    "summary_detail",
    "published",
    "published_parsed",
]


"""premier_article = cnbc_finance.entries[1]  # selection premier article
composants = premier_article.keys()  # colonnes du flux
contenu_article = premier_article.values()  # valeurs du flux

id_article = premier_article.id  # id unique de l'article
title_article = premier_article.title  # titre de l'article
resume_article = premier_article.summary  # résumé de l'article (presque égal au titre)
lien_article = premier_article.link

nombre_articles = len(cnbc_finance.entries)"""

########################################################### ATELIER


def extraction_titre_hashtag(
    titre_article_cible=None,
):  # identifier des mots clés et générer les hashtag pour création d'un quote tweet, sinon renvoie None
    tweet_cast_casse = str(titre_article_cible).lower()

    key_word_selection = [
        "#" + mot for mot in liste_key_words if mot in tweet_cast_casse
    ]
    liste_en_phrase = " ".join(key_word_selection)

    if len(key_word_selection) == 0:
        return None
    else:
        return liste_en_phrase


def extraction_articles(url_rss=None):  # retourne la liste des articles crypto

    liste_finale = []

    for article in url_rss:
        titre_non_cast = article.title
        id_art = article.id
        link_art = article.link

        hashtag = extraction_titre_hashtag(titre_article_cible=titre_non_cast)

        if hashtag != None:
            tuple_article = (id_art, hashtag, titre_non_cast, link_art)

            liste_finale.append(tuple_article)

    print(liste_finale)

    return liste_finale


def creation_tweet(tuple_input=None):
    id_article = tuple_input[0]
    liste_hashtag = tuple_input[1]
    titre = tuple_input[2]
    link = tuple_input[3]

    intro_seanode = "🌐 NEWS ;"

    tweet_final = f"{intro_seanode} {liste_hashtag}\n\n{titre}\n{link}"

    if len(tweet_final) < 280:

        if existence_article_id(id_cible=int(id_article)) == False:
            print("Publication d'un tweet")
            creer_tweet(contenu_tweet=tweet_final)
            record_action(media_name="CNBC", id_article=id_article)
            time.sleep(600)
            return (id_article, tweet_final)
        print("article déja tweeté, pas de création de tweet")
        return (False, False)
    print("Tweet trop grand, abandon de la création du tweet")
    return (False, False)


def extraction_all_article_id():

    connexion = psycopg2.connect(
        host="localhost",
        database="bdd_seanode",
        user="postgres",
        password="archi",
    )

    curseur_selection = connexion.cursor()
    curseur_selection.execute("SELECT article_id FROM robot_twitter_medias")
    liste_id_articles = curseur_selection.fetchall()
    curseur_selection.close()
    liste_clean = [id_art[0] for id_art in liste_id_articles]

    return liste_clean


def record_action(
    media_name=None, id_article=None
):  # enregistre la dernier action realisée dans la bdd activité:

    logger.debug("--------------------------------------------------------")

    connexion = psycopg2.connect(
        host="localhost",
        database="bdd_seanode",
        user="postgres",
        password="archi",
    )

    curseur = connexion.cursor()

    timestamp = int(time.time() * 1000)

    try:

        insertion = "INSERT INTO robot_twitter_medias(media_name, article_id, ts_article_id) VALUES(%s, %s, %s)"
        creation = (
            media_name,
            id_article,
            timestamp,
        )
        curseur.execute(insertion, creation)
        connexion.commit()
        connexion.close()
        logger.debug(f"enregistrement article {media_name} effectué")

        logger.debug("--------------------------------------------------------")

    except Exception as e:
        logger.exception(e)

        logger.debug("--------------------------------------------------------")


def creer_tweet(contenu_tweet=None):
    create_tweet = client_push.create_tweet(text=contenu_tweet)
    return True


def existence_article_id(id_cible=None):
    if id_cible in extraction_all_article_id():
        return True  # il existe bien l'article dans la BDD
    return False


###################### MAIN

while True:

    try:
        for url in liste_url_articles:

            for article in extraction_articles(url_rss=url):

                creation_tweet(tuple_input=article)

    except Exception as e:
        logger.exception(e)

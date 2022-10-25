import tweepy

######################### CONSTANTES

liste_key_words = [
    "keyword1",
    "keyword2",
    "keyword3",
]

bearer_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

client = tweepy.Client(bearer_token=bearer_token)

# créer un tweet :
client_push = tweepy.Client(
    consumer_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    consumer_secret="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    access_token="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    access_token_secret="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
)


# identify keyword from a string
def extraction_hashtags(
    text_cible=None,
):
    txt_lower = str(text_cible).lower()

    key_word_extraction = [mot for mot in liste_key_words if mot in txt_lower]

    if len(key_word_extraction) == 0:
        return None
    else:
        return key_word_extraction


# replace all keywords by #keyword in the string
def hashtagueur(string_cible=None):

    liste_kw = extraction_hashtags(text_cible=string_cible)

    if liste_kw != None:

        compteur = 0
        seuil_compteur = len(liste_kw)

        while compteur != seuil_compteur:
            string_mod = string_cible.replace(
                liste_kw[compteur], f"#{liste_kw[compteur]}"
            )
            compteur += 1
            string_cible = string_mod

        return string_cible

    else:
        return string_cible


## THREAD COMPACT VERSION
def creer_thread(contenu_tweet=None, contenu_tweet2=None):

    create_tweet = client_push.create_tweet(text=contenu_tweet)
    id_tweet_source = create_tweet[0]["id"]

    client_push.create_tweet(text=contenu_tweet2, in_reply_to_tweet_id=id_tweet_source)
    id_second_tweet = create_tweet[0]["id"]

    return True


## VERSION SEMI-INDUSTRIELLE


def creer_tweet_source(contenu_tweet=None):

    create_tweet = client_push.create_tweet(text=contenu_tweet)

    return create_tweet[0]["id"]


def creer_tweet_supplementaire(contenu_tweet=None, id_tweet_source=None):
    create_tweet = client_push.create_tweet(
        text=contenu_tweet, in_reply_to_tweet_id=id_tweet_source
    )

    return create_tweet[0]["id"]

from cgi import print_arguments
import time
import psycopg2
import requests
import random
from bs4 import BeautifulSoup
import re
from threading import Thread

######################################################################### CONSTANTES

API_KEY = "SA7BFKJMMDMYV8KXCA76ESUCYC4WHUR61H"

#########################################################################


def trace(func):
    def decorateur():
        print("execution", func)
        func()

    return decorateur


class robot_BDD(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()

    def run(self):
        while True:

            try:
                prix_eth()
            except Exception as e:
                print(e)
            finally:
                time.sleep(5)
                try:
                    supply_ethereum2()
                except Exception as e:
                    print(e)
                finally:
                    time.sleep(5)
                    try:
                        parse_nb_tx()
                    except Exception as e:
                        print(e)
                    finally:
                        time.sleep(5)
                        try:
                            parse_hashrate_tps()
                        except Exception as e:
                            print(e)
                        finally:
                            time.sleep(5)
                            try:
                                parse_difficulty_rate()
                            except Exception as e:
                                print(e)
                            finally:
                                time.sleep(5)
                                try:
                                    gas_oracle()
                                except Exception as e:
                                    print(e)
                                finally:
                                    time.sleep(5)
                                    try:
                                        nodes_count()
                                    except Exception as e:
                                        print(e)
                                    finally:
                                        time.sleep(5)
                                        try:
                                            market_cap()
                                        except Exception as e:
                                            print(e)


if __name__ == "__main__":

    try:
        robot_BDD()

    except Exception as e:
        print(e)


######################################################################### FONCTION ENREGISTREMENT BDD


def requeteur(requete):

    connexion = psycopg2.connect(
        host="localhost",
        database="node_eth",
        user="postgres",
        password="archi",
    )

    try:
        curseur = connexion.cursor()
        curseur.execute(requete)
        selection_BDD = curseur.fetchall()
        resultat = selection_BDD[0][0]
        connexion.close()

        return resultat

    except Exception as e:
        return e


def create_row_BDD(table=None, liste_colonnes=None, tuple_valeurs=None):

    try:
        connexion = psycopg2.connect(
            host="localhost",
            database="node_eth",
            user="postgres",
            password="archi",
        )
        str_colonne_join = ",".join(liste_colonnes)
        nb_colonnes = len(liste_colonnes)
        liste_values = [("%" + "s,") * nb_colonnes]
        str_value_join = "".join(liste_values)
        str_value_strip = str_value_join.rstrip(str_value_join[-1])

        insertion = f"INSERT INTO {table}({str_colonne_join}) VALUES({str_value_strip})"
        curseur = connexion.cursor()
        creation = tuple_valeurs
        curseur.execute(insertion, creation)
        connexion.commit()
        connexion.close()

        return True

    except Exception as e:
        print(e)

        return False


######################################################################### FONCTIONS RECUPERATION DATA API / SCRAPPING


def prix_eth():
    try:
        timestamp = int(time.time())
        prix_eth = requests.get(
            f"https://api.etherscan.io/api?module=stats&action=ethprice&apikey={API_KEY}"
        )
        content = prix_eth.json()
        eth_btc = float(content["result"]["ethbtc"])
        eth_usd = float(content["result"]["ethusd"])

        create_row_BDD(
            table="explorer_prix_eth",
            liste_colonnes=["timestamp", "eth_price_usd", "eth_price_btc"],
            tuple_valeurs=(timestamp, eth_usd, eth_btc),
        )
        return True

    except Exception as e:
        print(e)

        return False


def supply_ethereum2():
    timestamp = int(time.time())
    try:
        requete = requests.get(
            f"https://api.etherscan.io/api?module=stats&action=ethsupply2&apikey={API_KEY}"
        )
        content = requete.json()
        eth_supply_brute = int(float(content["result"]["EthSupply"]) / float(10**18))
        eth2_staking = int(float(content["result"]["Eth2Staking"]) / float(10**18))
        burnt_fees = int(float(content["result"]["BurntFees"]) / float(10**18))
        eth_supply_nette = eth_supply_brute + eth2_staking - burnt_fees

        create_row_BDD(
            table="explorer_supply",
            liste_colonnes=[
                "timestamp",
                "supply_brute",
                "eth2_staking",
                "burnt_fees",
                "supply_nette",
            ],
            tuple_valeurs=(
                timestamp,
                eth_supply_brute,
                eth2_staking,
                burnt_fees,
                eth_supply_nette,
            ),
        )
    except Exception as e:
        print(e)
        return True


def market_cap():
    timestamp = int(time.time())

    requete_supply_nette = requeteur(
        "SELECT supply_nette FROM explorer_supply ORDER BY timestamp DESC"
    )

    requete_eth_price_usd = requeteur(
        "SELECT eth_price_usd FROM explorer_prix_eth ORDER BY timestamp DESC"
    )

    market_cap = int(requete_supply_nette * requete_eth_price_usd)

    create_row_BDD(
        table="explorer_marketcap",
        liste_colonnes=["timestamp", "market_cap"],
        tuple_valeurs=(timestamp, market_cap),
    )

    return market_cap


#################################### SCRAPPING

###################### BLOC UNIQUE USER AGENT


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


######################


def parse_nb_tx(url="https://etherscan.io/txs"):
    timestamp = int(time.time())
    headers = {"User-Agent": GET_UA()}
    content = None

    try:
        response = requests.get(url, headers=headers)
        ct = response.headers["Content-Type"].lower().strip()

        if "text/html" in ct:
            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            data_cible = soup.find("span", {"class": "d-flex align-items-center"})
            data_cible_txt = data_cible.text
            extraction = re.sub("\D", "", data_cible_txt)

            create_row_BDD(
                table="explorer_nbtransactions",
                liste_colonnes=["timestamp", "nombre_tx"],
                tuple_valeurs=(timestamp, int(extraction)),
            )
            return int(extraction)
        else:
            data_cible_txt = False
            data_cible = False
            content = response.content
            return False

    except Exception as e:
        print("Error", e)
        return False


def parse_hashrate_tps(url="https://etherscan.io/"):
    timestamp = int(time.time())
    headers = {"User-Agent": GET_UA()}
    content = None

    try:
        response = requests.get(url, headers=headers)
        ct = response.headers["Content-Type"].lower().strip()
        if "text/html" in ct:
            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            # hashrate
            hashrate = soup.find("span", {"id": "hashrate"})
            hashrate_clean = hashrate.text
            extraction_hashrate = int(re.sub("\D", "", hashrate_clean)) / 100
            # TPS
            tps_indicateur = soup.find("span", {"class": "text-secondary small"})
            tps_indicateur_clean = tps_indicateur.text
            extraction_tps = int(re.sub("\D", "", tps_indicateur_clean)) / 10
            # enregistrement bdd

            create_row_BDD(
                table="explorer_nbtpshashrate",
                liste_colonnes=["timestamp", "hashrate", "nb_tps"],
                tuple_valeurs=(timestamp, int(extraction_hashrate), extraction_tps),
            )

            return True
        else:
            content = response.content
            soup = None
            return False

    except Exception as e:
        print("Error", e)

    return False


def parse_difficulty_rate(url="https://etherscan.io/chart/difficulty"):
    timestamp = int(time.time())
    headers = {"User-Agent": GET_UA()}
    content = None

    try:
        response = requests.get(url, headers=headers)
        ct = response.headers["Content-Type"].lower().strip()

        if "text/html" in ct:
            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            data_cible = soup.find("b")
            data_nettoyee = data_cible.text
            extraction_difficulty = int(re.sub("\D", "", data_nettoyee)) / 1000
            create_row_BDD(
                table="explorer_difficulty",
                liste_colonnes=["timestamp", "difficulty"],
                tuple_valeurs=(timestamp, int(extraction_difficulty)),
            )
            return True

        else:
            content = response.content
            soup = None
            return False

    except Exception as e:
        print("Error", e)
        return False


##############################################################


def gas_oracle():
    timestamp = int(time.time())
    requete_gas = requests.get(
        f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={API_KEY}"
    )
    content = requete_gas.json()
    dernier_block = content["result"]["LastBlock"]
    safe_gas_price = content["result"][
        "SafeGasPrice"
    ]  # en gwei : prix le plus bas proposé, attendre + pour payer moins de gas fees

    propose_gas_price = content["result"][
        "ProposeGasPrice"
    ]  # en gwei : frais de gas marché

    fast_gas_price = content["result"]["FastGasPrice"]
    # en gwei : frais de gas élevés pour aller + vite
    suggest_base_fee = content["result"]["suggestBaseFee"]
    # en gwei : généré par le protocole, qté minimale nécéssaire pour inclure tx dans un block - donc pour qu'elle soit completée, montant burné

    gas_used_ratio = content["result"]["gasUsedRatio"]
    # pour estimer la congestion du reseau (renvoie liste de : 5 valeurs)

    create_row_BDD(
        table="explorer_gweilvl",
        liste_colonnes=[
            "timestamp",
            "gas_oracle_lower_fees",
            "gas_oracle_market_fees",
            "gas_oracle_base_fees",
            "gas_oracle_higher_fees",
        ],
        tuple_valeurs=(
            timestamp,
            int(safe_gas_price),
            int(propose_gas_price),
            round(float(suggest_base_fee), 2),
            int(fast_gas_price),
        ),
    )

    return True


def nodes_count():
    timestamp = int(time.time())
    requete = requests.get(
        f"https://api.etherscan.io/api?module=stats&action=nodecount&apikey={API_KEY}"
    )
    content = requete.json()
    extraction = content["result"]["TotalNodeCount"]

    create_row_BDD(
        table="explorer_nodes",
        liste_colonnes=["timestamp", "total_node_count"],
        tuple_valeurs=(timestamp, int(extraction)),
    )
    return True


#####################################################################################################


def estimation_time(
    gas_previsionnel=None,
):  # input en gwei, retour en secondes ///////// non utilisé pour le moment
    return eth.get_est_confirmation_time(gas_price=gas_previsionnel)

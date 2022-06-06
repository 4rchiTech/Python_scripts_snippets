from web3 import Web3
import psycopg2
import json

# Commandes ##################################################

# lancer noeud light dans console : geth --syncmode light --http --http.api "eth,debug"

# Constantes ##################################################

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

seuil_whale = 500000000000000000000  # en wei =  500 ETH

############################################################### REQUETES


def get_balance(addresse=None):
    requete = w3.eth.get_balance(addresse)
    return int(requete)


def get_tx_test_extraction(hash_tx):

    requete = w3.eth.get_transaction(transaction_hash=hash_tx)
    block_number = requete["blockNumber"]
    emetteur = requete["from"]
    destinataire = requete["to"]
    valeur_tx = requete["value"]
    index = requete["transactionIndex"]
    valeur_en_eth = valeur_tx / 10**18

    return print(valeur_tx, valeur_en_eth, index)


########################## ATELIER ###############################


def requete():
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost", database="node_eth", user="postgres", password="archi"
        )
        cur = conn.cursor()
        # execute a statement
        cur.execute("SELECT * FROM public.node_eth_whales")
        requete = cur.fetchall()
        print(requete)
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


def insertion_bdd_tx(
    colonne1,
    colonne2,
    colonne3,
    colonne4,
    colonne5,
    valeur1,
    valeur2,
    valeur3,
    valeur4,
    valeur5,
):
    conn = psycopg2.connect(
        host="localhost", database="node_eth", user="postgres", password="archi"
    )
    try:
        cursor = conn.cursor()
        requete = f"INSERT INTO public.explorer_transaction({colonne1},{colonne2},{colonne3},{colonne4},{colonne5}) VALUES(%s, %s, %s, %s, %s)"
        valeur_insertion = (valeur1, valeur2, valeur3, valeur4, valeur5)
        cursor.execute(requete, valeur_insertion)
        conn.commit()
        cursor.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return True


def insertion_bloc(
    colonne1=None,
    colonne2=None,
    colonne3=None,
    colonne4=None,
    colonne5=None,
    colonne6=None,
    colonne7=None,
    valeur1=None,
    valeur2=None,
    valeur3=None,
    valeur4=None,
    valeur5=None,
    valeur6=None,
    valeur7=None,
):
    conn = psycopg2.connect(
        host="localhost", database="node_eth", user="postgres", password="archi"
    )
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO explorer_bloc({colonne1},{colonne2},{colonne3},{colonne4},{colonne5},{colonne6},{colonne7}) VALUES(%s, %s, %s, %s, %s, %s, %s)",
            (
                valeur1,
                valeur2,
                valeur3,
                valeur4,
                valeur5,
                valeur6,
                valeur7,
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return True


def insertion_bloc_2col(table, colonne1, colonne2, valeur1, valeur2):
    conn = psycopg2.connect(
        host="localhost", database="node_eth", user="postgres", password="archi"
    )
    try:
        cursor = conn.cursor()
        requete = f"INSERT INTO {table}({colonne1},{colonne2}) VALUES(%s, %s)"
        valeur_insertion = (valeur1, valeur2)
        cursor.execute(requete, valeur_insertion)
        conn.commit()
        cursor.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return True


def get_block_extraction(numero_bloc):

    try:
        requete = w3.eth.get_block(numero_bloc)
        timestamp = requete["timestamp"]
        difficulty = requete["difficulty"]
        gas_used = requete["gasUsed"]
        addresse_mineur = requete["miner"]
        total_difficulty = requete["totalDifficulty"]
        size = requete["size"]
        nombre_tx = len(requete["transactions"])
        liste_tx = requete["transactions"]

        insertion_bloc(
            colonne1="timestamp",
            colonne2="number",
            colonne3="difficulty",
            colonne4="size",
            colonne5="gas_used",
            colonne6="total_difficulty",
            colonne7="nb_tx_bloc",
            valeur1=timestamp,
            valeur2=numero_bloc,
            valeur3=difficulty,
            valeur4=size,
            valeur5=gas_used,
            valeur6=total_difficulty,
            valeur7=nombre_tx,
        )

        liste_traitee = []

        for tx in liste_tx:
            cast_tx = tx.hex()
            liste_traitee.append(cast_tx)

        solde_mineur = get_balance(addresse_mineur)

        if solde_mineur > seuil_whale:
            insertion_bloc_2col(
                table="public.explorer_mineurs",
                colonne1="addresse",
                colonne2="statut_whale",
                valeur1=addresse_mineur,
                valeur2=True,
            )

        else:
            insertion_bloc_2col(
                table="public.explorer_mineurs",
                colonne1="addresse",
                colonne2="statut_whale",
                valeur1=addresse_mineur,
                valeur2=False,
            )

            return liste_traitee

    except Exception as e:
        print(e)


def get_tx_extraction(hash_tx):

    try:
        requete = w3.eth.get_transaction(transaction_hash=hash_tx)
        block_number = requete["blockNumber"]
        hashtx = requete["blockNumber"]
        emetteur = requete["from"]
        destinataire = requete["to"]
        valeur_tx = requete["value"]

        if valeur_tx > seuil_whale:

            insertion_bdd_tx(
                colonne1="number_bloc",
                colonne2="hash_tx",
                colonne3="emetteur_from",
                colonne4="destinataire_to",
                colonne5="value_tx",
                valeur1=block_number,
                valeur2=hashtx,
                valeur3=emetteur,
                valeur4=destinataire,
                valeur5=valeur_tx,
            )

        solde_emetteur = get_balance(emetteur)
        if solde_emetteur > seuil_whale:
            insertion_bloc_2col(
                table="public.explorer_whales",
                colonne1="addresse",
                colonne2="dernier_solde",
                valeur1=emetteur,
                valeur2=solde_emetteur,
            )

        solde_destinataire = get_balance(destinataire)
        if solde_destinataire > seuil_whale:
            insertion_bloc_2col(
                table="public.explorer_whales",
                colonne1="addresse",
                colonne2="dernier_solde",
                valeur1=destinataire,
                valeur2=solde_destinataire,
            )

    except Exception as e:
        print(e)

    return (block_number, emetteur, destinataire, valeur_tx)


################ MAIN ########################################

"""genesis = 14676250
fonctionnement = True

while fonctionnement:
    if get_block_extraction(numero_bloc=genesis) != None:
        for i in get_block_extraction(numero_bloc=genesis):
            get_tx_extraction(hash_tx=i)
            print("transaction analysée N° :", i)
    genesis += 1
    print("bloc analysé N°", genesis)
    continue
"""


############# ATELIER SMART CONTRACTS

"""contrat_cible = w3.contract.Contract("address")"""

contrat = w3.eth.contract(address="0x514910771AF9Ca656af840dff83E8264EcF986CA")


print(contrat)


test = w3.eth.get_transaction(
    "0x3087506e1654a4f86fec47ce830bf9279ac86ffc018c6a46d2beef9a0917be05"
)
print(test)

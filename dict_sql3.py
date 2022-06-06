import ccxt
import sqlite3
import cds.cds as cds
import ast
import threading


########### LISTE MODULES CEX

gate = ccxt.gateio()
aax = ccxt.aax()
bigone = ccxt.bigone()
binance = ccxt.binance()
bytetrade = ccxt.bytetrade()
cexio = ccxt.cex()
digifinex = ccxt.digifinex()
ftx = ccxt.ftx()
gateio = ccxt.gateio()
huobi = ccxt.huobi()
kucoin = ccxt.kucoin()
latoken = ccxt.latoken()
lbank = ccxt.lbank()
liquid = ccxt.liquid()
lykke = ccxt.lykke()
novadax = ccxt.novadax()
oceanex = ccxt.oceanex()
phemex = ccxt.phemex()
therock = ccxt.therock()
wazirx = ccxt.wazirx()
zipmex = ccxt.zipmex()

#### EXTRACTION DE LA BDD ET TRASNFORMATION EN DICTIONNAIRE


def BDD_en_dictionnaire():

    requete_fetch_all = "SELECT * FROM BDD_suivi_trading_chaines"

    connexionBDD = sqlite3.connect("BDD_suivi_trading_chaines.db")
    curseur = connexionBDD.cursor()
    curseur.execute(requete_fetch_all)
    selection_BDD = curseur.fetchall()

    liste_dictionnaire_chaines = []

    # DICO A COMPLETER

    dico_infos_cex_ccxt = [
        {
            "cex_str": "Gate.io",
            "cex_variable": gate,
            "module_ccxt": ccxt.gateio(),
            "type_ordre": "market",
            "cds": "None",
        },
        {
            "cex_str": "AAX",
            "cex_variable": aax,
            "module_ccxt": ccxt.aax(),
            "type_ordre": "market",
            "cds": "None",
        },
        {
            "cex_str": "Binance",
            "cex_variable": binance,
            "module_ccxt": ccxt.binance(),
            "type_ordre": "limit",
            "cds": cds.binance_sand,
        },
        {
            "cex_str": "FTX",
            "cex_variable": ftx,
            "module_ccxt": ccxt.ftx(),
            "type_ordre": "market",
            "cds": "None",
        },
        {
            "cex_str": "Huobi",
            "cex_variable": huobi,
            "module_ccxt": ccxt.huobi(),
            "type_ordre": "market",
            "cds": cds.huobi,
        },
    ]

    for i in selection_BDD:
        primary_key = i[0]
        cex_name = str(i[1])
        tuplage_chaine = str(ast.literal_eval(i[2]))
        paireA = i[3]
        paireB = i[4]
        paireC = i[5]
        path = i[6]
        statut_trading = i[7]
        etape_trading = i[8]
        statut_ordre_en_cours = i[9]
        last_order_id = i[10]
        limite_paire_A = i[12]
        limite_paire_B = i[13]
        limite_paire_C = i[14]
        res_path = i[15]
        amount_paire_A = i[16]
        amount_paire_B = i[17]
        amount_paire_C = i[18]
        res_token_base = i[19]
        for infos_cex in dico_infos_cex_ccxt:
            if cex_name == infos_cex["cex_str"]:
                module_cex_cible = infos_cex["module_ccxt"]
                module_ccxt = module_cex_cible
                type_order_cex = infos_cex["type_ordre"]
                cds_cex = infos_cex["cds"]
            else:
                pass
        dico = {
            "primary_key": primary_key,
            "cex": cex_name,
            "chaine": tuplage_chaine,
            "paire_A": paireA,
            "paire_B": paireB,
            "paire_C": paireC,
            "path": path,
            "statut_trading": statut_trading,
            "module_ccxt": module_ccxt,
            "cds": cds_cex,
            "etape_trading": etape_trading,
            "statut_ordre_en_cours": statut_ordre_en_cours,
            "type_ordre": type_order_cex,
            "last_order_id": last_order_id,
            "limite_paire_A": limite_paire_A,
            "limite_paire_B": limite_paire_B,
            "limite_paire_C": limite_paire_C,
            "res_path": res_path,
            "amount_paire_A": amount_paire_A,
            "amount_paire_B": amount_paire_B,
            "amount_paire_C": amount_paire_C,
            "res_token_base": res_token_base,
        }

        liste_dictionnaire_chaines.append(dico)

    connexionBDD.close()

    return liste_dictionnaire_chaines


# A CE STADE, DICTIONNAIRE COMPLET (COPIE DE LA BDD)


############## FONCTIONS

verrou = threading.RLock()


def limit_order_buy_pathA_paires_AB(cds_cex_cible, paire_cible, amount, budget):
    cds_cex_cible.load_markets()
    price = budget
    symbol = paire_cible
    formatted_amount = cds_cex_cible.amount_to_precision(symbol, amount)
    formatted_price = cds_cex_cible.price_to_precision(symbol, price)

    response = cds_cex_cible.create_limit_buy_order(
        paire_cible, amount=formatted_amount, price=formatted_price
    )

    return response["info"]["orderId"]


def limit_order_sell_pathA_paire_C(cds_cex_cible, paire_cible, amount, budget):
    cds_cex_cible.load_markets()
    price = budget
    symbol = paire_cible
    formatted_amount = cds_cex_cible.amount_to_precision(symbol, amount)
    formatted_price = cds_cex_cible.price_to_precision(symbol, price)

    response = cds_cex_cible.create_limit_sell_order(
        paire_cible, amount=formatted_amount, price=formatted_price
    )

    return response["info"]["orderId"]


def maj_except_BDD(chaine_cle_primaire, valeur_except):

    with verrou:
        statut_trading = "impossible"

        connexionBDD = sqlite3.connect("BDD_suivi_trading_chaines.db")
        curseur = connexionBDD.cursor()
        requete_fetch_all_pour_MAJ = "SELECT * FROM BDD_suivi_trading_chaines"
        curseur.execute(requete_fetch_all_pour_MAJ)
        maj_iteration = "UPDATE BDD_suivi_trading_chaines SET statut_trading = ?, remarque =?  WHERE primary_key = ?"
        curseur_update = connexionBDD.cursor()
        colonne_ts_res_maj = (
            statut_trading,
            valeur_except,
            chaine_cle_primaire,
        )
        curseur_update.execute(maj_iteration, colonne_ts_res_maj)
        connexionBDD.commit()
        connexionBDD.close()
        print(
            "trading chaine interdit à cause except:",
            chaine_cle_primaire,
        )

    return True


def maj_BDD(
    primary_key=None, etape_trading_maj=None, statut_ordre_maj=None, order_id=None
):
    with verrou:
        requete_part1 = "SELECT * FROM BDD_suivi_trading_chaines WHERE primary_key ='"
        requete_part_3 = "'"
        requete_chaine_cible = requete_part1 + primary_key + requete_part_3

        connexionBDD = sqlite3.connect("BDD_suivi_trading_chaines.db")
        curseur_selection = connexionBDD.cursor()
        executer_requete = curseur_selection.execute(requete_chaine_cible)

        maj_chaine_trade = "UPDATE BDD_suivi_trading_chaines SET etape_trading = ?, statut_ordre_en_cours = ?, last_order_id = ? WHERE primary_key = ?"
        curseur_maj_chaine = connexionBDD.cursor()
        colonnes_maj = (etape_trading_maj, statut_ordre_maj, order_id, primary_key)
        curseur_maj_chaine.execute(maj_chaine_trade, colonnes_maj)
        connexionBDD.commit()

        connexionBDD.close()

    return True


def maj_BDD_etape_C(
    primary_key=None,
    statut_trading=None,
    etape_trading_maj=None,
    statut_ordre_maj=None,
    order_id=None,
):
    with verrou:
        requete_part1 = "SELECT * FROM BDD_suivi_trading_chaines WHERE primary_key ='"
        requete_part_3 = "'"
        requete_chaine_cible = requete_part1 + primary_key + requete_part_3

        connexionBDD = sqlite3.connect("BDD_suivi_trading_chaines.db")
        curseur_selection = connexionBDD.cursor()
        executer_requete = curseur_selection.execute(requete_chaine_cible)

        maj_chaine_trade = "UPDATE BDD_suivi_trading_chaines SET statut_trading = ?, etape_trading = ?, statut_ordre_en_cours = ?, last_order_id = ? WHERE primary_key = ?"
        curseur_maj_chaine = connexionBDD.cursor()
        colonnes_maj = (
            statut_trading,
            etape_trading_maj,
            statut_ordre_maj,
            order_id,
            primary_key,
        )
        curseur_maj_chaine.execute(maj_chaine_trade, colonnes_maj)
        connexionBDD.commit()

        connexionBDD.close()

    return True


def maj_initialisation(
    primary_key,
    statut_trading,
    etape_trading,
    statut_ordre,
    check_paireA,
    check_paireB,
    check_paireC,
    resultat_path_round,
    amount_paire_A,
    amount_paire_B,
    amount_paire_C,
    res_base_token,
):
    with verrou:
        connexionBDD = sqlite3.connect("BDD_suivi_trading_chaines.db")
        curseur = connexionBDD.cursor()
        requete_fetch_all_pour_MAJ = "SELECT * FROM BDD_suivi_trading_chaines"
        curseur.execute(requete_fetch_all_pour_MAJ)
        maj_iteration = "UPDATE BDD_suivi_trading_chaines SET statut_trading = ?, etape_trading = ?, statut_ordre_en_cours = ?, limite_paire_A = ?, limite_paire_B = ?, limite_paire_C = ?, res_path = ?, amount_paire_A = ?, amount_paire_B = ?, amount_paire_C = ?, res_token_base = ? WHERE primary_key = ?"
        curseur_update = connexionBDD.cursor()
        colonne_ts_res_maj = (
            statut_trading,
            etape_trading,
            statut_ordre,
            check_paireA,
            check_paireB,
            check_paireC,
            resultat_path_round,
            amount_paire_A,
            amount_paire_B,
            amount_paire_C,
            res_base_token,
            primary_key,
        )
        curseur_update.execute(maj_iteration, colonne_ts_res_maj)
        connexionBDD.commit()
        connexionBDD.close()
        print("trading chaine autorisé:", primary_key)

    return True


def maj_denied(primary_key):

    with verrou:
        statut_trading = "denied"
        connexionBDD = sqlite3.connect("BDD_suivi_trading_chaines.db")
        curseur = connexionBDD.cursor()
        requete_fetch_all_pour_MAJ = "SELECT * FROM BDD_suivi_trading_chaines"
        curseur.execute(requete_fetch_all_pour_MAJ)
        maj_iteration = "UPDATE BDD_suivi_trading_chaines SET statut_trading = ? WHERE primary_key = ?"
        curseur_update = connexionBDD.cursor()
        colonne_ts_res_maj = (
            statut_trading,
            primary_key,
        )
        curseur_update.execute(maj_iteration, colonne_ts_res_maj)
        connexionBDD.commit()
        connexionBDD.close()
        print("trading chaine interdit:", primary_key)

    return True


def delete_BDD_denied(chaine):
    with verrou:
        connexionBDD = sqlite3.connect("BDD_suivi_trading_chaines.db")
        curseur = connexionBDD.cursor()
        requete_delete = (
            "DELETE FROM BDD_suivi_trading_chaines WHERE statut_trading = 'denied'"
        )
        curseur.execute(requete_delete)
        connexionBDD.commit()
        print("trading chaine effacé de la BDD:", chaine["primary_key"])

    return True


def veille_orders(
    cds_cex_cible=None,
    paire_cible=None,
    order_id_cible=None,
):

    closed_orders = cds_cex_cible.fetch_closed_orders(symbol=paire_cible)
    for orders in closed_orders:
        if orders["clientOrderId"] == order_id_cible:
            if orders["status"] == "closed":
                return True
            else:
                print("ordre non clôturé, statut:", orders["status"])
                return False


############## MAIN SCRIPT


def scanner_initialisation(objectif=None, budget_par_trade=None):
    try:
        for chaine in BDD_en_dictionnaire():
            cds_cex_cible = chaine["cds"]

            if chaine["statut_trading"] == "initialisation":
                if chaine["path"] == "pathA":

                    try:
                        paire_A = chaine["paire_A"]
                        paire_B = chaine["paire_B"]
                        paire_C = chaine["paire_C"]
                        module_cex_cible = chaine["module_ccxt"]
                        pathA_check_paireA = module_cex_cible.fetch_order_book(paire_A)[
                            "asks"
                        ][0][0]
                        pathA_check_paireB = module_cex_cible.fetch_order_book(paire_B)[
                            "asks"
                        ][0][0]
                        pathA_check_paireC = module_cex_cible.fetch_order_book(paire_C)[
                            "bids"
                        ][0][0]

                        resultat_pathA = (
                            (1 / pathA_check_paireA)
                            * (1 / pathA_check_paireB)
                            * pathA_check_paireC
                        )
                        resultat_pathA_round = round(resultat_pathA, 5)

                        print(
                            "le résultat du traitement de chaine initialisée:",
                            chaine,
                            resultat_pathA_round,
                        )

                        if resultat_pathA_round > objectif:
                            # VARIABLES DE STATUT
                            statut_trading = "autorised"
                            etape_trading = "initialisation"
                            statut_ordre = "aucun"

                            amount_paire_A = budget_par_trade / pathA_check_paireA
                            amount_paire_B = amount_paire_A / pathA_check_paireB
                            amount_paire_C = amount_paire_B * pathA_check_paireC
                            res_base_token = round(budget_par_trade * resultat_pathA, 4)

                            maj_initialisation(
                                primary_key=chaine["primary_key"],
                                statut_trading=statut_trading,
                                etape_trading=etape_trading,
                                statut_ordre=statut_ordre,
                                check_paireA=pathA_check_paireA,
                                check_paireB=pathA_check_paireB,
                                check_paireC=pathA_check_paireC,
                                resultat_path_round=resultat_pathA_round,
                                amount_paire_A=amount_paire_A,
                                amount_paire_B=amount_paire_B,
                                amount_paire_C=amount_paire_C,
                                res_base_token=res_base_token,
                            )

                        else:
                            maj_denied(chaine["primary_key"])

                    except:
                        maj_denied(chaine["primary_key"])

                if chaine["path"] == "pathB":

                    try:
                        paire_A_pathB = chaine["paire_A"]
                        paire_B_pathB = chaine["paire_B"]
                        paire_C_pathB = chaine["paire_C"]
                        module_cex_cible = chaine["module_ccxt"]
                        pathB_check_paireA = module_cex_cible.fetch_order_book(
                            paire_A_pathB
                        )["bids"][0][0]
                        pathB_check_paireB = module_cex_cible.fetch_order_book(
                            paire_B_pathB
                        )["bids"][0][0]
                        pathB_check_paireC = module_cex_cible.fetch_order_book(
                            paire_C_pathB
                        )["asks"][0][0]

                        resultat_pathB = (
                            (1 / pathB_check_paireC)
                            * pathB_check_paireB
                            * pathB_check_paireA
                        )
                        resultat_pathB_round = round(resultat_pathB, 5)

                        print(
                            "le résultat du traitement:", chaine, resultat_pathB_round
                        )

                        if resultat_pathB_round > objectif:
                            # VARIABLES DE STATUT
                            statut_trading = "autorised"
                            etape_trading = "initialisation"
                            statut_ordre = "aucun"

                            ########" ATTENTION PATH? BONNE PAIRE?"

                            amount_paire_C_pathB = budget_par_trade / pathB_check_paireC
                            amount_paire_B_pathB = amount_paire_C * pathB_check_paireB
                            amount_paire_A_pathB = amount_paire_B * pathB_check_paireA
                            res_base_token_pathB = budget_par_trade * resultat_pathB

                            maj_initialisation(
                                primary_key=chaine["primary_key"],
                                statut_trading=statut_trading,
                                etape_trading=etape_trading,
                                statut_ordre=statut_ordre,
                                check_paireA=pathB_check_paireA,
                                check_paireB=pathB_check_paireB,
                                check_paireC=pathB_check_paireC,
                                resultat_path_round=resultat_pathB_round,
                                amount_paire_A=amount_paire_A_pathB,
                                amount_paire_B=amount_paire_B_pathB,
                                amount_paire_C=amount_paire_C_pathB,
                                res_base_token=res_base_token_pathB,
                            )

                        else:
                            # VARIABLES DE STATUT
                            maj_denied(chaine["primary_key"])

                    except:
                        maj_denied(chaine["primary_key"])

            if chaine["statut_trading"] == "denied":
                delete_BDD_denied(chaine["primary_key"])
                pass

    except Exception as e:
        print("crash de l'except principal :", e)
        pass

    finally:

        return True


def script_etape_A():

    print("Script 4 en fonctionnement : trading des chaines en étape 1")

    for chaine in BDD_en_dictionnaire():
        try:
            cds_cex_cible = chaine["cds"]
            paire_A = chaine["paire_A"]
            paire_B = chaine["paire_B"]
            if chaine["statut_trading"] == "autorised":
                if chaine["path"] == "pathA":
                    if chaine["etape_trading"] == "initialisation":
                        if chaine["statut_ordre_en_cours"] == "aucun":
                            # VARIABLES
                            etape_maj = "A"
                            statut_maj_order = "running"
                            # FONCTION ACHAT ORDRE LIMIT
                            order_id = limit_order_buy_pathA_paires_AB(
                                cds_cex_cible=cds_cex_cible,
                                paire_cible=paire_A,
                                amount=chaine["amount_paire_A"],
                                budget=chaine["limite_paire_A"],
                            )
                            order_id_stock = order_id
                            print("ordre achat initié", chaine["primary_key"])

                            # maj bdd
                            maj_BDD(
                                chaine["primary_key"],
                                etape_maj,
                                statut_maj_order,
                                order_id_stock,
                            )
            continue
        except Exception as e:  # maj denied
            maj_except_BDD(chaine["primary_key"], str(e))
            print("crash sur script étape 1 trading :", e)
        finally:
            pass


def script_etape_B():

    print("Script 4 en fonctionnement : trading des chaines en étape 2")

    for chaine in BDD_en_dictionnaire():
        try:
            cds_cex_cible = chaine["cds"]
            paire_A = chaine["paire_A"]
            paire_B = chaine["paire_B"]
            paire_C = chaine["paire_C"]
            if chaine["statut_trading"] == "autorised":
                if chaine["path"] == "pathA":
                    if chaine["etape_trading"] == "B":
                        if chaine["statut_ordre_en_cours"] == "aucun":
                            # VARIABLES
                            etape_maj = "B"
                            statut_maj_order = "running"
                            # FONCTION ACHAT ORDRE LIMIT
                            order_id = limit_order_buy_pathA_paires_AB(
                                cds_cex_cible=cds_cex_cible,
                                paire_cible=paire_B,
                                amount=chaine["amount_paire_B"],
                                budget=chaine["limite_paire_B"],
                            )
                            order_id_stock = order_id
                            print("ordre achat initié", chaine["primary_key"])

                            # maj bdd
                            maj_BDD(
                                chaine["primary_key"],
                                etape_maj,
                                statut_maj_order,
                                order_id_stock,
                            )
            continue
        except Exception as e:  # maj denied
            maj_except_BDD(chaine["primary_key"], str(e))
            print("crash sur script étape 2 trading :", e)
        finally:
            pass


def script_etape_C():

    print("Script 4 en fonctionnement : trading des chaines en étape 3")

    for chaine in BDD_en_dictionnaire():
        try:
            cds_cex_cible = chaine["cds"]
            paire_A = chaine["paire_A"]
            paire_B = chaine["paire_B"]
            paire_C = chaine["paire_C"]
            if chaine["statut_trading"] == "autorised":
                if chaine["path"] == "pathA":
                    if chaine["etape_trading"] == "C":
                        if chaine["statut_ordre_en_cours"] == "aucun":
                            # VARIABLES
                            etape_maj = "C"
                            statut_maj_order = "running"
                            # FONCTION ACHAT ORDRE LIMIT
                            order_id = limit_order_sell_pathA_paire_C(
                                cds_cex_cible=cds_cex_cible,
                                paire_cible=paire_C,
                                amount=chaine["amount_paire_B"],
                                budget=chaine["limite_paire_C"],
                            )
                            order_id_stock = order_id
                            print("ordre vente initié", chaine["primary_key"])

                            # maj bdd
                            maj_BDD(
                                chaine["primary_key"],
                                etape_maj,
                                statut_maj_order,
                                order_id_stock,
                            )
            continue
        except Exception as e:  # maj denied
            maj_except_BDD(chaine["primary_key"], str(e))
            print("crash sur script étape 3 trading :", e)
        finally:
            pass


def script_veille():  ########## mettre verrou?

    print("Script 4 en fonctionnement : MAJ des ordres en cours")
    try:
        for chaine in BDD_en_dictionnaire():
            cds_cex_cible = chaine["cds"]
            order_id = chaine["last_order_id"]

            if chaine["statut_ordre_en_cours"] == "running":

                if chaine["etape_trading"] == "A":
                    paire_cible = chaine["paire_A"]
                    etape_trading_maj = "B"
                    statut_ordre_maj = "aucun"
                    if veille_orders(
                        cds_cex_cible=cds_cex_cible,
                        paire_cible=paire_cible,
                        order_id_cible=order_id,
                    ):

                        maj_BDD(
                            chaine["primary_key"],
                            etape_trading_maj=etape_trading_maj,
                            statut_ordre_maj=statut_ordre_maj,
                            order_id="aucun",
                        )

                elif chaine["etape_trading"] == "B":
                    paire_cible = chaine["paire_B"]
                    etape_trading_maj = "C"
                    statut_ordre_maj = "aucun"
                    if veille_orders(
                        cds_cex_cible=cds_cex_cible,
                        paire_cible=paire_cible,
                        order_id_cible=order_id,
                    ):

                        maj_BDD(
                            chaine["primary_key"],
                            etape_trading_maj=etape_trading_maj,
                            statut_ordre_maj=statut_ordre_maj,
                            order_id="aucun",
                        )

                elif chaine["etape_trading"] == "C":
                    print("entrée dans la chaine C")
                    paire_cible = chaine["paire_C"]
                    statut_trading = "initialisation"
                    etape_trading_maj = "initialisation"
                    statut_ordre_maj = "aucun"
                    if veille_orders(
                        cds_cex_cible=cds_cex_cible,
                        paire_cible=paire_cible,
                        order_id_cible=order_id,
                    ):

                        maj_BDD_etape_C(
                            chaine["primary_key"],
                            statut_trading=statut_trading,
                            etape_trading_maj=etape_trading_maj,
                            statut_ordre_maj=statut_ordre_maj,
                            order_id="aucun",
                        )
    except Exception as e:
        print("crash sur script veille MAJ trading :", e)

    finally:

        return True

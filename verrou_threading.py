import ccxt
import sqlite3
import time
import ast
import threading

verrou = threading.RLock()


def maj_BDD_scanner(
    cex_cible=None,
    resultat_pathA_round=None,
    resultat_pathB_round=None,
    cle_primaire=None,
):

    with verrou:
        time_stamp_actuel = int(time.time())
        delai_secondes_avant_update = str(2000 * 60)
        time_stamp_seuil = str(time_stamp_actuel - int(delai_secondes_avant_update))

        connexionBDD = sqlite3.connect("BDD_scanner.db")
        curseur = connexionBDD.cursor()

        requete_part1 = "SELECT * FROM BDD_scanner WHERE cex = '"
        requete_part2 = str(cex_cible)
        requete_part3 = "' AND timestamp IS NULL OR timestamp < "
        requete_all = str(
            requete_part1 + requete_part2 + requete_part3 + time_stamp_seuil
        )

        chercher_timestamp_expire = curseur.execute(requete_all)
        maj_iteration = "UPDATE BDD_scanner SET timestamp = ?, res_pathA = ?, res_pathB = ? WHERE primary_key = ?"
        curseur_update = connexionBDD.cursor()

        colonne_ts_res_maj = (
            time_stamp_actuel,
            resultat_pathA_round,
            resultat_pathB_round,
            cle_primaire,
        )
        curseur_update.execute(maj_iteration, colonne_ts_res_maj)
        connexionBDD.commit()
        print("MAJ enregistrée de la chaine :", cle_primaire)


def fonction_scanner_chaines(cex_cible=None):

    print("Script 2 en fonctionnement : scanning des chaines existantes")

    try:
        # VARIABLES
        time_stamp_actuel = int(time.time())
        delai_secondes_avant_update = str(2000 * 60)
        time_stamp_seuil = str(time_stamp_actuel - int(delai_secondes_avant_update))

        # EXTRACTION BDD ET REFORMATAGE EN TUPLE

        requete_part1 = "SELECT * FROM BDD_scanner WHERE cex = '"
        requete_part2 = str(cex_cible)
        requete_part3 = "' AND timestamp IS NULL OR timestamp < "
        requete_all = str(
            requete_part1 + requete_part2 + requete_part3 + time_stamp_seuil
        )

        connexionBDD = sqlite3.connect("BDD_scanner.db")
        curseur = connexionBDD.cursor()
        curseur.execute(requete_all)
        selection_BDD = curseur.fetchall()

        selection_reformatee = []

        for i in selection_BDD:
            primary_key = i[0]
            cex_name = i[1]
            tuplage_chaine = ast.literal_eval(i[2])
            paireA = i[3]
            paireB = i[4]
            paireC = i[5]
            tuple_i = (primary_key, cex_name, tuplage_chaine, paireA, paireB, paireC)
            selection_reformatee.append(tuple_i)

        connexionBDD.close()

        # TEST DES CHAINES ET ENREGISTREMENT BDD RESU POUR TRADING

        for i in selection_reformatee:
            try:
                cle_primaire = i[0]
                # PATH A - fiabilité/complétude data puis enregistrement resultat PATH
                pathA_check_paireA = cex_cible.fetch_order_book(symbol=i[2][0])["asks"]
                pathA_check_paireB = cex_cible.fetch_order_book(symbol=i[2][1])["asks"]
                pathA_check_paireC = cex_cible.fetch_order_book(symbol=i[2][2])["bids"]
                # PATH B
                pathB_check_paireA = cex_cible.fetch_order_book(symbol=i[2][0])["bids"]
                pathB_check_paireB = cex_cible.fetch_order_book(symbol=i[2][1])["bids"]
                pathB_check_paireC = cex_cible.fetch_order_book(symbol=i[2][2])["asks"]

                if len(pathA_check_paireA) == 0:
                    pass
                else:
                    if len(pathA_check_paireB) == 0:
                        pass
                    else:
                        if len(pathA_check_paireC) == 0:
                            pass
                        else:

                            resultat_pathA = (
                                (1 / pathA_check_paireA[0][0])
                                * (1 / pathA_check_paireB[0][0])
                                * pathA_check_paireC[0][0]
                            )
                            resultat_pathA_round = round(resultat_pathA, 5)
                            print(resultat_pathA_round)

                            resultat_pathB = (
                                (1 / pathB_check_paireC[0][0])
                                * pathB_check_paireB[0][0]
                                * pathB_check_paireA[0][0]
                            )
                            resultat_pathB_round = round(resultat_pathB, 5)
                            print(resultat_pathB_round)

                            # ENREGISTREMENT

                            maj_BDD_scanner(
                                cex_cible=cex_cible,
                                resultat_pathA_round=resultat_pathA_round,
                                resultat_pathB_round=resultat_pathB_round,
                                cle_primaire=cle_primaire,
                            )

            except Exception as e:
                print("Crash du script, cause :", e)
                pass
        connexionBDD.close()
    except Exception as f:
        print("crash majeur", f)

    return True

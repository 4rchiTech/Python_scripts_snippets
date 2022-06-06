import ccxt
import sqlite3

import time

from random import *

time_stamp_actuel = int(time.time())

# LISTE MODULES CEX
liste_totale = ccxt.exchanges
######


def fonction_creation_chaines(cex_cible=None, paires_cible=None):
    def tirage():

        connexionBDD = sqlite3.connect("BDD_scanner.db")
        curseur = connexionBDD.cursor()
        chaine_fusible = []
        chaine_construite = []
        chaine_fusible.append(paires_cible[compteur])
        for i in paires_cible:
            if i[1] == chaine_fusible[0][0]:
                paireC = i[0], chaine_fusible[0][1]
                chaine_construite.append(chaine_fusible[0] + i + paireC)

                if len(chaine_construite) > 1:
                    for i in chaine_construite:
                        paireA = str(i[0] + "/" + i[1])
                        paireB = str(i[2] + "/" + i[3])
                        paireC = str(i[4] + "/" + i[5])

                        chaine_finale = str((paireA, paireB, paireC))
                        primary_key = (
                            str_cex_cible + i[0] + i[1] + i[2] + i[3] + i[4] + i[5]
                        )
                        paireC_formatTuple = (i[4], i[5])

                        try:
                            if paireC_formatTuple in paires_cible:
                                ajout_iteration = "INSERT INTO BDD_scanner(primary_key, cex, chain, paireA, paireB, paireC) VALUES(?, ?, ?, ?, ?, ?)"
                                infos_iteration = (
                                    primary_key,
                                    str_cex_cible,
                                    chaine_finale,
                                    paireA,
                                    paireB,
                                    paireC,
                                )
                                curseur.execute(ajout_iteration, infos_iteration)
                                connexionBDD.commit()
                                print("chaine enregistrée :", cex_cible, chaine_finale)
                                pass
                            else:
                                pass
                        except Exception as e:
                            pass
        connexionBDD.close()
        return 1

    ##### VARIABLES
    str_cex_cible = str(cex_cible)
    seuil = len(paires_cible)
    compteur = 0

    while seuil != compteur:
        tirage()
        compteur += 1
        print(compteur)

    return True

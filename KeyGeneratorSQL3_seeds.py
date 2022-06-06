# coding:utf-8

from random import *
from secrets import *
import sqlite3


def module_create_seeds():

    statut_seed = "untested"

    def usine_cles():

        longueur_seed = 12

        ##########" Listes mots

        liste_3_car = []
        liste_4_car = []
        liste_5_car = []
        liste_6_car = []
        liste_7_car = []
        liste_8_car = []

        ###### ouverture de fichier pour création liste de nuage de mots à 3 car nettoyée

        with open(
            r"C:\Users\crypt\Desktop\MetaBot_vF\Modules\Nuages_mots\mots_3_car.txt",
            "r",
        ) as BDD_3_car:
            liste_bdd_3 = BDD_3_car.readlines()

        liste_nettoyee_3 = liste_bdd_3

        for i in liste_nettoyee_3:
            liste_3_car.append(i.rstrip("\n"))

        ###### ouverture de fichier pour création liste de nuage de mots à 4 car nettoyée

        with open(
            r"C:\Users\crypt\Desktop\MetaBot_vF\Modules\Nuages_mots\mots_4_car.txt",
            "r",
        ) as BDD_4_car:
            liste_bdd_4 = BDD_4_car.readlines()

        liste_nettoyee_4 = liste_bdd_4

        for i in liste_nettoyee_4:
            liste_4_car.append(i.rstrip("\n"))

        ###### ouverture de fichier pour création liste de nuage de mots à 5 car nettoyée

        with open(
            r"C:\Users\crypt\Desktop\MetaBot_vF\Modules\Nuages_mots\mots_5_car.txt",
            "r",
        ) as BDD_5_car:
            liste_bdd_5 = BDD_5_car.readlines()

        liste_nettoyee_5 = liste_bdd_5

        for i in liste_nettoyee_5:
            liste_5_car.append(i.rstrip("\n"))

        ###### ouverture de fichier pour création liste de nuage de mots à 6 car nettoyée

        with open(
            r"C:\Users\crypt\Desktop\MetaBot_vF\Modules\Nuages_mots\mots_6_car.txt",
            "r",
        ) as BDD_6_car:
            liste_bdd_6 = BDD_6_car.readlines()

        liste_nettoyee_6 = liste_bdd_6

        for i in liste_nettoyee_6:
            liste_6_car.append(i.rstrip("\n"))

        ###### ouverture de fichier pour création liste de nuage de mots à 7 car nettoyée

        with open(
            r"C:\Users\crypt\Desktop\MetaBot_vF\Modules\Nuages_mots\mots_7_car.txt",
            "r",
        ) as BDD_7_car:
            liste_bdd_7 = BDD_7_car.readlines()

        liste_nettoyee_7 = liste_bdd_7

        for i in liste_nettoyee_7:
            liste_7_car.append(i.rstrip("\n"))

        ###### ouverture de fichier pour création liste de nuage de mots à 8 car nettoyée

        with open(
            r"C:\Users\crypt\Desktop\MetaBot_vF\Modules\Nuages_mots\mots_8_car.txt",
            "r",
        ) as BDD_8_car:
            liste_bdd_8 = BDD_8_car.readlines()

        liste_nettoyee_8 = liste_bdd_8

        for i in liste_nettoyee_8:
            liste_8_car.append(i.rstrip("\n"))

        #############################" Fonction nombre tirages par nuages de mots"

        def tirage():

            nombre_mots_tires = 0

            liste_tirage_mots = []

            liste_concatenation_mots = []

            ############# process 3 car (Nb mot aleatoire + shuffle + tirage nb mots)

            Tirage_nuage_3_car = randbelow(3)

            shuffle(liste_3_car)

            tirage3c = sample(liste_3_car, k=Tirage_nuage_3_car)

            ############## ajout du tirage nb de mots dans liste compilation

            liste_tirage_mots.extend(tirage3c)

            #######################

            Tirage_nuage_4_car = randint(1, 5)

            shuffle(liste_4_car)

            tirage4c = sample(liste_4_car, k=Tirage_nuage_4_car)

            ######################

            liste_tirage_mots.extend(tirage4c)

            ######################

            Tirage_nuage_5_car = randint(1, 5)

            shuffle(liste_5_car)

            tirage5c = sample(liste_5_car, k=Tirage_nuage_5_car)

            ######################

            liste_tirage_mots.extend(tirage5c)

            ######################

            Tirage_nuage_6_car = randint(1, 5)

            shuffle(liste_6_car)

            tirage6c = sample(liste_6_car, k=Tirage_nuage_6_car)

            ######################

            liste_tirage_mots.extend(tirage6c)

            ######################

            Tirage_nuage_7_car = randbelow(5)

            shuffle(liste_7_car)

            tirage7c = sample(liste_7_car, k=Tirage_nuage_7_car)

            ######################

            liste_tirage_mots.extend(tirage7c)

            ######################

            Tirage_nuage_8_car = randbelow(3)

            shuffle(liste_8_car)

            tirage8c = sample(liste_8_car, k=Tirage_nuage_8_car)

            ######################

            liste_tirage_mots.extend(tirage8c)

            ###################### DOUBLE SHUFFLE FINAL DES MOTS (hors somme tirage)
            shuffle(liste_tirage_mots)
            shuffle(liste_tirage_mots)
            #####################

            nombre_mots_tires = (
                Tirage_nuage_3_car
                + Tirage_nuage_4_car
                + Tirage_nuage_5_car
                + Tirage_nuage_6_car
                + Tirage_nuage_7_car
                + Tirage_nuage_8_car
            )

            if nombre_mots_tires == longueur_seed:
                return liste_tirage_mots
            else:
                return tirage()

        liste_mots_str = " ".join(tirage())

        def ecriture_fichier():

            connexionBDD = sqlite3.connect(
                r"C:\Users\crypt\Desktop\MetaBot_vF\MetaBDD.db"
            )

            curseur = connexionBDD.cursor()

            # Création de la requete qui créera la ligne SQL par clé

            ajout_iteration = (
                "INSERT INTO MetaBDDTable(seedId, seed, statutSeed) VALUES(?, ?, ?)"
            )

            # Renseigner les données intégrées à la requête

            infos_iteration = (curseur.lastrowid, liste_mots_str, statut_seed)

            # Exécution et application

            curseur.execute(ajout_iteration, infos_iteration)

            connexionBDD.commit()

            connexionBDD.close()

            return 1

        ecriture_fichier()

    i = 0
    while i < 1000:
        usine_cles()
        i += 1
        print("Le nombre de clés générées est de :", i)
    return 1

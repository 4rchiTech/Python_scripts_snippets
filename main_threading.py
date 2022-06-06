import script1_creation_BDD as script_1
import script2_Update_BDD as script_2
import script3_Initialisation_BDD_trading as script_3
import script4_Scanner_Trader as script_4

import ccxt
import sqlite3
import threading

import data.data_tuple_cex_module as data_tuples


liste_traitement = data_tuples.tuples_cex

# MAIN

fonctionnement = True

"""for i in liste_traitement:
    script_1.fonction_creation_chaines(i[0], i[1])
"""


def premier_process():
    while fonctionnement:
        for i in liste_traitement:
            script_2.fonction_scanner_chaines(i[0])
    return True


for i in liste_traitement:
    script_2.fonction_scanner_chaines(i[0])

"""
def second_process():
    while fonctionnement:
        for i in liste_source:
            script_3.initialisation_trading(i[0])
            time.sleep(20)
    return True


def troisieme_process():
    while fonctionnement:
        script_4.scanner_initialisation(1, 500)
        time.sleep(20)
    return True


def quatrieme_process():
    while fonctionnement:
        script_4.script_etape_A()
        script_4.script_veille()
        script_4.script_etape_B()
        script_4.script_veille()
        script_4.script_etape_C()
        script_4.script_veille()
    return True


try:

    premier_coeur = threading.Thread(target=premier_process)
    second_coeur = threading.Thread(target=second_process)
    troisieme_coeur = threading.Thread(target=troisieme_process)
    quatrieme_coeur = threading.Thread(target=quatrieme_process)

    premier_coeur.start()
    second_coeur.start()
    troisieme_coeur.start()
    quatrieme_coeur.start()

except Exception as e:
    print("Exception levée par le threading", e)
"""

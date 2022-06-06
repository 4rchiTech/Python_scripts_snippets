import sqlite3
import threading

my_lock = threading.RLock()


def premier_process(x=2, y=4):
    calcul = x + y
    ecriture(str(calcul))
    print("écriture ajoutée 1er process")
    return calcul


def troisieme_process(c=2, o=4):
    calcul3 = c + o
    ecriture(str(calcul3))
    print("écriture ajoutée 3ème process")
    return calcul3


def ecriture(item):
    with my_lock:
        try:
            connexionBDD2 = sqlite3.connect("test.db")
            curseur2 = connexionBDD2.cursor()
            ajout_chaines = "INSERT INTO test(ajout) VALUES(?)"
            maj = item
            curseur2.execute(ajout_chaines, maj)
            connexionBDD2.commit()
        except Exception as e:
            print(e)
            connexionBDD2.rollback()


fonctionnement = True

connexionBDD2 = sqlite3.connect("test.db")

try:
    while fonctionnement:
        premier_coeur = threading.Thread(target=premier_process)
        second_coeur = threading.Thread(target=troisieme_process)

        premier_coeur.start()
        second_coeur.start()
except Exception as e:
    print(e)
    connexionBDD2.close()

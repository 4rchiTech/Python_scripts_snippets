import csv

chemin_fichier = r"C:\Users\crypt\Desktop\export.csv"


def export_csv(input=None):
    data = ["coucou", "hello"]
    with open(chemin_fichier, "a") as fichier:
        ecriture = csv.writer(fichier, delimiter=",")
        ecriture.writerow(data)


export_csv(input=None)

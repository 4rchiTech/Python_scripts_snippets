# source : video youtube : https://www.youtube.com/watch?v=j9fO9-59EdI
# chiffrement sûr (à condition d'avoir une clé aléatoire et de longueur égale à la taille initiale du fichier à chiffrer)

from hashlib import sha256


entree = input(
    "entrez le nom du fichier à chiffrer ou déchiffrer"
)  # ex : fichier test.py dans local
sortie = input("entrez le nom du fichier de sortie")

key = input("entrez la clé")  # il faut garder la clé pour déchiffrer le fichier chiffré
keys = sha256(key.encode("utf-8")).digest()

with open(entree, "rb") as f_entree:
    with open(sortie, "wb") as f_sortie:
        i = 0
        while f_entree.peek():
            c = ord(f_entree.read(1))
            j = i % len(keys)
            b = bytes([c ^ keys[j]])
            f_sortie.write(b)
            i = i + 1

# coding:utf-8

from binance.client import Client

from statistics import mean

from math import sqrt

api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
api_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

client = Client(api_key, api_secret, testnet=False)

###################################################### EXTRACTION KLINES - Dernier cours de cloture - KLINE 1 MIN


def module_veille_bollinger():

    valeurClotureEMA = 0

    klineLastEnd = client.get_historical_klines(
        "BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 min ago UTC"
    )

    for colonneCloture in klineLastEnd:
        valeurClotureEMA = colonneCloture[4]

    ###################################################### MOYENNE MOBILE 20 BOUGIES

    dataMM20 = client.get_historical_klines(
        "BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "20 min ago UTC"
    )

    kline_cloture = dataMM20
    Nombre_seances = 20
    Sigma_clotures_seances = 0
    MM20 = 0

    for ValeurColonneCloture in kline_cloture:
        """
        print("Valeurs colonnes 5 : cours de cloture :", float(ValeurColonneCloture[4]))
        """
        ValeurCloturesExtraites = float(ValeurColonneCloture[4])
        Sigma_clotures_seances += ValeurCloturesExtraites
        MM20 = Sigma_clotures_seances // Nombre_seances
    """
	print("La moyenne mobile sur {} séances est de : {} $".format(Nombre_seances, MM20))
	"""

    ####################################################### Moyenne mobile exponentielle des 20 dernières bougies (cours de clôture)

    multiplicateur = 2 / (1 + 20)

    moyenneMobileExpo = float(valeurClotureEMA) * multiplicateur + MM20 * (
        1 - multiplicateur
    )
    """
	print("La moyenne mobile exponentielle est de ;", moyenneMobileExpo)
	"""

    ###################################################### MOYENNE DES PLUS BAS SUR 20 BOUGIES

    moyennnePlusBas20 = client.get_historical_klines(
        "BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "20 min ago UTC"
    )

    kline_plusbas = moyennnePlusBas20
    Sigma_plus_bas_seances = 0
    resMoyPlusBas20 = 0

    for ValeurColonnePlusBas in kline_plusbas:
        ValeurPlusBasExtraits = float(ValeurColonnePlusBas[3])
        Sigma_plus_bas_seances += ValeurPlusBasExtraits
        resMoyPlusBas20 = Sigma_plus_bas_seances // Nombre_seances
    """
	print("La moyenne des plus bas sur {} séances est de : {} $".format(Nombre_seances, resMoyPlusBas20))
	"""
    ###################################################### MOYENNE DES PLUS HAUT SUR 20 BOUGIES

    moyennnePlusHaut20 = client.get_historical_klines(
        "BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "20 min ago UTC"
    )

    kline_plushaut = moyennnePlusHaut20
    Sigma_plus_haut_seances = 0
    resMoyPlusHaut20 = 0

    for ValeurColonnePlusHaut in kline_plushaut:
        ValeurPlusHautExtraits = float(ValeurColonnePlusHaut[2])
        Sigma_plus_haut_seances += ValeurPlusHautExtraits
        resMoyPlusHaut20 = Sigma_plus_haut_seances // Nombre_seances
    """
	print("La moyenne des plus haut sur {} séances est de : {} $".format(Nombre_seances, resMoyPlusHaut20))
	"""

    ###################################################### BOLLINGER PERSONNALISE

    # Variables de bollinger :
    # Déviation = Moyenne mobile - cours de cloture
    # Ecart quadratique = deviation puissance 2
    # Ecart type = RACINE de (Moyenne des (plus haut - plus bas))

    ############################ VARIABLES

    deviation = moyenneMobileExpo - float(valeurClotureEMA)
    ecart_quadra = deviation**2
    ecart_type = sqrt(resMoyPlusHaut20 - resMoyPlusBas20)
    """
	print("L'écart type moyen sur 20 séances est de :", ecart_type)
	"""
    ############################ RESULTAT BOLLINGER PERSONNALISE

    bandeSuperieure = moyenneMobileExpo + (ecart_type * 2)
    """
	print("La limite de la bande supérieure de Bollinger est de :", bandeSuperieure)
	"""

    bandeInferieure = moyenneMobileExpo - (ecart_type * 2)
    """
	print("La limite de la bande inférieure de Bollinger est de :", bandeInferieure)
	"""
    carnet_ordre_premiere_ligne = client.get_orderbook_ticker(symbol="BTCUSDT")

    carnet_ordre_premiere_ligne_offre_achat = float(
        carnet_ordre_premiere_ligne["bidPrice"]
    )
    """
	print("Meilleur prix d'achat possible à cet instant :", round(carnet_ordre_premiere_ligne_offre_achat, 2))
	"""

    dernier_prix = client.get_symbol_ticker(symbol="BTCUSDT")
    """
	print("Dernier cours :", dernier_prix)
	"""

    extrac_dernier_prix = float(dernier_prix["price"])
    """
	print(extrac_dernier_prix)
	"""
    resultat_bollinger = 0

    if float(extrac_dernier_prix) > float(bandeInferieure) and float(
        extrac_dernier_prix
    ) < float(bandeSuperieure):
        resultat_bollinger = 1
        """
		print("Trading possible", resultat_bollinger)
		"""
    else:
        """
        print("Trading impossible", resultat_bollinger)
        """
    return resultat_bollinger

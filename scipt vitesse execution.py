import ccxt
import sqlite3
import time
import ast
import threading


###################### ACTUEL

start = time.time()
cex_cible = ccxt.binance()
symbol = "BTC/USDT"
symbol2 = "ETH/BTC"
symbol3 = "ETH/USDT"

pathA_check_paireA = cex_cible.fetch_order_book(symbol)["asks"][0][0]
pathA_check_paireB = cex_cible.fetch_order_book(symbol2)["asks"][0][0]
pathA_check_paireC = cex_cible.fetch_order_book(symbol3)["bids"][0][0]

print(pathA_check_paireA)
print(pathA_check_paireB)
print(pathA_check_paireC)

resultat_pathA = (
    (1 / pathA_check_paireA) * (1 / pathA_check_paireB) * pathA_check_paireC
)
resultat_pathA_round = round(resultat_pathA, 5)

print(resultat_pathA_round)

end = time.time()

print("performance :", end - start)

###################### TEST

startBIS = time.time()
cex_cible = ccxt.binance()
symbol = "BTC/USDT"
symbol2 = "ETH/BTC"
symbol3 = "ETH/USDT"

path_check_paireA = cex_cible.fetch_order_book(symbol)["asks"][0][0]
path_check_paireB = cex_cible.fetch_order_book(symbol2)["asks"][0][0]
path_check_paireC = cex_cible.fetch_order_book(symbol3)["bids"][0][0]

print(path_check_paireA)
print(path_check_paireB)
print(path_check_paireC)

resultat_path = round(
    (1 / path_check_paireA) * (1 / path_check_paireB) * path_check_paireC, 5
)

print(resultat_path)

endBIS = time.time()

print("performance :", endBIS - startBIS)

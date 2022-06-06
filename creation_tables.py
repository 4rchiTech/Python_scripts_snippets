import psycopg2


def create_tables():

    try:

        commands = (
            """
            CREATE TABLE bdd_trading (
                num SERIAL PRIMARY KEY,
                timestamp BIGINT NOT NULL,
                order_id_achat BIGINT,
                statut TEXT,
                prix_ordre NUMERIC,
                amount NUMERIC,
                order_id_vente TEXT,
                prix_liquidation NUMERIC
            )
            """,
            """
            CREATE TABLE bdd_indicateurs (
                cle_primaire SERIAL PRIMARY KEY,
                timestamp BIGINT NOT NULL,
                volume_MM18 NUMERIC,
                ratio_MM3_MM18 NUMERIC,
                ratio_MM6_MM18 NUMERIC,
                dernier_prix NUMERIC
            )
            """,
            """
            CREATE TABLE bdd_tresorerie (
                num SERIAL PRIMARY KEY,
                liquidity_available NUMERIC
            )
            """,
        )
        try:
            connexion = psycopg2.connect(
                host="localhost",
                database="dusteater_bdd_trading",
                user="postgres",
                password="archi",
            )

            cur = connexion.cursor()

            for command in commands:
                cur.execute(command)

            cur.close()
            connexion.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connexion is not None:
                connexion.close()

    except Exception as e:
        print(e)


###########################################


num = 1  # AUTOINCREMENTATION
timestamp = 154125741
order_id = 1784256545541
side = "achat"
statut = "running"
prix_ordre = 1.04544
amount = 145214
ordre_suivant = "aucun"
prix_liquidation = 5.145412


def insertion_BDD():

    insertion = """INSERT INTO bdd_trading(timestamp, order_id, side, statut, prix_ordre, amount, ordre_suivant, prix_liquidation) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"""
    data = (
        timestamp,
        order_id,
        side,
        statut,
        prix_ordre,
        amount,
        ordre_suivant,
        prix_liquidation,
    )
    try:
        connexion = psycopg2.connect(
            host="localhost",
            database="dusteater_bdd_trading",
            user="postgres",
            password="archi",
        )
        cur = connexion.cursor()
        cur.execute(insertion, data)
        connexion.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connexion is not None:
            connexion.close()
    return True


################################################ REQUETE BDD


def requete_BDD():
    """query parts from the parts table"""
    try:
        connexion = psycopg2.connect(
            host="localhost",
            database="dusteater_bdd_trading",
            user="postgres",
            password="archi",
        )
        cur = connexion.cursor()
        cur.execute("SELECT * FROM bdd_trading")
        rows = cur.fetchall()
        print("The number of parts: ", cur.rowcount)
        for row in rows:
            print(row)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if connexion is not None:
            connexion.close()


def requeteur(requete):

    try:
        connexion = psycopg2.connect(
            host="localhost",
            database="dusteater_bdd_trading",
            user="postgres",
            password="archi",
        )
        curseur = connexion.cursor()
        curseur.execute(requete)
        selection_BDD = curseur.fetchall()
        resultat = selection_BDD[0][0]
        connexion.close()

        return resultat

    except Exception as e:
        return e


###############################################################


def update_BDD():

    statut = "completed"
    order_id = 1784256545541
    update = """ UPDATE bdd_trading SET statut = %s WHERE order_id = %s"""
    contenu_update = (statut, order_id)

    try:
        connexion = psycopg2.connect(
            host="localhost",
            database="dusteater_bdd_trading",
            user="postgres",
            password="archi",
        )
        cur = connexion.cursor()
        cur.execute(update, contenu_update)
        connexion.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if connexion is not None:
            connexion.close()

    return True


############################################################### MAIN

if __name__ == "__main__":
    create_tables()

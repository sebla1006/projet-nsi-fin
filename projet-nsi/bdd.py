import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('./Database/niveau.db')

# Création d'un curseur
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS Profile (id INTEGER PRIMARY KEY, nom TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS Niveaux (id INTEGER PRIMARY KEY, nom TEXT)')

# Fermeture de la connexion
conn.close()

from cassandra.cluster import Cluster
import uuid

# Connexion à Cassandra
cluster = Cluster(['localhost'])
session = cluster.connect()

print(str(session))


# Création de la base de données
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS my_keyspace
    WITH replication = {
        'class': 'SimpleStrategy',
        'replication_factor': 1
    }
""")

# Sélection de la base de données
session.set_keyspace('my_keyspace')

# Création de la table Users
session.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY,
        name TEXT,
        age INT,
        email TEXT
    )
""")

def insert_user(session, name, age, email):
    user_id = uuid.uuid4()
    session.execute(
        """
        INSERT INTO users (id, name, age, email) 
        VALUES (%s, %s, %s, %s)
        """,
        (user_id, name, age, email)
    )
    print(f"Inserted User: {name}, Age: {age}, Email: {email}")


def fetch_users(session):
    rows = session.execute("SELECT * FROM users")
    for row in rows:
        print(f"ID: {row.id}, Name: {row.name}, Age: {row.age}, Email: {row.email}")


session.execute("""
 DROP KEYSPACE IF EXISTS my_keyspace;
 """)

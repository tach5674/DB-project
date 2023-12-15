import psycopg2


def connect_to_postgres():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="mypassword",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None


def create_database(conn):
    try:
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE canteen")

        conn.commit()
        cursor.close()
        print("Database 'canteen' created successfully")
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")


if __name__ == "__main__":
    connection = connect_to_postgres()

    if connection:
        create_database(connection)
        connection.close()
    else:
        print("Failed to connect to PostgreSQL server")

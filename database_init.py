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

        conn = psycopg2.connect(
            dbname="canteen",
            user="postgres",
            password="mypassword",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute("""
                        CREATE TABLE dishes (
                            id SERIAL PRIMARY KEY, 
                            name VARCHAR(50), 
                            price float(2),
                            category VARCHAR(50), 
                            calories INT, 
                            weight INT
                        )
                       """)

        cursor.execute("""
                        CREATE TABLE customers (
                            id SERIAL PRIMARY KEY, 
                            first_name VARCHAR(50),
                            second_name VARCHAR(50), 
                            age INT,
                            organisation VARCHAR(50),
                            preferences TEXT
                        )
                       """)

        cursor.execute("""
                        CREATE TABLE orders (
                            dish_id INT, 
                            customer_id INT, 
                            FOREIGN KEY (dish_id) REFERENCES dishes(id),
                            FOREIGN KEY (customer_id) REFERENCES customers(id), 
                            PRIMARY KEY (dish_id, customer_id),
                            time TIME, 
                            payment_method VARCHAR(50)
                        )
                       """)

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

import mysql.connector

def connect_to_mysql(host, user, password, database):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
        return None
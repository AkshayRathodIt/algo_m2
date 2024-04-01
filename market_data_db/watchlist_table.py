import mysql.connector
def create_watchlist_table(connection):
    try:
        cursor = connection.cursor()

        # Define the SQL query to create the watchlist table
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS watchlist (
            fyers_id VARCHAR(255) PRIMARY KEY,
            detail_symbol VARCHAR(255),
            minimum_lot_size INT,
            minimum_tick_size FLOAT,
            ISIN VARCHAR(255),
            Fyers_symbol VARCHAR(255),
            exchange INT,
            strategy VARCHAR(255)
        )
        '''

        # Execute the SQL query
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'watchlist' created successfully.")

    except mysql.connector.Error as error:
        print(f"Failed to create table: {error}")

def insert_into_watchlist(connection, data):
    try:
        cursor = connection.cursor()

        # Define the SQL query to insert a row into the 'watchlist' table
        insert_query = '''
        INSERT INTO watchlist (fyers_id, detail_symbol, minimum_lot_size, minimum_tick_size, ISIN, Fyers_symbol, exchange, strategy)
        VALUES (%(fyers_id)s, %(detail_symbol)s, %(minimum_lot_size)s, %(minimum_tick_size)s, %(ISIN)s, %(Fyers_symbol)s, %(exchange)s, %(strategy)s)
        '''

        # Execute the SQL query
        cursor.execute(insert_query, data)
        connection.commit()
        print("Row inserted successfully.")

    except mysql.connector.Error as error:
        print(f"Failed to insert row: {error}")


def delete_from_watchlist_by_fyers_symbol(connection, fyers_symbol):
    try:
        cursor = connection.cursor()

        # Define the SQL query to delete a row from the 'watchlist' table based on 'Fyers_symbol'
        delete_query = '''
        DELETE FROM watchlist WHERE Fyers_symbol = %(fyers_symbol)s
        '''

        # Execute the SQL query with the specified 'Fyers_symbol'
        cursor.execute(delete_query, {'fyers_symbol': fyers_symbol})
        connection.commit()

        # Check if any rows were affected by the deletion
        if cursor.rowcount > 0:
            print(f"Row with Fyers_symbol '{fyers_symbol}' deleted successfully.")
        else:
            print(f"No rows found with Fyers_symbol '{fyers_symbol}'.")

    except mysql.connector.Error as error:
        print(f"Failed to delete row: {error}")


def get_fyers_symbols_by_strategy(connection, strategy):
    try:
        cursor = connection.cursor()

        # SQL query to select Fyers_symbol for a specific strategy
        select_query = "SELECT Fyers_symbol FROM watchlist WHERE strategy = %s"

        # Execute the query with the strategy parameter
        cursor.execute(select_query, (strategy,))

        # Fetch all rows as a list of tuples and extract Fyers_symbol values
        fyers_symbols = [row[0] for row in cursor.fetchall()]

        cursor.close()

        return fyers_symbols

    except mysql.connector.Error as error:
        print(f"Failed to fetch Fyers_symbols: {error}")
        return []
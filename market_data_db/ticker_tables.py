import mysql.connector
import pandas as pd

def create_tables_for_tickres(connection, tickers_list):
    try:
        cursor = connection.cursor()

        for ticker in tickers_list:
            # Convert ticker name to the table name format (e.g., 'NSE:TCS-EQ' to 'TCS_EQ')
            table_name = ticker.replace(':', '_').replace('-', '_')

            # SQL query to create a table for each ticker
            create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                volume BIGINT,
                adj_close FLOAT,
                PRIMARY KEY (time_stamp)
            )
            '''

            # Execute the SQL query to create the table
            cursor.execute(create_table_query)
            print(f"Table '{table_name}' created successfully")

        # Commit changes to the database
        connection.commit()
        cursor.close()

    except mysql.connector.Error as error:
        print(f"Failed to create tables: {error}")



def insert_data_into_table(connection, dataframe, ticker_name):
    try:
        cursor = connection.cursor()

        # Convert ticker name to the table name format (e.g., 'NSE:TCS-EQ' to 'TCS_EQ')
        table_name = ticker_name.replace(':', '_').replace('-', '_')

        # SQL query to insert DataFrame values into the corresponding table
        insert_query = f'''
        INSERT INTO {table_name} (time_stamp, open, high, low, close, volume, adj_close)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''

        # Extract values from DataFrame and insert into the table row by row
        for index, row in dataframe.iterrows():
            values = (
                row['time_stamp'],
                row['open'],
                row['high'],
                row['low'],
                row['close'],
                row['volume'],
                row['adj_close']
            )
            cursor.execute(insert_query, values)

        # Commit changes to the database
        connection.commit()
        cursor.close()
        print(f"Data inserted into '{table_name}' table successfully")

    except mysql.connector.Error as error:
        print(f"Failed to insert data: {error}")


import mysql.connector


def get_data_for_specific_day(connection, ticker_name, specific_date):
    try:
        cursor = connection.cursor()

        # Convert ticker name to the table name format (e.g., 'NSE:TCS-EQ' to 'TCS_EQ')
        table_name = ticker_name.replace(':', '_').replace('-', '_')

        # SQL query to retrieve data for a specific day for a given ticker
        select_query = f'''
        SELECT *
        FROM {table_name}
        WHERE DATE(time_stamp) = %s
        '''

        # Execute the query with the specific date parameter
        cursor.execute(select_query, (specific_date,))

        # Fetch all rows from the result set
        result = cursor.fetchall()

        # Get column names from cursor description
        columns = [desc[0] for desc in cursor.description]

        cursor.close()

        # Convert result to a Pandas DataFrame
        df = pd.DataFrame(result, columns=columns)

        return df

    except mysql.connector.Error as error:
        print(f"Failed to retrieve data: {error}")
        return pd.DataFrame()  # Return an empty DataFrame on failure
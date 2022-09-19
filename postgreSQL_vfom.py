import psycopg2
from psycopg2 import Error
import pandas as pd

username = 'sms_user'
password = '!Vfoman@009988'

""" hostname = 'localhost'
port = '5431'
database = 'bulksmssend'

select(hostname, port, database, "SELECT version();") """


def select(hostname, port, database, cmd):

    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=hostname,
                                    port=port,
                                    database=database)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute(cmd)
        # Fetch result
        record = cursor.fetchall()
        print("You are connected to - ", record, "\n")
        return pd.read_sql_query(cmd, connection)

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def insert(hostname, port, database, cmd):
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=hostname,
                                    port=port,
                                    database=database)

        cursor = connection.cursor()
        # Executing a SQL query to insert data into  table
        insert_query = cmd
        cursor.execute(insert_query)
        connection.commit()
        print("1 Record inserted successfully")
        
        """ # Fetch result
        cursor.execute("SELECT * from mobile")
        record = cursor.fetchall()
        print("Result ", record)
        return record """

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def delete(hostname, port, database, cmd):
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=hostname,
                                    port=port,
                                    database=database)

        cursor = connection.cursor()
        # Executing a SQL query to delete table
        delete_query = cmd
        cursor.execute(delete_query)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record deleted successfully ")

        """ # Fetch result
        cursor.execute("SELECT * from mobile")
        print("Result ", cursor.fetchall()) """

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def update(hostname, port, database, cmd):
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=hostname,
                                    port=port,
                                    database=database)

        cursor = connection.cursor()
        # Executing a SQL query to update table
        update_query = cmd
        cursor.execute(update_query)
        connection.commit()
        count = cursor.rowcount
        print(count, " Record updated successfully ")

        """ # Fetch result
        cursor.execute("SELECT * from mobile")
        print("Result ", cursor.fetchall())
        """
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")















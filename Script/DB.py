import psycopg2
from psycopg2 import Error
import DB_read_file as a

try:
    connection = psycopg2.connect(user = a.user,
                                  password = a.passwd,
                                  host = a.host,
                                  port = a.port,
                                  database = a.db)
    cursor = connection.cursor()
    

    print("Table query successfully in PostgreSQL ")
    
except (Exception, psycopg2.DatabaseError) as error :   
    print ("Error while creating PostgreSQL table", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")





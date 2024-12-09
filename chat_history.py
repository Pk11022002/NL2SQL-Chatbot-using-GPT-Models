import os 
import mysql.connector
from mysql.connector import Error
from main import db_host, db_name, db_password, db_user

def insert_data(user_id: int, user_query: str, sql_query: str):
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        
        if conn.is_connected():
            print("Connected to the database")
            cursor = conn.cursor()
            query = "INSERT INTO nl2sql_audit_log (fk_user_id, user_question, generated_sql) VALUES (%s, %s, %s)"
            values = (user_id, user_query, sql_query)
            cursor.execute(query, values)
            conn.commit()
            
            print(f"Record inserted successfully into table.")  
    
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()
            print("MySQL connection is closed")

# data = insert_data(11,"Pranav", "sql query")

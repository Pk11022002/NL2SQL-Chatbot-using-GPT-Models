import pandas as pd
from main import db_host, db_name, db_password, db_user
import mysql.connector
import streamlit as st
from agent import agent
import requests

def execute_query(query):
    db = mysql.connector.connect(
                    host=db_host,
                    user=db_user,
                    password=db_password,
                    database=db_name
                )
    print("Database connection established.")

    cursor = db.cursor()

    try:
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        print("Columns:", columns)

        # Fetch all rows and convert to DataFrame
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=columns)
        return df
        #print("DataFrame:", df)

    except Exception as query_error:
        print("Error executing query or creating DataFrame:", query_error)
        # return pd.DataFrame({"Error": [str("No Data Found")]})
        return "No Data Found"
    
    finally:
        cursor.close()
        db.close()
        print("Database connection closed.")

def authenticate(email, password):
    url = "https://api.cloud.scogo.in:8080/v1/auth"
    payload = {
        "email": email,
        "password": password,
        "logged_in_from": "web"
    }
    response = requests.post(url, json=payload) 
    
    try:
        response_json = response.json()
        # print("response_json:", response_json)
        # customer_id = response_json['data']['user']['customer_id']
        #fk_user_id = response_json['data']['user']['id']
             
        if response.status_code == 200 and "data" in response_json and "token" in response_json["data"]:
            customer_id = response_json['data']['user'].get('customer_id')
            fk_user_id = response_json['data']['user']['id']

            if fk_user_id is not None:
                print("user_id:", fk_user_id)
                st.session_state['fk_user_id'] = fk_user_id
            
            if customer_id is not None:
                print("customer_id:", customer_id)
                st.session_state['customer_id'] = customer_id
            else:
                print("customer_id not found")

            return response_json["data"]["token"]
        else:
            return None
    except ValueError:
        st.error("Invalid response format")
        return None

# Function to check if user is authenticated
def is_authenticated():
    return "token" in st.session_state 


    


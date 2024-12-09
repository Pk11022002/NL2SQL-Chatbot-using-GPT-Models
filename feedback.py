import mysql.connector
from mysql.connector import Error
from main import db_host, db_name, db_password, db_user

def update_feedback_status(fk_user_id, feedback_type, prompt, query):

    # Determine feedback value based on user input
    if feedback_type == 'like':
        feedback_value = 1
    if feedback_type == 'dislike':
        feedback_value = 0

    try:
        # Establish database connection
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor()

        # Update query
        sql_query = """
        UPDATE nl2sql_audit_log
        SET feedback_status = %s
        WHERE fk_user_id = %s AND user_question = %s AND generated_sql = %s
        """
        # Execute the update query
        cursor.execute(sql_query, (feedback_value, fk_user_id, prompt, query))

        # Commit the changes
        connection.commit()
        
        # Optional: Provide feedback in the console or log
        print(f"Updated feedback_status to {feedback_value} for user_id {fk_user_id}")

    except mysql.connector.Error as err:
        # Handle errors (e.g., connection errors, execution errors)
        print(f"Error: {err}")
    finally:
        # Clean up and close the connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
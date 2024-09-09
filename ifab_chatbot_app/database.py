import psycopg2
from psycopg2 import sql
import os

# Database connection parameters
host = os.getenv('POSTGRES_HOST')
dbname =  os.getenv("POSTGRES_DB")
user =  os.getenv("POSTGRES_USER")
password =  os.getenv("POSTGRES_PASSWORD")




def init_db():   

    # SQL commands
    create_schema_sql = "CREATE SCHEMA IF NOT EXISTS ifab_rag;"
    create_table_sqls = [
    """
    CREATE TABLE IF NOT EXISTS ifab_rag.feedbacks (
        qna_id TEXT,
        feedback BOOLEAN, 
        insert_ts TIMESTAMP WITH TIME ZONE
    );
    """
    ,"""
    CREATE TABLE IF NOT EXISTS ifab_rag.qna (
		qna_id TEXT,
        question TEXT,
        answer TEXT,        
        insert_ts TIMESTAMP WITH TIME ZONE 
    );
    """
    ]



    # Establish the database connection
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host
        )

    # Create a cursor object using the cursor() method
    cur = conn.cursor()

    try:
        # Execute SQL commands
        cur.execute(create_schema_sql)

        # Commit the transaction
        conn.commit()

        for q in create_table_sqls:
            cur.execute(q)
            # Commit the transaction
            conn.commit()
        

        print("Schema and table created successfully.")
    
    except Exception as e:
        # Rollback in case there is any error
        conn.rollback()
        print("Failed to create schema and table:", e)
    
    finally:
        # Close communication with the database
        cur.close()
        conn.close()


# Function to insert a record into the feedbacks table
def insert_record_feedback(qna_id, feedback):
    insert_sql = """
    INSERT INTO ifab_rag.feedbacks (qna_id, feedback, insert_ts)
    VALUES (%s, %s, current_timestamp);
    """

        # Establish the database connection
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host
        ) 
    cur = conn.cursor()

    feedback_bl = None

    # if feedback == 1:
    #     feedback_bl = True
    # elif feedback == 0:
    #     feedback_bl = False
    
    try:
        # Execute the insertion command
        cur.execute(insert_sql, (qna_id, feedback))
        conn.commit()
        print("Record inserted successfully.")
    except Exception as e:
        conn.rollback()
        print("Failed to insert record:", e)
    finally:
        cur.close()
        conn.close()


# Function to insert a record into qna table
def insert_record_qna(qna_id, question, answer):
    insert_sql = """
    INSERT INTO ifab_rag.qna (qna_id, question, answer, insert_ts )
    VALUES (%s, %s, %s, current_timestamp);
    """

        # Establish the database connection
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host
        ) 
    cur = conn.cursor()  
    
    try:
        # Execute the insertion command
        cur.execute(insert_sql, (qna_id, question, answer))
        conn.commit()
        print("Record inserted successfully.")
    except Exception as e:
        conn.rollback()
        print("Failed to insert record:", e)
    finally:
        cur.close()
        conn.close()


def get_state():
    count_sql_positive = """
    SELECT COUNT(*) FROM ifab_rag.feedbacks WHERE feedback;
    """
    count_sql_negative = """
    SELECT COUNT(*) FROM ifab_rag.feedbacks WHERE NOT feedback;
    """

    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cur = conn.cursor()
    cnt_positive = 0
    cnt_negative = 0

    try:
        cur.execute(count_sql_positive)
        cnt_positive = cur.fetchone()[0]
        print(f"Count of positive feedback: {cnt_positive}")

        cur.execute(count_sql_negative)
        cnt_negative = cur.fetchone()[0]
        print(f"Count of positive feedback: {cnt_negative}")

    except Exception as e:
        print("Failed to count records:", e)
    finally:
        cur.close()
        conn.close()
    # return the feedback state from DB
    return {'cnt_positive':cnt_positive
            ,'cnt_negative':cnt_negative}


# initialize DB structure
init_db()
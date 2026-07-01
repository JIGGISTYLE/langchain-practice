import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

db_pass=os.getenv("DB_PASSWORD")

def get_connection():
    conn=psycopg2.connect(host="localhost",dbname="RAG",user="postgres",password=db_pass,port=6969)
    cur=conn.cursor()
    return conn,cur

def clean_up(conn,cur):
    conn.commit()
    cur.close()
    conn.close()

def initialize_table():
    conn,cur=get_connection()
    cur.execute("""CREATE TABLE IF NOT EXISTS chat_history(
                id SERIAL PRIMARY KEY,
                question TEXT, 
                answer TEXT, 
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
                """)
    clean_up(conn,cur)

def insert_message(question,answer):
    conn,cur=get_connection()
    cur.execute("""INSERT INTO chat_history(question,answer) VALUES (%s,%s); """,(question,answer))
    clean_up(conn,cur)

def get_history():
    conn,cur=get_connection()
    try:
        cur.execute(""" SELECT * FROM chat_history WHERE time >= NOW() - INTERVAL '24 hours' ORDER BY time ASC; """)
        chat_history=cur.fetchall()
        return chat_history
    finally:
        clean_up(conn,cur)
    
print(get_history())
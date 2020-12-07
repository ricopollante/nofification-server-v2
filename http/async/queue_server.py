import mysql.connector
import time
import requests
import threading
import socket
import time


while True:
    db_conn = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="iam100%pureROOT",
    database="cnmdb"
    )
    mycursor = db_conn.cursor()
    mycursor.execute("SELECT * from notifications")
    result = mycursor.fetchall()
    for result in result:
        print(result)
        try:
            #http(result[4])
            query = str("DELETE from notifications where id=") + str(result[0])
            mycursor.execute(query)
            db_conn.commit()
        except:
            pass

    db_conn.close()

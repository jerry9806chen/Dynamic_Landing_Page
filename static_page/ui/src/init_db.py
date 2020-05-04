import mysql.connector as mysql

# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST'] #Use localhost outside of docker. #'localhost' # different than inside the container and assumes default port of 3306

# Connect to the database
db = mysql.connect(host=db_host, database=db_name, user=db_user, password=db_pass)
cursor = db.cursor()
# Create table (wrapping it in a try-except is good practice)
#cursor.execute("drop table if exists users;")
try:
  cursor.execute("""
    CREATE TABLE Users (
      id    integer AUTO_INCREMENT PRIMARY KEY,
      fname VARCHAR(30) NOT NULL,
      lname VARCHAR(30) NOT NULL,
      email VARCHAR(30) NOT NULL,
    );
  """)
except:
  print("Users Table already exists. Not recreating it.")


#Insert Records
query = "insert into Users (fname, lname, email) values (%s, %s, %s)"
values = [
  ('Jerry','Chen','jerryjchen98@gmail.com')
]
cursor.executemany(query, values)
db.commit()

# Selecting Records
cursor.execute("select * from Users;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]
db.close()

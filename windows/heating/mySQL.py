import mysql.connector


try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ranger02?",
        database="mqtt"
    )
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))


mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)
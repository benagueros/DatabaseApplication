import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Janaifloyd0209!",
        database="mydatabase"
)


# mycursor = mydb.cursor()

# mycursor.execute("SHOW DATABASES")

# for x in mycursor:
#    print(x)

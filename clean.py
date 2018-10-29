import mysql.connector

mydb=mysql.connector.connect(
        host="localhost",
        user="HW3335",
        passwd="PW3335,
        database="mydatabase"
)

mycursor = mydb.cursor()

sql="DROP TABLE IF EXISTS "
table1="Experiment"
table2="ParametersTypes"
table3="ResultTypes"
table4="Runs"
table5="RunsParameter"
table6="RunsResult"

mycursor.execute(sql + table6)
mycursor.execute(sql + table5)
mycursor.execute(sql + table4)
mycursor.execute(sql + table3)
mycursor.execute(sql + table2)
mycursor.execute(sql + table1)



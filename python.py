import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Janaifloyd0209!",
        database="mydatabase"
)


mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE Experiment (ExperimentID VARCHAR(255) PRIMARY KEY, ManagerID CHAR(6), startDate DATE, DataEntryDate DATE)")


#in this table, need to set constraints on Type
mycursor.execute("CREATE TABLE ParametersTypes (ExperimentID VARCHAR(255) FOREIGN KEY REFERENCES Experiment(ExperimentID), ParameterName VARCHAR(255) PRIMARY KEY, Type VARCHAR(255), Required BOOLEAN)")

mycursor.execute("CREATE TABLE ResultTypes (ExperimentID VARCHAR(255) FOREIGN KEY REFERENCES Experiment(ExperimentID), ")




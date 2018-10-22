import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Janaifloyd0209!",
        database="mydatabase"
)


mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE Experiment(ExperimentID VARCHAR(255) PRIMARY KEY, ManagerID CHAR(6), startDate DATE, DataEntryDate DATE)")


#in this table, need to set constraints on Type
mycursor.execute("CREATE TABLE ParametersTypes(ExperimentID VARCHAR(255), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID), ParameterName VARCHAR(255) PRIMARY KEY, Type VARCHAR(255), Required BOOLEAN)")

#in this table, need to set constraints on Type
mycursor.execute("CREATE TABLE ResultTypes(ExperimentID VARCHAR(255), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID), ResultName VARCHAR(255) PRIMARY KEY, Type VARCHAR(255), Required BOOLEAN)")

mycursor.execute("CREATE TABLE Runs(ExperimentID VARCHAR(255), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID), TimeOfRun DATETIME PRIMARY KEY, ExperimentSSN CHAR(6), Success BOOLEAN)")

mycursor.execute("CREATE TABLE RunsParameter(ExperimentID VARCHAR(255), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID), TimeOfRun DATETIME, ParameterName VARCHAR(255), Value VARCHAR(255), KEY(TimeOfRun, ParameterName))")

mycursor.execute("CREATE TABLE RunsResult(ExperimentID VARCHAR(255), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID), TimeOfRun DATETIME, ResultName VARCHAR(255), Value VARCHAR(255), KEY(TimeOfRun, ResultName))")


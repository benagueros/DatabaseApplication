import mysql.connector

def buildTables(mycursor):
	mycursor.execute("CREATE TABLE Experiment(ExperimentID VARCHAR(255) PRIMARY KEY, ManagerID CHAR(6), startDate DATE, DataEntryDate DATE)")
	#in this table, need to set constraints on Type
	mycursor.execute("CREATE TABLE ParametersTypes(ExperimentID VARCHAR(255), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID), ParameterName VARCHAR(255), Type VARCHAR(255) CHECK (Type IN ('INT', 'FLOAT', 'STRING', 'URL', 'DATE', 'DATETIME')), Required BOOLEAN, KEY(ExperimentID, ParameterName))")
	#in this table, need to set constraints on Type
	mycursor.execute("CREATE TABLE ResultTypes(ExperimentID VARCHAR(255), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID), ResultName VARCHAR(255), Type VARCHAR(255) CHECK (Type IN ('INT', 'FLOAT', 'STRING', 'URL', 'DATE', 'DATETIME')), Required BOOLEAN, KEY(ExperimentID, ResultName))")
	mycursor.execute("CREATE TABLE Runs(ExperimentID VARCHAR(255), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID), TimeOfRun DATETIME, ExperimentSSN CHAR(6), Success BOOLEAN, KEY(ExperimentID, TimeOfRun))")
	mycursor.execute("CREATE TABLE RunsParameter(ExperimentID VARCHAR(255), TimeOfRun DATETIME, FOREIGN KEY(ExperimentID, TimeOfRun) REFERENCES Runs(ExperimentID, TimeOfRun), ParameterName VARCHAR(255), FOREIGN KEY(ExperimentID, ParameterName) REFERENCES ParametersTypes(ExperimentID, ParameterName),Value VARCHAR(255), KEY(ExperimentID, TimeOfRun, ParameterName))")
	mycursor.execute("CREATE TABLE RunsResult(ExperimentID VARCHAR(255), TimeOfRun DATETIME, ResultName VARCHAR(255), FOREIGN KEY(ExperimentID, TimeOfRun) REFERENCES Runs(ExperimentID, TimeOfRun), FOREIGN KEY(ExperimentID, ResultName) REFERENCES ResultTypes(ExperimentID, ResultName), Value VARCHAR(255), KEY(ExperimentID, TimeOfRun, ResultName))")

def destroyTables(mycursor):
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



mydb = mysql.connector.connect(
	host="localhost",
    user="root",
    passwd="Janaifloyd0209!",
    database="mydatabase"
	)
	
mycursor = mydb.cursor()
buildTables(mycursor)
destroyTables(mycursor)


import mysql.connector
import datetime
import sys

def buildTables(mycursor):
	mycursor.execute("CREATE TABLE Experiment(ExperimentID VARCHAR(255) PRIMARY KEY, ManagerID CHAR(6), startDate DATE, DataEntryDate DATE)")
	mycursor.execute("CREATE TABLE ParametersTypes(ExperimentID VARCHAR(255), ParameterName VARCHAR(255), Type VARCHAR(255), Required BOOLEAN, KEY(ExperimentID, ParameterName), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID), CONSTRAINT CHK_Type CHECK (Type IN ('INT', 'FLOAT', 'STRING', 'URL', 'DATE', 'DATETIME')))")
	mycursor.execute("CREATE TABLE ResultTypes(ExperimentID VARCHAR(255), ResultName VARCHAR(255), Type VARCHAR(255), Required BOOLEAN, KEY(ExperimentID, ResultName), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID), CONSTRAINT CHK_Type CHECK (Type IN ('INT', 'FLOAT', 'STRING', 'URL', 'DATE', 'DATETIME')))")
	mycursor.execute("CREATE TABLE Runs(ExperimentID VARCHAR(255), TimeOfRun DATETIME, ExperimenterSSN CHAR(6), Success BOOLEAN, KEY(ExperimentID, TimeOfRun), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID))")
	mycursor.execute("CREATE TABLE RunsParameter(ExperimentID VARCHAR(255), TimeOfRun DATETIME, ParameterName VARCHAR(255), Value VARCHAR(255), KEY(ExperimentID, TimeOfRun, ParameterName), FOREIGN KEY(ExperimentID, TimeOfRun) REFERENCES Runs(ExperimentID, TimeOfRun), FOREIGN KEY(ExperimentID, ParameterName) REFERENCES ParametersTypes(ExperimentID, ParameterName))")
	mycursor.execute("CREATE TABLE RunsResult(ExperimentID VARCHAR(255), TimeOfRun DATETIME, ResultName VARCHAR(255), Value VARCHAR(255), KEY(ExperimentID, TimeOfRun, ResultName), FOREIGN KEY(ExperimentID, TimeOfRun) REFERENCES Runs(ExperimentID, TimeOfRun), FOREIGN KEY(ExperimentID, ResultName) REFERENCES ResultTypes(ExperimentID, ResultName))")

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
#buildTables(mycursor)


while True:
	print("What would you like to do?")
	print("1. Experiment entry")
	print("2. Run Entry")
	choice = int(input(""))
	if choice != 1 and choice != 2:
		print("Invalid Choice")
		print("")
	else:
		break

print("")

#entering experiment information
if choice == 1:
	ExperimentID = input("Enter ExperimentID: ")
	ManagerID = input("Enter ManagerID: ")
	print("Enter StartDate")
	
	try:
		Month = int(input("   Enter Month: "))
		Day = int(input("   Enter Day: "))
		Year = int(input("   Enter Year: "))
	except:
		print("")
		print("MUST ENTER INTEGER VALUE. EXITING PROGRAM...")
		destroyTables(mycursor)
		sys.exit(-1)
		
	try:	
		date1 = datetime.date(Year, Month, Day)
	except:
		print("")
		print("INVALID DATE. MUST BE  DAY(1-31) MONTH(1-12) YEAR(YYYY). EXITING PROGRAM...")
		destroyTables(mycursor)
		sys.exit(-2)

	print("Enter DataEntryDate")
	
	try:
		Month = int(input("   Enter Month: "))
		Day = int(input("   Enter Day: "))
		Year = int(input("   Enter Year: "))
		print("")
	except:
		print("")
		print("MUST ENTER INTEGER VALUE. EXITING PROGRAM...")
		destroyTables(mycursor)
		sys.exit(-1)
	
	try:	
		date2 = datetime.date(Year, Month, Day)
	except:
		print("")
		print("INVALID DATE. MUST BE  DAY(1-31) MONTH(1-12) YEAR(YYYY). EXITING PROGRAM...")
		destroyTables(mycursor)
		sys.exit(-2)
	
	if date1  > datetime.date.today():
		print("")
		print("START DATE IS IN THE FUTURE. EXITING PROGRAM...")
		destroyTables(mycursor)
		sys.exit(-2)
	elif date2 > datetime.date.today():
		print("")
		print("DATA ENTRY DATE IS IN THE FUTURE. EXITING PROGRAM...")
		destroyTables(mycursor)
		sys.exit(-2)
	elif date1 > date2:
		print("")
		print("START DATE IS BEFORE DATA ENTRY DATE. EXITING PROGRAM...")
		destroyTables(mycursor)
		sys.exit(-2)
		
	try:
		parameters = int(input("How many parameters are there? "))
	except:
		print("")
		print("MUST ENTER INTEGER VALUE. EXITING PROGRAM...")
		destroyTables(mycursor)
		sys.exit(-1)
	
	sql = "INSERT INTO Experiment(ExperimentID, ManagerID, StartDate, DataEntryDate) VALUES (%s, %s, %s, %s)"
	val = (ExperimentID, ManagerID, date1, date2)
	mycursor.execute(sql, val)
	mydb.commit()
	
	
	
	
	while parameters > 0:
		ParameterName = input("Enter ParameterName: ")
		#The CHECK is ignored for some reason so this constraint is still vulnerable
		Type = input("Enter Type: ")
			
		Required = input("Is It Required? (y/n):  ")
		
		if Required == "y":
			Required = 1
		elif Required == "n":
			Required = 0
		else:
			print("")
			print("INVALID INPUT. MUST ENTER y or n. EXITING PROGRAM...")
			destroyTables(mycursor)
			sys.exit(-3)
		
	
		sql = "INSERT INTO ParametersTypes(ExperimentID, ParameterName, Type, Required) VALUES (%s, %s, %s, %s)"
		val = (ExperimentID, ParameterName, Type, Required)
		
		mycursor.execute(sql, val)	
		mydb.commit()
		print(mycursor.rowcount, "record inserted.")
		print("")
		
		
		parameters-=1
		#probably use execute many function
	

if choice == 2:
	ExperimentID = input("Enter ExperimentID: ")
	print("Enter TimeOfRun")
	try:
		Month = int(input("   Enter Month: "))
		Day = int(input("   Enter Day: "))
		Year = int(input("   Enter Year: "))
	except:
		print("")
		print("MUST ENTER INTEGER VALUE. EXITING PROGRAM...")
		destroyTables(mycursor)
		sys.exit(-1)
		
	try:	
		TimeOfRun = datetime.date(Year, Month, Day)
	except:
		print("")
		print("INVALID DATE. MUST BE  DAY(1-31) MONTH(1-12) YEAR(YYYY). EXITING PROGRAM...")
		destroyTables(mycursor)
		sys.exit(-2)
	
	ExperimenterSSN = input("Enter ExperimenterSSN: ")
	Success = input("Was the run successful?(y/n) ")
	if Success == "y":
			Success = 1
	elif Success == "n":
			Success = 0
	else:
			print("")
			print("INVALID INPUT. MUST ENTER y or n. EXITING PROGRAM...")
			destroyTables(mycursor)
			sys.exit(-3)
	
	sql = "INSERT INTO Runs(ExperimentID, TimeOfRun, ExperimenterSSN, Success) VALUES (%s, %s, %s, %s)"
	val = (ExperimentID, TimeOfRun, ExperimenterSSN, Success)
	mycursor.execute(sql, val)
	mydb.commit()



#destroyTables(mycursor)

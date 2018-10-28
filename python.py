import mysql.connector
import datetime
import sys

def buildTables(mycursor):
	mycursor.execute("CREATE TABLE Experiment(ExperimentID VARCHAR(255) PRIMARY KEY, ManagerID CHAR(6), startDate DATE, DataEntryDate DATE)")
	mycursor.execute("CREATE TABLE ParametersTypes(ExperimentID VARCHAR(255), ParameterName VARCHAR(255), Type VARCHAR(255), Required BOOLEAN, KEY(ExperimentID, ParameterName), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID))")
	mycursor.execute("CREATE TABLE ResultTypes(ExperimentID VARCHAR(255), ResultName VARCHAR(255), Type VARCHAR(255), Required BOOLEAN, KEY(ExperimentID, ResultName), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID))")
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

def createProcedure(mycursor):
	#mycursor.execute("CREATE PROCEDURE checkTypes (IN Type VARCHAR(255)) BEGIN IF Type != %s AND Type != %s AND Type != %s AND Type != %s AND Type != %s AND Type != %s THEN BEGIN SIGNAL SQLSTATE %s SET MESSAGE_TEXT = %s; END; END IF; END", ("INT", "FLOAT", "STRING", "URL", "DATE", "DATETIME", "0700C","INVALID VALUE FOR Type"))
	mycursor.execute("CREATE TRIGGER paramtypes BEFORE INSERT ON ParametersTypes FOR EACH ROW BEGIN CALL checkTypes(new.Type); END") 
	mycursor.execute("CREATE TRIGGER paramtypesupdate BEFORE UPDATE ON ParametersTypes FOR EACH ROW BEGIN CALL checkTypes(new.Type); END")
	mycursor.execute("CREATE TRIGGER resulttypes BEFORE INSERT ON ResultTypes FOR EACH ROW BEGIN CALL checkTypes(new.Type); END") 
	mycursor.execute("CREATE TRIGGER resulttypesupdate BEFORE UPDATE ON ResultTypes FOR EACH ROW BEGIN CALL checkTypes(new.Type); END")
	
def enterExperiment(mycursor):
	#Enter into Experiment Table
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
	
	#Enter into ParametersTypes Table
	while parameters > 0:
		ParameterName = input("Enter ParameterName: ")
		
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

	try:
		results = int(input("How many results will there be? "))
	except:
		print("")
		print("MUST ENTER INTEGER VALUE. EXITING PROGRAM...")
		destroyTables(mycursor)
		sys.exit(-1)
	
	#Enter into ResultParameters Table	
	while results > 0:
		ResultName = input("Enter ResultName: ")
		
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
			
		sql = "INSERT INTO ResultTypes(ExperimentID, ResultName, Type, Required) VALUES (%s, %s, %s, %s)"
		val = (ExperimentID, ResultName, Type, Required)
		mycursor.execute(sql, val)	
		mydb.commit()
		print(mycursor.rowcount, "record inserted.")
		print("")
		
		results-=1
			
def enterRun(mycursor):
	#Enter into Runs Table
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
	
	#Enter into RunsParameter Table needs to be consistent with experiment table
	#Foreign Key Constraints handle the input of data here
	#Still need to check required status
	#Use the data in the parameters types table with the same Experiment id to askl the user for the appropriate data
	
	#Do a query on the parameterstype table using the given experiment id to find all parameter
	mycursor.execute("SELECT * FROM ParametersTypes WHERE ExperimentID = %s", ExperimentID)
	myresult = myscursor.fetchall()
	for x in myresult:
		ParameterName = x['ParameterName']
		sql = "INSERT INTO RunsParameter(ExperimentID, TimeOfRun, ParameterName, Value) VALUE(%s, %s, %s, %s)"
		if x['Required'] == 1:
			Value = input("Enter the value of parameter %s", ParameterName)
			val = (ExperimentID, TimeOfRun, ParamerterName, Value)
			mycursor.execute(sql, val)
		else:
			ans = input("Was %s entered? (y/n) ", ParameterName)
			while ans != 'y' and ans != 'n':
				print("Invalid response. Please try again.")
				ans = input("Was %s entered? (y/n) ", ParameterName)
			if ans == 'y':
				Value = input("Enter the value of parameter %s", ParameterName)
				val = (ExperimentID, TimeOfRun, ParamerterName, Value)
				mycursor.execute(sql, val)
	
	
	#Enter into RunsResultTable
	#Do a query on just like above but on Result
	
	mycursor.execute("SELECT * FROM ResultTypes WHERE ExperimentID = %s", ExperimentID)
	myresult = mycursor.fetchall()
	for x in myresult:
		ResultName = x['ResultName']
		sql = "INSERT INTO RunsResult(ExperimentID, TimeOfRun, ResultName, Value) VALUE(%s, %s, %s, %s)"
		if x['Required'] == 1 
			Value = input("Enter the value of result %s", ResultName)
			val = (ExperimentID, TimeOfRun, ResultName, Value)
			mycursor.execute(sql, val)
		else:
			ans = input("Was %s entered? (y/n) ", ResultName)
			while ans != 'y' and ans!= 'n':
				print("Invalid response. Please try again.")
				ans = input("Was %s entered? (y/n) ", ResultName)
			if ans == 'y':
				Value = input("Enter the value of parameter %s", ParameterName)
				val = (ExperimentID, TimeOfRun, ParamerterName, Value)
				mycursor.execute(sql, val)

mydb = mysql.connector.connect(
	host="localhost",
    user="root",
    passwd="Janaifloyd0209!",
    database="mydatabase"
	)
	
mycursor = mydb.cursor()
buildTables(mycursor)
createProcedure(mycursor)


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

if choice == 1:
	enterExperiment(mycursor)
	
if choice == 2:
	enterRun(mycursor)
	



#destroyTables(mycursor)

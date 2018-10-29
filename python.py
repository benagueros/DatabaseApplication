import mysql.connector
import datetime
import sys

def buildDB():

	mydb = mysql.connector.connect(
		host="localhost",
    		user="HW3335",
    		passwd="PW3335"
	)
	
	mycursor = mydb.cursor()
	mycursor.execute("CREATE DATABASE IF NOT EXISTS Experiment")
	
	mydb = mysql.connector.connect(
		host="localhost",
    		user="HW3335",
    		passwd="PW3335",	
		database="Experiment"
	)
	
	mycursor = mydb.cursor()
	mycursor.execute("CREATE TABLE IF NOT EXISTS Experiment(ExperimentID VARCHAR(255) PRIMARY KEY, ManagerID CHAR(6), startDate DATE, DataEntryDate DATE)")
	mycursor.execute("CREATE TABLE IF NOT EXISTS ParametersTypes(ExperimentID VARCHAR(255), ParameterName VARCHAR(255), Type VARCHAR(255), Required BOOLEAN, UNIQUE KEY(ExperimentID, ParameterName), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID))")
	mycursor.execute("CREATE TABLE IF NOT EXISTS ResultTypes(ExperimentID VARCHAR(255), ResultName VARCHAR(255), Type VARCHAR(255), Required BOOLEAN, UNIQUE KEY(ExperimentID, ResultName), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID))")
	mycursor.execute("CREATE TABLE IF NOT EXISTS Runs(ExperimentID VARCHAR(255), TimeOfRun DATETIME, ExperimenterSSN CHAR(6), Success BOOLEAN, UNIQUE KEY(ExperimentID, TimeOfRun), FOREIGN KEY(ExperimentID) REFERENCES Experiment(ExperimentID))")
	mycursor.execute("CREATE TABLE IF NOT EXISTS RunsParameter(ExperimentID VARCHAR(255), TimeOfRun DATETIME, ParameterName VARCHAR(255), Value VARCHAR(255), UNIQUE KEY(ExperimentID, TimeOfRun, ParameterName), FOREIGN KEY(ExperimentID, TimeOfRun) REFERENCES Runs(ExperimentID, TimeOfRun), FOREIGN KEY(ExperimentID, ParameterName) REFERENCES ParametersTypes(ExperimentID, ParameterName))")
	mycursor.execute("CREATE TABLE IF NOT EXISTS RunsResult(ExperimentID VARCHAR(255), TimeOfRun DATETIME, ResultName VARCHAR(255), Value VARCHAR(255), UNIQUE KEY(ExperimentID, TimeOfRun, ResultName), FOREIGN KEY(ExperimentID, TimeOfRun) REFERENCES Runs(ExperimentID, TimeOfRun), FOREIGN KEY(ExperimentID, ResultName) REFERENCES ResultTypes(ExperimentID, ResultName))")
	return mycursor
	
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
	mycursor.execute("DROP PROCEDURE IF EXISTS checkTypes")
	mycursor.execute("CREATE PROCEDURE checkTypes (IN Type VARCHAR(255)) BEGIN IF Type != %s AND Type != %s AND Type != %s AND Type != %s AND Type != %s AND Type != %s THEN BEGIN SIGNAL SQLSTATE %s SET MESSAGE_TEXT = %s; END; END IF; END", ("INT", "FLOAT", "STRING", "URL", "DATE", "DATETIME", "0700C","INVALID VALUE FOR Type"))
	mycursor.execute("DROP TRIGGER IF EXISTS paramtypes")
	mycursor.execute("CREATE TRIGGER paramtypes BEFORE INSERT ON ParametersTypes FOR EACH ROW BEGIN CALL checkTypes(new.Type); END") 
	mycursor.execute("DROP TRIGGER IF EXISTS paramtypesupdate")
	mycursor.execute("CREATE TRIGGER paramtypesupdate BEFORE UPDATE ON ParametersTypes FOR EACH ROW BEGIN CALL checkTypes(new.Type); END")
	mycursor.execute("DROP TRIGGER IF EXISTS resulttypes")
	mycursor.execute("CREATE TRIGGER resulttypes BEFORE INSERT ON ResultTypes FOR EACH ROW BEGIN CALL checkTypes(new.Type); END") 
	mycursor.execute("DROP TRIGGER IF EXISTS resulttypesupdate")
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
		sys.exit(-1)
		
	try:	
		date1 = datetime.date(Year, Month, Day)
	except:
		print("")
		print("INVALID DATE. MUST BE  DAY(1-31) MONTH(1-12) YEAR(YYYY). EXITING PROGRAM...")
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
		sys.exit(-2)
		
	elif date2 > datetime.date.today():
		print("")
		print("DATA ENTRY DATE IS IN THE FUTURE. EXITING PROGRAM...")
		sys.exit(-2)
		
	elif date1 > date2:
		print("")
		print("START DATE IS BEFORE DATA ENTRY DATE. EXITING PROGRAM...")
		sys.exit(-2)
		
	sql = "INSERT INTO Experiment(ExperimentID, ManagerID, StartDate, DataEntryDate) VALUES (%s, %s, %s, %s)"
	val = (ExperimentID, ManagerID, date1, date2)
	mycursor.execute(sql, val)
	mydb.commit()
	
	#Enter into ParametersTypes Table
	try:
		parameters = int(input("How many parameters are there? "))
	except:
		print("")
		print("MUST ENTER INTEGER VALUE. EXITING PROGRAM...")
		sys.exit(-1)
	
	while parameters > 0:
		ParameterName = input("Enter ParameterName: ")
		Type = input("Enter Type: ")
		Required = input("Is It Required? (y/n):  ")
		
		while Required != 'y' and Required != 'n':
			print("Invalid input. Try again.")
			Required = input("Is it Required? (y/n): ")
			
		if Required == "y":
			Required = 1
		else: 
			Required = 0
	
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
		sys.exit(-1)
	
	#Enter into ResultParameters Table	
	while results > 0:
		ResultName = input("Enter ResultName: ")
		Type = input("Enter Type: ")
		Required = input("Is It Required? (y/n):  ")
		
		while Required != 'y' and Required != 'n':
			print("Invalid input. Try Again.")
			Required = input("Is It Required? (y/n):  ")
			
		if Required == "y":
			Required = 1
		else:
			Required = 0
			
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
		sys.exit(-1)
		
	try:	
		TimeOfRun = datetime.date(Year, Month, Day)
	except:
		print("")
		print("INVALID DATE. MUST BE  DAY(1-31) MONTH(1-12) YEAR(YYYY). EXITING PROGRAM...")
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
			sys.exit(-3)
	
	sql = "INSERT INTO Runs(ExperimentID, TimeOfRun, ExperimenterSSN, Success) VALUES (%s, %s, %s, %s)"
	val = (ExperimentID, TimeOfRun, ExperimenterSSN, Success)
	mycursor.execute(sql, val)
	mydb.commit()
	
	#Enter into RunParameters Table
	mycursor.execute("SELECT * FROM ParametersTypes WHERE ExperimentID = %s", (ExperimentID,))
	myresult = mycursor.fetchall()
	for x in myresult:
		ParameterName = x[1]
		sql = "INSERT INTO RunsParameter(ExperimentID, TimeOfRun, ParameterName, Value) VALUE(%s, %s, %s, %s)"
		if x[3] == 1:
			print("Enter the value of parameter", ParameterName)
			Value = input("")
			val = (ExperimentID, TimeOfRun, ParameterName, Value)
			mycursor.execute(sql, val)
		else:
			print("Was", ParameterName,"entered? (y/n) ")
			ans = input("")
			while ans != 'y' and ans != 'n':
				print("Invalid response. Please try again.")
				print("Was", ParameterName,"entered? (y/n) ")
				ans = input("")
			if ans == 'y':
				print("Enter the value of parameter", ParameterName)
				Value = input("")
				val = (ExperimentID, TimeOfRun, ParamerterName, Value)
				mycursor.execute(sql, val)
	
	
	#Enter into RunsResultTable
	if Success == 1:
		mycursor.execute("SELECT * FROM ResultTypes WHERE ExperimentID = %s", (ExperimentID,))
		myresult = mycursor.fetchall()
		for x in myresult:
			ResultName = x[1]
			sql = "INSERT INTO RunsResult(ExperimentID, TimeOfRun, ResultName, Value) VALUE(%s, %s, %s, %s)"
			if x[3] == 1:
				print("Enter the value of result", ResultName)
				Value = input("")
				val = (ExperimentID, TimeOfRun, ResultName, Value)
				mycursor.execute(sql, val)
			else:
				print("Was", ResultName, "determined? (y/n) ")
				ans = input("")
				while ans != 'y' and ans!= 'n':
					print("Invalid response. Please try again.")
					print("Was", ResultName, "determined? (y/n) ")
					ans = input("")
				if ans == 'y':
					print("Enter the value of result", ResultName)
					Value = input("")
					val = (ExperimentID, TimeOfRun, ResultName, Value)
					mycursor.execute(sql, val)

def viewExperiment(mycursor):
	ExperimentID = input("Enter the desired ExperimentID: ")
	mycursor.execute("SELECT * FROM Experiment WHERE ExperimentID = %s", (ExperimentID,))
	myresult = mycursor.fetchall()
	
	if mycursor.rowcount != 0:
		print("Experiment", ExperimentID)
		for x in myresult:
			print("	Manager:", x[1])
			print("	Start Date:", x[2])
			print("	Entry Date:", x[3])
	else:
		print("Invalid Experiment ID.")
		return	
		
	mycursor.execute("SELECT * FROM ParametersTypes WHERE ExperimentID = %s", (ExperimentID,))
	myresult = mycursor.fetchall()
	if mycursor.rowcount != 0:
		print("	Parameters:")
		for x in myresult:
			if x[3] == 1:
				required="Required"
			else:
				required="Not Required" 
			print("		", x[1], x[2], required)
	else:
		print("No Parameters.")	
		
	mycursor.execute("SELECT * FROM ResultTypes WHERE ExperimentID = %s", (ExperimentID,))
	myresult = mycursor.fetchall()
	if mycursor.rowcount != 0:
		print("	Results: ")
		for x in myresult:
			if x[3] == 1:
				required="Required"
			else:
				required="Not Required" 
			print("		", x[1], x[2], required)
	else:
		print("No Results.")

#need to finish modifying this funciton	
def viewRun(mycursor)	
	ExperimentID = input("Enter the desired ExperimentID: ")
	mycursor.execute("SELECT * FROM Runs WHERE ExperimentID = %s", (ExperimentID,))
	myresult = mycursor.fetchall()
	
	if mycursor.rowcount != 0:
		print("Experiment", ExperimentID)
		for x in myresult:
			print("	Time of run:", x[1])
			print("	Experimenter SSN:", x[2])
			if x[3] == 0:
				Success = "Success"
			else:
				Success = "Failure"
			print("	", Success) #specifically stopped here
	else:
		print("Invalid Experiment ID.")
		return	
		
	mycursor.execute("SELECT * FROM ParametersTypes WHERE ExperimentID = %s", (ExperimentID,))
	myresult = mycursor.fetchall()
	if mycursor.rowcount != 0:
		print("	Parameters:")
		for x in myresult:
			if x[3] == 1:
				required="Required"
			else:
				required="Not Required" 
			print("		", x[1], x[2], required)
	else:
		print("No Parameters.")	
		
	mycursor.execute("SELECT * FROM ResultTypes WHERE ExperimentID = %s", (ExperimentID,))
	myresult = mycursor.fetchall()
	if mycursor.rowcount != 0:
		print("	Results: ")
		for x in myresult:
			if x[3] == 1:
				required="Required"
			else:
				required="Not Required" 
			print("		", x[1], x[2], required)
	else:
		print("No Results.")
	
	
	
	
buildDB()

mydb = mysql.connector.connect(
		host="localhost",
    		user="HW3335",
    		passwd="PW3335",	
		database="Experiment"
	)
	
mycursor = mydb.cursor()

createProcedure(mycursor)
	
while True:
	while True:
		print("What would you like to do?")
		print("1. Experiment entry")
		print("2. Run Entry")
		print("3. View Experiment Info")
		print("4. View Run Info")
		choice = int(input(""))
		if choice != 1 and choice != 2 and choice != 3 and choice != 4:
			print("Invalid Choice")
			print("")
		else:
			break

	print("")

	if choice == 1:
		enterExperiment(mycursor)
	
	if choice == 2:
		enterRun(mycursor)
		
	if choice == 3:
		viewExperiment(mycursor)
	if choice == 4:
		viewRun(mycursor)
			
	ans = input("Press m to go back to the menu or e to exit. ")
	while ans != 'm' and ans != 'e':
		print("Invalid option selected. Try again.")
		ans = input("Press m to go back to the menu or e to exit. ")
	
	if ans == 'e':
		break
		


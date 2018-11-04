import mysql.connector
import datetime
import sys

#Builds the database and all the tables if they don't already exist
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

#Created the procedures needed to make sure Type attribute isn't violated
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
	
	
	
#Experiment information is added to the database
def enterExperiment(mycursor):

	#Enter into Experiment Table
	#All data is validated before the entry into the database
	ExperimentID = input("Enter ExperimentID: ")
	ManagerID = input("Enter ManagerID: ")
	print("Enter StartDate")
	
	try:
		Month = int(input("   Enter Month: "))
		Day = int(input("   Enter Day: "))
		Year = int(input("   Enter Year: "))
	except:
		print("")
		print("MUST ENTER INTEGER VALUE. RETURNING TO MENU...")
		return
		
	try:	
		date1 = datetime.date(Year, Month, Day)
	except:
		print("")
		print("INVALID DATE. MUST BE  DAY(1-31) MONTH(1-12) YEAR(YYYY). RETURNING TO MENU...")
		return

	print("Enter DataEntryDate")
	
	try:
		Month = int(input("   Enter Month: "))
		Day = int(input("   Enter Day: "))
		Year = int(input("   Enter Year: "))
		print("")
	except:
		print("")
		print("MUST ENTER INTEGER VALUE. RETURNING TO MENU...")
		return
	
	try:	
		date2 = datetime.date(Year, Month, Day)
	except:
		print("")
		print("INVALID DATE. MUST BE  DAY(1-31) MONTH(1-12) YEAR(YYYY). RETURNING TO MENU...")
		return
	
	if date1  > datetime.date.today():
		print("")
		print("START DATE IS IN THE FUTURE. RETURNING TO MENU...")
		return
		
	elif date2 > datetime.date.today():
		print("")
		print("DATA ENTRY DATE IS IN THE FUTURE.RETURNING TO MENU...")
		return
		
	elif date1 > date2:
		print("")
		print("START DATE IS BEFORE DATA ENTRY DATE. RETURNING TO MENU...")
		return
		
	sql = "INSERT INTO Experiment(ExperimentID, ManagerID, StartDate, DataEntryDate) VALUES (%s, %s, %s, %s)"
	val = (ExperimentID, ManagerID, date1, date2)
	
	#Data is entered here and if it already exists then we stop and return
	try:
		mycursor.execute(sql, val)
	except mysql.connector.errors.IntegrityError:
		print("DATA ALREADY EXISTS. RETURNING TO MENU...")
		return
		
	
	#Enter into ParametersTypes Table
	#Validate number of parameters
	while True:
		try:
			parameters = int(input("How many parameters do you want to enter?: "))
			if parameters >= 0:
				break
			else:
				print("ERROR: Must enter integer > 0.")
				print("Try Again")
		except:
				print("ERROR: Must enter an integer!")
				print("Try Again.")
			
	
	while parameters > 0:
		ParameterName = input("Enter ParameterName: ")
		Type = input("Enter Type: ")
		Required = input("Is It Required? (y/n):  ")
		
		#Validate input for Required Field
		while Required != 'y' and Required != 'n':
			print("ERROR: Invalid input.")
			print("Try again.")
			Required = input("Is it Required? (y/n): ")
			
		if Required == "y":
			Required = 1
		else: 
			Required = 0
	
		sql = "INSERT INTO ParametersTypes(ExperimentID, ParameterName, Type, Required) VALUES (%s, %s, %s, %s)"
		val = (ExperimentID, ParameterName, Type, Required)
		
		#Possibility Type is incorrect and Info has already been enterted
		try:
			mycursor.execute(sql, val)	
			print(mycursor.rowcount, "record inserted.")
			print("")
			parameters-=1
		#Catches Type error and asks if they want to try again
		except mysql.connector.errors.DatabaseError:
			print("Type must be of INT, FLOAT, STRING, URL, DATE, DATETIME")
			again = input("Want to try again? (y/n) ")
			while again != 'y' and again != 'n':
				print("ERROR: Invalid response, y or n expected.")
				again = input("Want to try again? (y/n) ")
			if again == 'n':		
				parameters-=1
		#Data has already been entered
		except mysql.connector.errors.IntegrityError:
			print("ERROR: Data already exists.")
			parameters-=1
			
	#Results validation
	while True:
		try:
			results = int(input("How many results will there be? "))
			if results >= 0:
				break
			else:
				print("ERROR: Integer must be > 0")
				print("Try again.")
		except:
			print("ERROR: must be an integer.")
			print("Try Again")
	
	#Enter into ResultParameters Table	
	while results > 0:
		ResultName = input("Enter ResultName: ")
		Type = input("Enter Type: ")
		Required = input("Is It Required? (y/n):  ")
		
		while Required != 'y' and Required != 'n':
			print("ERROR: Invalid input.")
			print("Try again.")
			Required = input("Is It Required? (y/n):  ")
			
		if Required == "y":
			Required = 1
		else:
			Required = 0
			
		sql = "INSERT INTO ResultTypes(ExperimentID, ResultName, Type, Required) VALUES (%s, %s, %s, %s)"
		val = (ExperimentID, ResultName, Type, Required)

		#Data is validated 		
		try:
			mycursor.execute(sql, val)	
			print(mycursor.rowcount, "record inserted.")
			print("")
			results-=1
		#Type is invalid
		except mysql.connector.errors.DatabaseError:
			print("Type must be of INT, FLOAT, STRING, URL, DATE, DATETIME")
			again = input("Want to try again? (y/n) ")
			while again != 'y' and again != 'n':
				print("ERROR: Invalid response, y or n expected.")
				again = input("Want to try again? (y/n) ")
			if again == 'n':		
				results-=1
		#Data already existed
		except mysql.connector.errors.IntegrityError:
			print("ERROR: Data already exists.")
			results-=1
	return
			
#Entering run information			
def enterRun(mycursor):

	#Enter into Runs Table
	ExperimentID = input("Enter ExperimentID: ")
	print("Enter TimeOfRun")
	
	#Validating Time of Run
	try:
		Month = int(input("   Enter Month: "))
		Day = int(input("   Enter Day: "))
		Year = int(input("  Enter Year: "))
		Hour = int(input("  Enter Hour: "))
		Minute = int(input("  Enter Minute: "))
	except:
		print("")
		print("MUST ENTER INTEGER VALUE. RETURNING TO MENU...")
		return
		
	try:	
		TimeOfRun = datetime.datetime(Year, Month, Day, Hour, Minute)
	except:
		print("")
		print("INVALID DATETIME. RETURNING TO MENU")
		return
	
	#Validate SSN length
	ExperimenterSSN = input("Enter ExperimenterSSN: ")
	while len(ExperimenterSSN) != 6:
		print("EXPERIMENTER SSN MUST BE LENGTH 6.")
		print("Try Again")
		print("")
		ExperimenterSSN = input("Enter ExperimenterSSN: ")
	
	#Validate run success	
	Success = input("Was the run successful?(y/n) ")
	while Success != 'y' and Success != 'n':
			print("Invalid input. Try Again.")
			Success = input("Was the run successful?(y/n) ")
	if Success == "y":
			Success = 1
	else:
			Success = 0

	sql = "INSERT INTO Runs(ExperimentID, TimeOfRun, ExperimenterSSN, Success) VALUES (%s, %s, %s, %s)"
	val = (ExperimentID, TimeOfRun, ExperimenterSSN, Success)
	
	#Validate entry
	try:
		mycursor.execute(sql, val)
	#Run Already Exists	
	except mysql.connector.errors.IntegrityError:
		print("Run already exists. Returning to menu...")
		return
	
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
			#Doesn't need to be validated
			mycursor.execute(sql, val)
		else:
			print("Was", ParameterName,"entered? (y/n) ")
			ans = input("")
			
			#Validate optional parameter input
			while ans != 'y' and ans != 'n':
				print("ERROR: Invalid response.")
				print("Try again.")
				print("Was", ParameterName,"entered? (y/n) ")
				ans = input("")
				
			if ans == 'y':
				print("Enter the value of parameter", ParameterName)
				Value = input("")
				val = (ExperimentID, TimeOfRun, ParameterName, Value)
				#Doesn't need to be validated
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
				#Doesn't need to be validated
				mycursor.execute(sql, val)
				
			else:
				print("Was", ResultName, "determined? (y/n) ")
				ans = input("")
				while ans != 'y' and ans!= 'n':
					print("ERROR: Invalid response.")
					print("Try again")
					print("Was", ResultName, "determined? (y/n) ")
					ans = input("")
				if ans == 'y':
					print("Enter the value of result", ResultName)
					Value = input("")
					val = (ExperimentID, TimeOfRun, ResultName, Value)
					#Doesn't need to be validated
					mycursor.execute(sql, val)

	return

#Reports Experiment information given an experiementID
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
		
	return

#Prints Run information given an experiment ID and creates an html table if specified	
def viewRun(mycursor, html):
	ExperimentID = input("Enter the desired ExperimentID: ")
	mycursor.execute("SELECT * FROM Runs WHERE ExperimentID = %s", (ExperimentID,))
	myresult = mycursor.fetchall()
		
	if mycursor.rowcount != 0:
		print("Experiment", ExperimentID)
		for x in myresult:
			print("	Time of run:", x[1])
			print("	Experimenter SSN:", x[2])
			if x[3] == 0:
				Success = "Failure"
			else:
				Success = "Success"
			print("       ",Success) 
			if html:
				file = open("runsreport.html", "w")
				linesoftext = ["<!DOCTYPE html>", "<html>", "<body>", "<h2>Run Results for Experiment %s</h2>" % ExperimentID, "<table style=\"width:100%\">", "<tr>", "<th>Time of Run</th>", "<th>Result Name</th>", "<th>Value</th>", "</tr>"]
				file.writelines(linesoftext)
	else:
		print("Invalid ExperimentID")
		return
						
	mycursor.execute("SELECT * FROM RunsParameter WHERE ExperimentID = %s AND TImeOfRun = %s", (ExperimentID,x[1]))
	paramresult = mycursor.fetchall()
	
	if mycursor.rowcount != 0:
		print("	Run Parameters:") 
		for y in paramresult:
			print("		Parameter Name: ", y[2])
			print("		Value: ", y[3])
	else:
		print("No Parameters.")
		
	mycursor.execute("SELECT * FROM RunsResult WHERE ExperimentID = %s AND TImeOfRun = %s", (ExperimentID,x[1]))
	runresult = mycursor.fetchall()
		
	if mycursor.rowcount != 0:
		print("	Run Results:")
		for y in runresult:
			if html:
				linesoftext = ["<tr>", "<td>%s</td>" % x[1], "<td>%s</td>" % y[2], "<td>%s</td>" % y[3], "</tr>"]
				file.writelines(linesoftext)
			print("		Result Name: ", y[2])
			print("		Value: ", y[3])
	else:
		print("No Results.")	

	if html:
		linesoftext = ["</table>", "</body>", "</html>"]
		file.writelines(linesoftext)
		file.close()
		print("Report generated..")
		
	return
	
#Generates an aggregate report based on selected aggregates	
def generateAgg(mycursor):
	ExperimentID = input("Enter an ExperimentID: ")
	print("What should we generate? ")
	print("1. Sum")
	print( "2. Average")
	choice = input("")
	while choice != "1" and choice != "2":
		print("ERROR: Invalid selection.")
		print("Try again.")
		print("What should we generate? ")
		print("1. Sum")
		print( "2. Average")
		choice = input("")
		
	if choice == "1":
		mycursor.execute("SELECT SUM(r.Value) FROM RunsParameter r, ParametersTypes p WHERE r.ExperimentID = p.ExperimentID AND r.ExperimentID = %s AND p.ExperimentID = %s AND r.ParameterName = p.ParameterName AND Type = 'INT'", (ExperimentID, ExperimentID))
		choice = "SUM:"
	else:
		mycursor.execute("SELECT AVG(r.Value) FROM RunsParameter r, ParametersTypes p WHERE r.ExperimentID = p.ExperimentID AND r.ExperimentID = %s AND p.ExperimentID = %s AND r.ParameterName = p.ParameterName AND Type = 'INT'", (ExperimentID, ExperimentID))
		choice = "AVG"
		
	result = mycursor.fetchall()	
	if mycursor.rowcount != 0:	
		for x in result:
			print("Experiment ID:", ExperimentID, choice, x[0])
	else:
		print("No information for the provided ExperimentID")
		
	
def paramSearch(mycursor):
	paramName = input("Enter Parameter Name: ")
	Type = input("Enter Type: ")
	
	mycursor.execute("SELECT e.ExperimentID, ManagerID, StartDate, DataEntryDate FROM Experiment e, ParametersTypes p WHERE e.ExperimentID = p.ExperimentID AND Type = %s AND ParameterName = %s ORDER BY StartDate", (Type, paramName))
	
	result = mycursor.fetchall()
	
	if mycursor.rowcount != 0:
		for x in result:
			print("ExperimentID:", x[0], "ManagerID:", x[1], "StartDate:", x[2], "EntryDate:", x[3])
	else:
		print("No Data Found.")
	
		
	
	
	
	
	
buildDB()

mydb = mysql.connector.connect(
		host="localhost",
    		user="HW3335",
    		passwd="PW3335",	
		database="Experiment"
	)

mydb.autocommit = True
mycursor = mydb.cursor()


createProcedure(mycursor)
	
while True:
	while True:
		print("What would you like to do?")
		print("1. Experiment entry")
		print("2. Run Entry")
		print("3. View Experiment Info")
		print("4. View Run Info")
		print("5. Generate Experiment Report")
		print("6. Generate Agregate Report")
		print("7. Parameter Search")
		print("8. Compare Experiments")
		print("9. Exit")
		choice = int(input(""))
		if choice > 9 or choice < 1:
			print("Invalid Choice")
			print("")
		else:
			break

	print("")

	if choice == 1:
		enterExperiment(mycursor)
	elif choice == 2:
		enterRun(mycursor)
	elif choice == 3:
		viewExperiment(mycursor)
	elif choice == 4:
		viewRun(mycursor, False)
	elif choice == 5:
		viewRun(mycursor, True)
	elif choice == 6:
		generateAgg(mycursor)
	elif choice == 7:
		paramSearch(mycursor)
	elif choice == 8:
		print("Choice 8 was selected")
	elif choice == 9:
		break
			
	print("")		
	ans = input("Press m to go back to the menu or e to exit. ")
	while ans != 'm' and ans != 'e':
		print("Invalid option selected. Try again.")
		ans = input("Press m to go back to the menu or e to exit. ")
	
	if ans == 'e':
		break
		


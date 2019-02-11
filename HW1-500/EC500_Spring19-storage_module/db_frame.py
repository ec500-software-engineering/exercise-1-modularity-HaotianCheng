import pymongo
import json

class storage:
	'''
	class for storage of data from input module
	basic functions: CRUD(create, read, update, delete)
	'''
	def readJson(self, jsonFile):
		'''
			change json file to dictionary
		'''
		dict = json.loads(jsonFile)
		pass

	def connectMySQL(self):
		'''
			connect to mysql 
		'''
		self.sqldb = mysql.connector.connect(
			host="localhost",
			user="xxxx",
			passwd="xxxxx",
			database = "xxx_mysql"
			)
		self.mycursor = self.sqldb.cursor()

		pass

	def create_table_mysql(self):
	'''
		this part is for creating the mysql table
	'''
	mydb = mysql.connector.connect(
		host="localhost",
		user="xxxxx",
		passwd="xxx",
		database= 'xxx_mysql'
	)
	mycursor = mydb.cursor()
	sql1 = '''
		CREATE TABLE tablename(
		id int(5) primary key,
		patientName VARCHAR(255),
		age VARCHAR(255),
		gender VARCHAR(255),
		pulse VARCHAR(255),
		blood_pressure VARCHAR(255),
		oxygen VARCHAR(255))
	'''
	mycursor.execute(sql1)

	mycursor.execute("SHOW TABLES")
	for x in mycursor:
		print(x)

	def connectMongob(self):
		'''
			connect to the mongodb
		'''
		self.client = pymongo.MongoClient()
		pass

	def insert_mongo(self, data):
		'''
			add data to the mongodb
		'''
		pass

	def insert_mysql(self, patientID, data):
		'''
			add data to the mysql
		'''
		pass

	def delete_mysql(self, patientID):
		'''
			delete data
		'''
		pass

	def delete_mongo(self, patientID):
		'''
			delete data
		'''
		pass

	def update_mysql(self, patientID):
		'''
			update data
		'''
		pass

	def update_mongo(self, patientID):
		'''
			update data
		'''
		pass

	def read_mongo(self, patientID):
		'''
			read data of patient
		'''
		pass

	def read_mysql(self, patientID):
		'''
			read data of patient
		'''
		pass




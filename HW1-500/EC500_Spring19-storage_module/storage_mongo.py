import pymongo
import json

global Debug
Debug =False

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
		return dict


	def connectMongob(self):
		'''
			connect to the mongodb
		'''
		self.client = pymongo.MongoClient()
		self.mydb = self.client.hospital
		self.mycol = self.mydb.patient

	def insert_mongo(self, patient_data, sensor_data):
		'''
			add data to the mongodb
		'''
		for key in patient_data.keys():
			patientId = key

		patient_dict = {}
		patient_dict['patientId'] = patientId
		patient_dict['name'] = patient_data[patientId]["name"]
		patient_dict['gender'] = patient_data[patientId]["gender"]
		patient_dict['age'] = patient_data[patientId]["age"]
		
		patient_dict['datetime'] = sensor_data[patientId]["time"]
		patient_dict['bloodPressure'] = sensor_data[patientId]["bloodPressure"]
		patient_dict['bloodOx'] =  sensor_data[patientId]["bloodOx"]
		patient_dict['pulse'] = sensor_data[patientId]["pulse"]
		insert = self.mycol.insert_one(patient_dict)

		if Debug:
			print("-------------------")
			print("insert data:")
			print("-------------------")
			print(patient_dict)
			print("-------------------")
			print("insertion complete")
			print("-------------------")



	def delete_mongo_many(self, patientID):
		'''
			delete all data of one patient
		'''
		query = { "patientId": patientID }

		if Debug:
			#read before delete
			self.read_mongo(patientID)

		# delete
		self.mycol.delete_many(query)

		if Debug:
			# read after delete
			self.read_mongo(patientID)


	def delete_mongo_one(self, patientID, datetime):
		'''
			delete all data of one patient
		'''
		query = { "patientId": patientID, "datetime": datetime}

		if Debug:
			#read before delete
			self.read_mongo(patientID)
		# delete
		self.mycol.delete_one(query)

		if Debug:
			# read after delete
			self.read_mongo(patientID)

	def update_mongo(self, patientID, datetime, item, data):
		'''
			update data
		'''
		query = {"patientId": patientID, "datetime": datetime}
		updated_data = {"$set": {item: data}}
		self.mycol.update_one(query, updated_data)


	def read_mongo(self, patientID):
		'''
			read data of patient
		'''
		data = []
		for info in self.mycol.find():
			if info['patientId'] ==patientID :
 				data.append(info)

		print("-------------------")
		print("read data:")
		print("-------------------")
		print(data)
		return data



def drop_colletion():
	drop = storage()
	drop.connectMongob()
	drop.mycol.drop()


def mongo_test():
	test = storage()
	test.connectMongob()

	#test insert
	
	test.insert_mongo(test_case[0],test_case[1])

	#test read
	
	#test.read_mongo("1")

	# test delete
	#test.delete_mongo_many("1")
	#test.delete_mongo_one("1","12:05:10pm-18/01/2019")

	# test update
	#test.update_mongo("1", "12:05:10pm-18/01/2019", "patientId", "2")
	


test_case = [{"1" :{
					"name": "wzy",
					"gender": "Male",
					"age": "23",
			  	}},
			{"1" :{
				"pulse": "90",
				"pulseRange": {"lower": "50", "higher": "120"},
				"bloodPressure": "45",
				"pressureRange": {"lower": "30", "higher": "100"},
				"bloodOx": "0.34",
				"oxRange": {"lower": "0.33", "higher": "0.80"},
				"time": "12:05:10pm-18/01/2019"
				}
			}]
def main():

	#drop_colletion()
	mongo_test()
	

if __name__ == '__main__':
	main()





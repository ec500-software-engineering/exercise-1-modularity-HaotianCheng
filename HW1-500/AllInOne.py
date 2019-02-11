import json
import pymongo

fileName = "input.txt"

file = open(fileName, "r")
fileContent = file.read().splitlines()
fileContent = [i.split() for i in fileContent]


# error check function
def ErrorCheck(line):
    checkEx1 = ["ID", "NAME", "GENDER", "AGE"]
    checkEx2 = ["ID", "PULSE", "PULSE RANGE", "BLOOD PRESSURE", "PRESSURE RANGE", "BLOOD OXYGEN", "OXYGEN RANGE",
                "TIME"]
    p = True
    error = "Error: "

    if len(line) == len(checkEx1):
        for n, i in enumerate(line):
            if i == "null":
                error += (checkEx1[n] + " IS MISSING. ")
                p = False
        # if error != "":
        #     print(error)

        return p, error

    elif len(line) == len(checkEx2):
        for n, i in enumerate(line):
            if i == "null":
                error += (checkEx2[n] + " IS MISSING. ")
                p = False
        # if error != "":
        #     print(error)

        return p, error


def SaveAlertData(alert_message, p_id):
    alert_dict = {"alert_message": alert_message, "patient_id": p_id}
    alert_json = json.dumps(alert_dict)
    # print(alert_json)
    # call_storage_module(alert_json)


def SendToUI(msg, data):
    patient = [i for i in data]
    patient_id = patient[0]
    ui_dict = {"ID": patient_id, "alert_message": msg, "pulse": data[patient_id]["pulse"],
               "bloodPressure": data[patient_id]["bloodPressure"],
               "bloodOx": data[patient_id]["bloodOx"]}
    ui_json = json.dumps(ui_dict)
    # print(ui_json)
    return ui_dict
    # call_output_method


def AlertCheck(data):
    alert_message = ""
    patient = [i for i in data]
    patient_id = patient[0]
    # print(data[patient_id]["pulseRange"]["lower"], data[patient_id]["pulseRange"]["upper"],
    #       data[patient_id]["pressureRange"]["lower"], data[patient_id]["pressureRange"]["upper"],
    #       data[patient_id]["oxRange"]["lower"], data[patient_id]["oxRange"]["upper"])
    if float(data[patient_id]["pulse"]) < float(data[patient_id]["pulseRange"]["lower"]):
        alert_message += "Pulse is Too low, "
    elif float(data[patient_id]["pulse"]) > float(data[patient_id]["pulseRange"]["upper"]):
        # print(data[patient_id]["pulse"], data[patient_id]["pulseRange"]["upper"])
        alert_message += "Pulse is Too high, "
    if float(data[patient_id]["bloodPressure"]) < float(data[patient_id]["pressureRange"]["lower"]):
        alert_message += "Pressure is Too low, "
    elif float(data[patient_id]["bloodPressure"]) > float(data[patient_id]["pressureRange"]["upper"]):
        alert_message += "Pressure is Too high, "
    if float(data[patient_id]["bloodOx"]) < float(data[patient_id]["oxRange"]["lower"]):
        alert_message += "Oxygen is Too low, "
    elif float(data[patient_id]["bloodOx"]) > float(data[patient_id]["oxRange"]["upper"]):
        alert_message += "Oxygen is Too high, "
    if alert_message != "":
        SaveAlertData(alert_message, data[patient_id])
    alert = SendToUI(alert_message, data)
    return alert


class patient(object):
    def __init__(self):
        self.name = "test"

    def set_bloodPressure(self, bloodPressure):
        self.bloodPressure = bloodPressure

    def set_pulse(self, pulse):
        self.pulse = pulse

    def set_bloodOx(self, bloodOx):
        self.bloodOx = bloodOx

    def get_bloodPressure(self, bloodPressure):
        return bloodPressure

    def get_pulse(self, pulse):
        return pulse

    def get_bloodOx(self, bloodOx):
        return bloodOx

    def recieveFromAlert(self, data):
        # print(data)
        self.patientID = data["ID"]
        self.msg = data["alert_message"]
        self.bloodPressure = data["bloodPressure"]
        self.pulse = data["pulse"]
        self.bloodOx = data["bloodOx"]

    def recieveFromUsers(self, data):
        patient = [i for i in data]
        patient_id = patient[0]
        self.patientID = patient_id
        self.name = data[patient_id]["name"]
        self.gender = data[patient_id]["gender"]
        self.age = data[patient_id]["age"]

    def send_alert_to_UI(self):
        send_data = json.dumps({
            'ID': self.patientID,
            'alert_message': self.msg,
            'bloodPressure': self.bloodPressure,
            'pulse': self.pulse,
            'bloodOx': self.bloodOx
        })
        print(send_data)
        return send_data

    def send_select_to_UI(self):
        send_data = json.dumps({
            'ID': self.patientID,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
        })
        print(send_data)
        return send_data




global Debug
Debug = False


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
        patient_dict['bloodOx'] = sensor_data[patientId]["bloodOx"]
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
        query = {"patientId": patientID}

        if Debug:
            # read before delete
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
        query = {"patientId": patientID, "datetime": datetime}

        if Debug:
            # read before delete
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
            if info['patientId'] == patientID:
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


def mangoStorage(data1, data2):
    test = storage()
    test.connectMongob()

    # test insert

    test.insert_mongo(data1, data2)


# test read

# test.read_mongo("1")

# test delete
# test.delete_mongo_many("1")
# test.delete_mongo_one("1","12:05:10pm-18/01/2019")

# test update
# test.update_mongo("1", "12:05:10pm-18/01/2019", "patientId", "2")


test_case = [{"1": {
    "name": "wzy",
    "gender": "Male",
    "age": "23",
}},
    {"1": {
        "pulse": "90",
        "pulseRange": {"lower": "50", "higher": "120"},
        "bloodPressure": "45",
        "pressureRange": {"lower": "30", "higher": "100"},
        "bloodOx": "0.34",
        "oxRange": {"lower": "0.33", "higher": "0.80"},
        "time": "12:05:10pm-18/01/2019"
    }
    }]


for line in fileContent:
    if ErrorCheck(line)[0]:
        if len(line) == 4:
            data1 = {}
            data1[line[0]] = {'name': line[1],
                              'gender': line[2],
                              'age': line[3]}
            # AlertCheck(data1)
            patient_1 = patient()
            patient_1.recieveFromUsers(data1)
            patient_1.send_select_to_UI()

        elif len(line) == 8:
            lower2, upper2 = line[2].split("-")
            lower4, upper4 = line[4].split("-")
            lower6, upper6 = line[6].split("-")
            data2 = {}
            data2[line[0]] = {'pulse': line[1],
                              'pulseRange': {'lower': lower2, 'upper': upper2},
                              'bloodPressure': line[3],
                              'pressureRange': {'lower': lower4, 'upper':upper4},
                              'bloodOx': line[5],
                              'oxRange': {'lower': lower6, 'upper': upper6},
                              'time': line[7]}
            alertData = AlertCheck(data2)
            patient_1 = patient()
            patient_1.recieveFromAlert(alertData)
            patient_1.send_alert_to_UI()
            # mangoStorage(data1, data2)

    else:
        print(ErrorCheck(line)[1])





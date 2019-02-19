import random
import time
import datetime
import names
import queue
import threading
import json

inputQueue = queue.Queue()
generalQueue = queue.Queue()
alertQueue = queue.Queue()


def randomNone(inputList):
    num = random.choice([1,1,1,2,2,3])
    whether = random.choice(range(9))
    if whether == 1:
        for i in range(num):
            inputList[random.choice(range(len(inputList)))] = "null"


def combineList(inputList):
    content = ""
    for i in inputList:
        content += i
        content += " "
    return content


def GenerateInput():

    openState = True
    justAdd = False
    patientID = 0

    while openState:
        if random.choice(range(5)) == 0 and patientID != 0:
            pulse = random.choice(range(300))
            pulseRange = "50-120"
            bloodPressure = random.choice(range(100))
            pressureRange = "30-100"
            bloodOx = random.choice(range(100))
            oxRange = "30-60"
            currentTime = str(datetime.datetime.now()).replace(" ","-")
            currentTime = currentTime[:-7]
            input_List = [str(patientID), str(pulse), pulseRange, str(bloodPressure), pressureRange, str(bloodOx),
                          oxRange, currentTime]
            randomNone(input_List)
            inputContent = combineList(input_List)[:-1]
            inputQueue.put(inputContent)
            justAdd = False
            time.sleep(random.choice(range(1,9)))
        elif justAdd:
            pulse = random.choice(range(300))
            pulseRange = "50-120"
            bloodPressure = random.choice(range(100))
            pressureRange = "30-100"
            bloodOx = random.choice(range(100))
            oxRange = "30-60"
            currentTime = str(datetime.datetime.now()).replace(" ","-")
            currentTime = currentTime[:-7]
            input_List = [str(patientID), str(pulse), pulseRange, str(bloodPressure), pressureRange, str(bloodOx),
                          oxRange, currentTime]
            randomNone(input_List)
            inputContent = combineList(input_List)[:-1]
            inputQueue.put(inputContent)
            time.sleep(random.choice(range(1,9)))

        else:
            patientID += 1
            justAdd = True
            gender = random.choice(["Male","Famale"])
            name = names.get_full_name(gender).replace(" ","_")
            age = random.choice(range(120))
            input_List = [str(patientID), name, gender, str(age)]
            randomNone(input_List)
            inputContent = combineList(input_List)[:-1]
            inputQueue.put(inputContent)
            time.sleep(random.choice(range(1,9)))
            # openState = False


def ErrorCheck(input_List):
    checkEx1 = ["ID", "NAME", "GENDER", "AGE"]
    checkEx2 = ["ID", "PULSE", "PULSE RANGE", "BLOOD PRESSURE", "PRESSURE RANGE", "BLOOD OXYGEN", "OXYGEN RANGE",
                "TIME"]
    p = True
    error = "Error: "

    if len(input_List) == len(checkEx1):
        for n, i in enumerate(input_List):
            if i == "null":
                error += (checkEx1[n] + " IS MISSING. ")
                p = False
        # if error != "":
        #     print(error)

        return p, error

    elif len(input_List) == len(checkEx2):
        for n, i in enumerate(input_List):
            if i == "null":
                error += (checkEx2[n] + " IS MISSING. ")
                p = False
        # if error != "":
        #     print(error)

        return p, error


def SendToUI(msg, data):
    patient = [i for i in data]
    patient_id = patient[0]
    ui_dict = {"ID": patient_id, "alert_message": msg, "pulse": data[patient_id]["pulse"],
               "bloodPressure": data[patient_id]["bloodPressure"],
               "bloodOx": data[patient_id]["bloodOx"]}
    
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



def ProcessInput():
    while True:
        if not inputQueue.empty():
            inputLine = inputQueue.get()
            inputList = inputLine.split()
            # print(inputLine)
            if ErrorCheck(inputList)[0]:
                if len(inputList) == 4:
                    data1 = {}
                    data1[inputList[0]] = {'name': inputList[1],
                                      'gender': inputList[2],
                                      'age': inputList[3]}
                    generalQueue.put(data1)
                    # patient_1 = patient()
                    # patient_1.recieveFromUsers(data1)
                    # patient_1.send_select_to_UI()
                    # print(data1)

                elif len(inputList) == 8:
                    lower2, upper2 = inputList[2].split("-")
                    lower4, upper4 = inputList[4].split("-")
                    lower6, upper6 = inputList[6].split("-")
                    data2 = {}
                    data2[inputList[0]] = {'pulse': inputList[1],
                                      'pulseRange': {'lower': lower2, 'upper': upper2},
                                      'bloodPressure': inputList[3],
                                      'pressureRange': {'lower': lower4, 'upper': upper4},
                                      'bloodOx': inputList[5],
                                      'oxRange': {'lower': lower6, 'upper': upper6},
                                      'time': inputList[7]}

                    alertData = AlertCheck(data2)
                    alertQueue.put(alertData)
                    # patient_1 = patient()
                    # patient_1.recieveFromAlert(alertData)
                    # patient_1.send_alert_to_UI()

                    # mangoStorage(data1, data2)
                    # print(data2)

            else:
                print(ErrorCheck(inputList)[1])
        time.sleep(1)
            
def GenerateOutput():
    while True:
        if not generalQueue.empty():
            patientData = generalQueue.get()
            patient_1 = patient()
            patient_1.recieveFromUsers(patientData)
            patient_1.send_select_to_UI()

        if not alertQueue.empty():
            alert = alertQueue.get()
            patient_1 = patient()
            patient_1.recieveFromAlert(alert)
            patient_1.send_alert_to_UI()

        time.sleep(1)




inputThread = threading.Thread(name = "Input", target = GenerateInput)

processThread = threading.Thread(name = "Process", target = ProcessInput)

outputThread = threading.Thread(name = "Output", target = GenerateOutput)

inputThread.start()
processThread.start()
outputThread.start()

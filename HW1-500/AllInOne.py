import json

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


for line in fileContent:
    if ErrorCheck(line)[0]:
        if len(line) == 4:
            data1 = {}
            data1[line[0]] = {'name': line[1],
                              'gender': line[2],
                              'age': line[3]}
            # AlertCheck(data1)

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


    else:
        print(ErrorCheck(line)[1])





import json
import os


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


def main():
    patient_1 = patient()
    json_dir = os.getcwd()
    with open(json_dir + '/patient.json', 'r') as rawJson:
        data = json.load(rawJson)
        patient_1.recieveFromAlert(data)
        patient_1.send_alert_to_UI()
        rawJson.close()

    with open(json_dir + '/users.json', 'r') as rawJson:
        data = json.load(rawJson)
        patient_1.recieveFromUsers(data)
        rawJson.close()


if __name__ == "__main__":
    main()

import json

j = {"patient_id": 1, "bp_id": 55, "pulse_id": 30, "pulse_range": {"lower": 40, "upper": 120},
     "temp_id": 102, "temp_range": {"lower": 92, "upper": 101}, "bp_range": {"lower": 50, "upper": 60}}
j_o = json.dumps(j)

# d_o=json.loads(j_o)


def saveAlertData(alert_message, p_id):

    alert_dict = {"alert_message": alert_message, "patient_id": p_id}
    alert_json = json.dumps(alert_dict)
    print(alert_json)
    # call_storage_module(alert_json)


def sendToUI(msg, j):
    ui_dict = {"alert_message": msg,
               "bp_id": j["bp_id"], "pulse_id": j["pulse_id"], "temp_id": j["temp_id"]}
    ui_json = json.dumps(ui_dict)
    print(ui_json)
    # call_output_method


def alertCheck(j_o):
    j = json.loads(j_o)
    alert_message = ""
    if(j["bp_id"] < j["bp_range"]["lower"]):
        alert_message += "BP is Too low, "
    elif(j["bp_id"] > j["bp_range"]["upper"]):
        alert_message = "BP is Too high, "
    if(j["pulse_id"] < j["pulse_range"]["lower"]):
        alert_message += "pulse is Too low, "
    elif(j["pulse_id"] > j["pulse_range"]["upper"]):
        alert_message += "pulse is Too high, "
    if(j["temp_id"] < j["temp_range"]["lower"]):
        alert_message += "temp is Too low, "
    elif(j["temp_id"] > j["temp_range"]["upper"]):
        alert_message += "temp is Too high, "
    if(alert_message != ""):
        saveAlertData(alert_message, j["patient_id"])
    sendToUI(alert_message, j)


alertCheck(j_o)

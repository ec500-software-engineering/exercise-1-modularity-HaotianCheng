#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 09:29:32 2019

@author: mohitbeniwal
"""
import json

j = {"patient_id": 1, "pulse": 55, "bloodPressure": 30, "pulse_range": {"lower": 40, "upper": 120},
     "bloodOx": 102, "temp_range": {"lower": 92, "upper": 101}, "bp_range": {"lower": 50, "upper": 60}}
data = json.dumps(j)

# d_o=json.loads(data)


def SaveAlertData(alert_message, p_id):
    
    alert_dict = {"alert_message": alert_message, "patient_id": p_id}
    alert_json = json.dumps(alert_dict)
    print(alert_json)
    # call_storage_module(alert_json)
  
    
def SendToUI(msg, data):
    patient_id = data.keys()[0]
    ui_dict = {"alert_message": msg, "pulse": data[patient_id]["pulse"], "bloodPressure": data[patient_id]["bloodPressure"],
               "bloodOx": data[patient_id]["bloodOx"]}
    ui_json = json.dumps(ui_dict)
    print(ui_json)
    # call_output_method


def AlertCheck(data):
    alert_message = ""
    patient_id = data.keys()[0]
    if data[patient_id]["pulse"] < data[patient_id]["pulseRange"]["lower"]:
        alert_message += "Pulse is Too low, "
    elif data[patient_id]["pulse"] > data[patient_id]["pulseRange"]["upper"]:
        alert_message = "Pulse is Too high, "
    if data[patient_id]["bloodPressure"] < data[patient_id]["pressureRange"]["lower"]:
        alert_message += "Pressure is Too low, "
    elif data[patient_id]["bloodPressure"] > data[patient_id]["pressureRange"]["upper"]:
        alert_message += "Pressure is Too high, "
    if data[patient_id]["bloodOx"] < data[patient_id]["oxRange"]["lower"]:
        alert_message += "Oxygen is Too low, "
    elif data[patient_id]["bloodOx"] > data[patient_id]["oxRange"]["upper"]:
        alert_message += "Oxygen is Too high, "
    if alert_message != "":
        SaveAlertData(alert_message, j[patient_id])
    SendToUI(alert_message, data)
    
    
AlertCheck(data)  
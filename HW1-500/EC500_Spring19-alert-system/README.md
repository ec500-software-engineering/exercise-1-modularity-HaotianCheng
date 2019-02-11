Alert system will receive a JSON file containing patient info from Input Analyzer.

 

Function stubs:

1.     alertCheck(Json):

This function reads JSON data and will check for the threshold value.

Input: JSON (patient information)

Output: json (Alert message,patientid)

2.     saveAlertData(json):

Input: This function will take alertCheck method’s output as input i.e list.

Output: void

3.     sendToUI(Json):

This method will send patient data and alerts to the UI.

Input: Json

Output: Josn


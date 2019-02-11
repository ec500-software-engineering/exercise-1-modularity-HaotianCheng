# EC500_Spring19  
# Output Module  
## Input Source  
#### 1.Alert Module  
- Jason Files
```
void recieveFromAlert(Json)
```
#### 2.Button(keyboard) input  
- User's input(Doctors or nurses)
```
void recieveFromUsers(Json)
```
## Processing  
### Choose the data to display based on user's input  
```
Json select(Json)
```
## Output  
#### Patient Data
```
Json sendToUI()
```
- Patient Pulse  
- Patient Blood Pressure  
- Patient Blood Oxgen
#### Alert message  

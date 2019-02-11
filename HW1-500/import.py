import json

data = {}   
data['000001'] = {'name': 'Joker',
              'gender': 'M',
              'age': 45}
data['000002'] = {'name': 'Mary',
              'gender': 'F',
              'age': 15}

data = {}   
data['000001'] = {'pulse': 90,
                  'pulseRange': {'lower': 120, 'upper': 50},
                  'bloodPressure': 45,
                  'pressureRange': {'lower':100, 'upper':30},
                  'bloodOx': 0.34,
                  'oxRange': {'lower':0.80, 'upper':0.33},
                  'time': '12:01pm 18/01/2019'}


with open('Patient List.json', 'w') as outfile:  
    json.dump(data, outfile)


with open('Patient List.json') as json_file:  
    data = json.load(json_file)
    for i in data:
        print('Name: ' + data[i]['Name'])
        print('Gender: ' + data[i]['Gender'])
        print('Age: ', data[i]['Age'])
        print('')

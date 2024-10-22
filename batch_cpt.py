import json

file = 'riverland_eco.json'

with open(file) as f:
   d = json.load(f)

for weight in d['weights']:
   print(weight['id'])
   print('-')
   if type(weight['scores']) is dict:
       print(list(weight['scores'].keys()))
       print('-') 
       print(
          calculate_CPT(list(weight['scores'].values()), weight['notideal'], weight['ideal'])
           )
   else:
      print('ideal: {}'.format(weight['ideal']))
      print('notideal: {}'.format(weight['notideal']))
   print('=')
   print('\n')

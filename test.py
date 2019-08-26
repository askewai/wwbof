import random

userid = ['2312', '2141', '5252', '4910']
displayname = ['babelac', 'buabelac', 'liana', 'tan']
# WW - Seer - Villager
desc = ['You can eat any villagers', 'You can see the werewolf', '']
data = {'player': []}

# Randomize roles for 4-6 players
role = ['Werewolf', 'Seer']
for y in range(2):
    role.append('Villager')
random.shuffle(role) 

for x in range(4): 
    each_data = {
        "userid": userid[x],
        "displayname": displayname[x],
        "role": role[x],
        "status": True
    }
    data['player'].append(each_data)

print(data)

# {
#     'player': [
#         {
#             'userid': '2312', 
#             'displayname': 'babelac', 
#             'role': 'Seer', 
#             'status': True
#         }, 
#         {
#             'userid': '2141', 
#             'displayname': 'buabelac', 
#             'role': 'Villager', 
#             'status': True
#         }, 
#         {
#             'userid': '5252', 
#             'displayname': 'liana', 
#             'role': 'Villager', 
#             'status': True
#         }, 
#         {
#             'userid': '4910', 
#             'displayname': 'tan', 
#             'role': 'Werewolf', 
#             'status': True
#         }
#     ]
# }

lele = {
    'userid': 'Villager'
}
if 'Villager' in lele.values():
    print('\nAda role villager')
elif 'userid' in lele.keys():
    print('Ada userid')







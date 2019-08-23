# userid = ['1124','2322', '1525', '2324']
# displayname = ['Kevkur', 'Kevsan', 'anomalick', 'johandick']

# data = {
#     'player': [
#     ]
# }

# for x in range(len(userid)):
#     each_data = {
#         "userid": userid[x],
#         "displayname": displayname[x]
#     }
#     data['player'].append(each_data)

# print(data)

# data = {
#     'player': [
#         {
#             'userid': 1124,
#             'displayname': 'Kevkur'
#         },
#         {
#             'userid': 2322,
#             'displayname': 'Kevsan'
#         },
#         {
#             'userid': 1525,
#             'displayname': 'anomalick'
#         },
#         {
#             'userid': 2324,
#             'displayname': 'johandick'
#         }
#     ]
# }

import random

role = ['Werewolf', 'Seer', 'Villager', 'Villager']
random.shuffle(role)
print(role)



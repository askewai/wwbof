
lele = ['Villager', 'Werewolf', 'Villager', 'Seer', 'Villager']


for x in range(len(lele)):
    print('Saya Werewolf' if lele[x] == 'Werewolf' else ('Saya Villager' if lele[x] == 'Villager' else 'Saya Seer'))

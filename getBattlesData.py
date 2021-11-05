from os import remove
import urllib.request
import json
import certifi
import ssl
from multiprocessing.pool import ThreadPool as Pool
import traceback
import helper

import time
start_time = time.time()

totalUsers = 0

pool_size = 10

battleDB = []
mainBattles = []
with open('users.json') as f:
    users = json.load(f)


def divide_chunks(l, n):
    for i in range(0, len(l), n): 
        yield l[i:i + n]

def getUserBattles(username):
    counter = 0
    try:
        with urllib.request.urlopen('https://game-api.splinterlands.com/battle/history?player='+username, context=ssl.create_default_context(cafile=certifi.where())) as url:
            data = json.loads(url.read().decode())
            battles = data['battles']
        
        for i in battles:

            battle = {}
            detail = json.loads(i['details'])

            try:
                if detail['type'] == 'Surrender':
                    continue
            except:
                num = '1' if i['winner'] == i['player_1'] else '2'
                battle['summoner_id']       = detail['team'+num]['summoner']['card_detail_id']
                battle['summoner_level']    = detail['team'+num]['summoner']['level']

                for x in range(0, 6):
                    try:
                    # if  detail['team'+num]['monsters'][x]:
                        battle['monster_'+str(x+1)+'_id']       = detail['team'+num]['monsters'][x]['card_detail_id']
                        battle['monster_'+str(x+1)+'_level']    = detail['team'+num]['monsters'][x]['level']
                        tmp                                     = detail['team'+num]['monsters'][x]['abilities']
                        battle['monster_'+str(x+1)+'_abilities']= [s for s in tmp if s not in detail['team'+num]['summoner']['state']['abilities'] ]
                    except:
                        battle['monster_'+str(x+1)+'_id'] = ""
                        battle['monster_'+str(x+1)+'_level'] = ""
                        battle['monster_'+str(x+1)+'_abilities'] = []

                battle["created_date"]  = i["created_date"]
                battle['match_type']    = i['match_type']
                battle['mana_cap']      = i['mana_cap']
                battle['ruleset']       = i['ruleset']
                battle['inactive']      = i['inactive']
                # "battle_queue_id": "sl_2b5954f93d426de4b1b014676cb50092",
                battle['battle_queue_id'] = i['battle_queue_id_' + num]
                # "player_rating_initial": 192,
                battle['player_rating_initial'] = i['player_' + num + '_rating_initial']
                # "player_rating_final": 211,
                battle['player_rating_final'] = i['player_' + num + '_rating_final']
                battle['winner'] = i['winner']
                

            battleDB.append(battle)
            counter = counter + 1
        print(counter," battles collected from ",username)
    except Exception as e:
        print(traceback.format_exc())

def updateHistory():
    with open("newHistory.json") as file:
        data = json.load(file)
        finalList = data + battleDB
    file.close

    with open("newHistory.json", "w") as outfile:
        outfile.write(json.dumps(finalList))
        print("newHistory.json file was updated!")
    outfile.close   


print("Fetching data from ", len(users), " users")
totalUsers = len(users)
batch = list(divide_chunks(users,100))

for i in batch:
    pool = Pool(pool_size)
    pool.map_async(getUserBattles, i)
    pool.close()
    pool.join()
    print("Updating newHistory.json")
    updateHistory()
    print("Removing duplicates from newHistory.json")
    helper.removeDuplicates('newHistory.json')
    print("Partially generated ",len(battleDB)," battle data.")
    print("waiting for next batch...")
    time.sleep(40)
print("Total generated ",len(battleDB)," battle data.")

"""def updateHistory():
    with open("newHistory.json") as file:
        data = json.load(file)
        finalList = data + battleDB
    file.close

    with open("newHistory.json", "w") as outfile:
        outfile.write(json.dumps(finalList))
        print("newHistory file was updated but not yet trimmed, possible duplicates may arrise")
    outfile.close"""

#helper.removeDuplicates('newHistory.json')

print("Process finished --- %s seconds ---" % (time.time() - start_time))

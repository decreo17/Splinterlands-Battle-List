from functools import reduce
import json
from os import readlink, remove
import numpy as np
import traceback
import pandas as pd


#collect names from names.txt and write to users.json
with open('names.txt', 'r') as file:
    data = file.read().split(',')
    users = open('users.json', 'w')
    users.write(json.dumps(list(filter(None,data))))
    users.close()
file.close


def removeDuplicates(filePath):
    '''This will removed duplicates from json file'''
    finalData = ""
    try:
        with open(filePath, 'r') as file:
            data = json.load(file)
            cleaned = np.unique(data)
            cleaned = list(filter(None, cleaned))
            print(str(len(cleaned)) +  " unique items.")
            finalData = json.dumps(cleaned)
        file.close

        with open(filePath, 'w') as file:
            file.write(finalData)
        file.close

    except TypeError:
        
        #cleaned = []
        #[cleaned.append(x) for x in data if x not in cleaned] 
        cleaned = []
        counter = 0
        for i in range(0, len(data)):
            if data[i] not in data[i+1:]:
                cleaned.append(data[i])
                counter = counter + 1
                print(counter, " of ", len(data))
        cleaned = list(filter(None, cleaned))
        print(str(len(cleaned)) +  " unique items.")
        finalData = json.dumps(cleaned)
        file.close

        with open(filePath, 'w') as file:
            file.write(finalData)
        file.close 
        
        """
        cleaned = pd.DataFrame(data)
        cleaned.drop_duplicates
        cleaned = list(filter(None, cleaned))
        print(str(len(cleaned)) +  " unique items.")
        finalData = json.dumps(cleaned)
        file.close

        with open(filePath, 'w') as file:
                file.write(finalData)
        file.close 
        """
    except Exception as e:
        print(traceback.format_exc())

removeDuplicates('newHistory.json')

    
    

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 16:41:02 2021

@author: Yasamin Moghaddas
"""

import requests
import json
import matplotlib.pyplot as plt
import csv
from datetime import date

with requests.Session() as session:
    appID = 'dc2b9c1a'
    appKey = 'e107718613d41c0a17c7b6aefb05faac'
    url = 'https://trackapi.nutritionix.com'
    url_branded = url+'/v2/search/instant'
    url_common = url+'/v2/natural/nutrients'
    
    session.headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'x-app-id': appID,
                'x-app-key': appKey,
                'x-remote-user-id': '0'
    }
    
    keep_adding = True
    total_nutrition = {
        'totalCalories': 0,
        'totalFat': 0,
        'totalCarbs': 0,
        'totalFiber': 0,
        'totalSugar': 0,
        'totalProtein': 0
        }
    all_foods = list()
    
    while(keep_adding):
        
        foodType = input('Is it a common or branded food?\n')
        foodName = input('Enter the name of the food\n')
        branded = False
    
    
        if foodType == 'branded':
            branded = True
    
        
        if foodType == 'branded':
            query = {
                "query":foodName,
                'branded':branded
            }
            response = session.get(url_branded, headers=session.headers, params=query)
        else:
            query = {
                "query":foodName
            }
            response = session.post(url_common, data=query, headers=session.headers)
        r = json.loads(response.content)
    
        if foodType=='branded':
            counter = 1
            for item in r[foodType]:
                print(str(counter)+':', item['brand_name_item_name'])
                counter += 1
            item_number = int(input('This is a list of all the food options. Please type in the number associated with the food item.\n'))
            query = {
                "nix_item_id": r[foodType][item_number-1]['nix_item_id']
            }
            response = session.get(url+'/v2/search/item', headers=session.headers, params=query)
            r = json.loads(response.content)

        all_foods.append(r['foods'][0]['food_name'])

        print('Enter the number of', r['foods'][0]['serving_unit'], 'you consumed or type \'default\' to use default serving quantity\n')
        servings = input()
        if (servings=='default'):
            servings = int(r['foods'][0]['serving_qty'])
        
        total_nutrition['totalCalories'] += (int(r['foods'][0]['nf_calories'])/int(r['foods'][0]['serving_qty']))*float(servings)
        total_nutrition['totalFat'] += (int(r['foods'][0]['nf_total_fat'])/int(r['foods'][0]['serving_qty']))*float(servings)
        total_nutrition['totalCarbs'] += (int(r['foods'][0]['nf_total_carbohydrate'])/int(r['foods'][0]['serving_qty']))*float(servings)
        total_nutrition['totalFiber'] += (int(r['foods'][0]['nf_dietary_fiber'])/int(r['foods'][0]['serving_qty']))*float(servings)
        total_nutrition['totalSugar'] += (int(r['foods'][0]['nf_sugars'])/int(r['foods'][0]['serving_qty']))*float(servings)
        total_nutrition['totalProtein'] += (int(r['foods'][0]['nf_protein'])/int(r['foods'][0]['serving_qty']))*float(servings)
        
        keep_adding = input('Would you like to keep adding foods ot your log? (Y/N)\n')
        if keep_adding == 'N':
            keep_adding = False
    
    #Plot Data
    labels = ['Total Fat', 'Total Carbs', 'Total Protein']
    data = [total_nutrition['totalFat'], total_nutrition['totalCarbs'], total_nutrition['totalProtein']]
    plt.pie(data, labels=labels)
    plt.axis('equal')
    plt.show()
    
    print('Total Fat:', total_nutrition['totalFat'])
    print('Total Carbohydrates: ', total_nutrition['totalCarbs'])
    print('Total Protein:', total_nutrition['totalProtein'])         
    
    with open('food_log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date.today()])
        for info, num in total_nutrition.items():
            writer.writerow([info, num])
        f.close()
    
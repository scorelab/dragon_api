#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
/#
 # =====================================================================================
 #
 #       Filename:  server.py
 #
 #    Description:  
 #
 #        Version:  1.0.0
 #        Created:  Wed Nov  8 17:41:17 2017
 #       Revision:  none
 #       Compiler:  python3
 #
 #         Author:  
 #   Organization:  SCoRE
 #        Credits:  
 #
 # =====================================================================================
 #/
"""
import json
from flask import Flask, render_template, request, jsonify, make_response
from datetime import datetime
import pymongo
app = Flask(__name__)  # initialization

################ Utilization functions #################

def getNormalizeValue(val, maxVal, minVal):
    return (val - minVal)/(maxVal - minVal)
    
def getWeightedSum(normArr, weightArr):
    weightedSum = 0
    for i in range(0, len(normArr)):
        weightedSum += normArr[i] * weightArr[i]
    return weightedSum/sum(weightArr)
    
################ DB Handeler ###########################
uri = 'mongodb://epihack:abcdefg@ds149535.mlab.com:49535/epihack'
client = pymongo.MongoClient(uri)
db = client.get_default_database()
epihack_data = db['epihack_data']

############ WEB APP ###################################
api_base_url = '/dragon-api'

# for index.html


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # user inputs
        my_input = request.form.get('first')
        print(my_input)
    return render_template('index.html')

# /predictions?w=???


@app.route('/predictions')
def predict():
    user_input = request.args.get('w')
    data = {}
    data['results'] = user_input
    data['best_match'] = "Null"
    json_data = json.dumps(data, ensure_ascii=False).encode('utf8')
    return json_data


@app.route(api_base_url + '/<string:ids>/run', methods=['GET'])
def sample1(ids):
    res = {"data": ids}
    return jsonify(res)


@app.route(api_base_url + '/add/x=<int:x>&y=<int:y>', methods=['GET'])
def sample2(x, y):
    res = {"data": x + y}
    return jsonify(res)


'''
data = {
        'district': 'D1',
        'ward': '1',
        'year': '2017',
        'month': '11',
        'week': '46',
        'data': { 'population_of_the_ward': '35832',
                'area_of_the_ward': '15378.54077',
                'no_of_public_place': '645',
                'no_of_school': '402', 
                'no_of_construction_site': '159',
                'no_of_highrise_building': '311',
                'area_of_water': '0.062',
                'area_of_abadon_house': '0.0367',
                'area_of_empty_land': '0.0361'
              }
    }
'''
@app.route(api_base_url + '/insertNew/district=<string:dis>/word=<int:word>/year=<int:yr>/month=<int:mnt>/week=<int:wk>/data=<string:json>', methods=["GET"])
def insertNew(dis, word, yr, mnt, wk, json):
    res = {'district': dis,
        'ward': word,
        'year': yr,
        'month': mnt,
        'week': wk,
        'data': json
        }
    x = db.epihack_data.insertOne(res)
    print(x)    
    return jsonify(res)

@app.route(api_base_url + '/insertData/district=<string:dis>/word=<int:word>/newdata=<string:data>', methods=['GET'])
def insertData(dis, word, data):
    res = {
        'district' : dis,
        'word' : word,
        "data" : data
        }
    return jsonify(res)
    print(res)


if __name__ == '__main__':
    app.run(debug=True)

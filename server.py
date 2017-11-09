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
import pymongo
from flask import Flask, render_template, request, jsonify, make_response
from datetime import datetime
import pymongo
app = Flask(__name__)  # initialization

################ DB Handeler ###########################
uri = 'mongodb://epihack:abcdefg@ds149535.mlab.com:49535/epihack'
client = pymongo.MongoClient(uri)
db = client.get_default_database()
epihack_data = db['epihack_data']
epihack_data_wieght = db['epihack_data_wieght']

################ Utilization functions #################


def getNormalizeValue(val, maxVal, minVal):
    return (val - minVal) / (maxVal - minVal)


def getWeightedSum(normArr, weightArr):
    weightedSum = 0
    for i in range(0, len(normArr)):
        weightedSum += normArr[i] * weightArr[i]
    return weightedSum / sum(weightArr)


def getWeight(weight_key):
    wieght_data = epihack_data_wieght.find_one(
        {'wieght_key': 'area_of_the_ward'})
    return wieght_data['wieght']


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
    data = {'district': dis,
            'ward': word,
            'year': yr,
            'month': mnt,
            'week': wk,
            'data': json
            }

    res = epihack_data_wieght.insert_one(data)
    return jsonify({'acknowledged': res.acknowledged})


@app.route(api_base_url + '/insertDataWieght/wieght_key=<string:wieght_key>/wieght_name=<string:wieght_name>/wieght=<int:wieght>', methods=['GET'])
def insertDataWieght(wieght_key, wieght_name, wieght):

    wieght_data = {
        'wieght_key': wieght_key,
        'wieght_name': wieght_name,
        "wieght": wieght
    }

    res = epihack_data_wieght.insert_one(wieght_data)
    return jsonify({'acknowledged': res.acknowledged})


if __name__ == '__main__':
    app.run(debug=True)

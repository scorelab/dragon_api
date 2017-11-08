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

app = Flask(__name__) # initialization


################ DB Handeler ###################

# mongodb://charitha:abcdefg123@ds149535.mlab.com:49535/epihack


############ WEB APP ########################



api_base_url = '/test-api'
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
    res = {"data" : ids}
    return jsonify(res)

@app.route(api_base_url + '/add/x=<int:x>&y=<int:y>', methods=['GET'])
def sample2(x,y):
    res = {"data" : x+y}
    return jsonify(res)




if __name__ == '__main__':
    app.run(debug=True)
    

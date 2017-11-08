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
 #         Author:  lasithniro (c)
 #   Organization:  L2N Inc.
 #        Credits:  
 #
 # =====================================================================================
 #/
"""



import difflib
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import json
from flask import Flask, render_template, request, jsonify, make_response
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

############ WEB APP ########################

app = Flask(__name__) # initialization

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # user inputs
        my_input = request.form.get('first')
        print(my_input)
    return render_template('index.html')

        
@app.route('/predictions')
def predict():
    user_input = request.args.get('w')
    data = {}
    data['results'] = user_input
    data['best_match'] = "Null"
    json_data = json.dumps(data, ensure_ascii=False).encode('utf8')
    return json_data

 
if __name__ == '__main__':
    app.run(debug=True)

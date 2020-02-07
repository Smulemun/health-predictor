# -*- coding: utf-8 -*-
from flask import Flask, url_for, render_template, request, redirect, session
from symptomaddform import SymptomAddForm
from symptommodel import SymptomModel
from illnessmodel import IllnessModel
from predictform import PredictForm
from shutil import copy
from db import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'codeday'

symptoms_db = DB('symptoms.db')
symptoms_init = SymptomModel(symptoms_db.get_connection())
symptoms_init.init_table()

illnesses_db = DB('illnesses.db')
illnesses_init = IllnessModel(illnesses_db.get_connection())
illnesses_init.init_table()


@app.route('/addsymptom', methods=['GET', 'POST'])
def addsymptom():
    
    form = SymptomAddForm()
    
    if form.validate_on_submit():
        symptom = form.symptom.data
        illness = form.illness.data
        
        illness_model = IllnessModel(illnesses_db.get_connection())
        illness_id = illness_model.exists(illness)[1]       
        
        symptom_model = SymptomModel(symptoms_db.get_connection())
        data = symptom_model.exists(symptom)        
        
        if not data[0]:            
            symptom_model.insert(symptom, illness, illness_id)
            return redirect("/addsymptom")
    return render_template('addsymptom.html', title='Add Symptom', form=form)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    
    form = PredictForm()
    
    if form.validate_on_submit():
        
        data = []
        
        symptom_model = SymptomModel(symptoms_db.get_connection())
        illness_model = IllnessModel(illnesses_db.get_connection())        
        
        symptom1 = form.symptom1.data
        data.append(symptom_model.exists(symptom1)[0])
        symptom2 = form.symptom2.data
        data.append(symptom_model.exists(symptom2)[0])
        symptom3 = form.symptom3.data
        data.append(symptom_model.exists(symptom3)[0])
        symptom4 = form.symptom4.data
        data.append(symptom_model.exists(symptom4)[0])
        symptom5 = form.symptom5.data 
        data.append(symptom_model.exists(symptom5)[0])  

        cooler_data = 'Q'.join(data)

        return redirect('/prediction/' + str(cooler_data))
    
    return render_template('predict.html', title='Health Predictor', form=form)

@app.route('/prediction/<string:data>')
def prediction(data):
    
    illness_model = IllnessModel(illnesses_db.get_connection())
    
    real_data = list(map(int, data.split('Q')))

    illnesses = []
    for i in real_data:
        illness = illness_model.get(i)
        if illness != 'no illness':
            illnesses.append(illness)
    
    illnesses.sort()
    print(illnesses)
    cur = 1
    q = []
    for i in range(1, len(illnesses)):
        if illnesses[i] == illnesses[i - 1]:
            cur += 1
        else:
            q.append((illnesses[i - 1], cur))
            cur = 1 
    if illnesses[-1] == illnesses[-2]:
        q.append((illnesses[-1], cur))
    else:
        q.append((illnesses[-1], 1))
    
    for i in q:
        print(i[0], str(int(i[1]/len(illnesses) * 100)) + '%')
    
    return render_template('index.html', title='Health Predictor')

@app.route('/')
@app.route('/index')
def index():
    

    return render_template('index.html', title='Health Predictor')

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
from flask import Flask, url_for, render_template, request, redirect, session
from db import DB
from symptommodel import SymptomModel
from illnessmodel import IllnessModel
from predictform import PredictForm

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'codeday2020'

symptoms_db = DB('symptoms.db')
symptoms_init = SymptomModel(symptoms_db.get_connection())
symptoms_init.init_table()

illnesses_db = DB('illnesses.db')
illnesses_init = IllnessModel(illnesses_db.get_connection())
illnesses_init.init_table()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='CheckApp')

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
        
        symptom1 = form.symptom1.data
        for symptom in symptom_model.exists(symptom1):
            data.append(symptom[0])
        symptom2 = form.symptom2.data
        for symptom in symptom_model.exists(symptom2):
            data.append(symptom[0])
        symptom3 = form.symptom3.data
        for symptom in symptom_model.exists(symptom3):
            data.append(symptom[0])
        symptom4 = form.symptom4.data
        for symptom in symptom_model.exists(symptom4):
            data.append(symptom[0])
        symptom5 = form.symptom5.data 
        for symptom in symptom_model.exists(symptom5):
            data.append(symptom[0])          
            
        data = list(map(str, data))
        cooler_data = 'Q'.join(data)

        return redirect('/prediction/' + str(cooler_data))
    
    return render_template('predict.html', title='CheckApp', form=form)

@app.route('/prediction/<string:data>')
def prediction(data):
    
    illness_model = IllnessModel(illnesses_db.get_connection())
    symptom_model = SymptomModel(symptoms_db.get_connection())

    symptom_data = list(map(int, data.split('Q')))
    
    illnesses = {}
    for i in symptom_data:
        symptom = symptom_model.get(i)
        illness = illness_model.get(symptom[3])
        if illness != ' No Disease':
            if illness not in illnesses:
                illnesses[illness] = round(float(symptom[2]) / 100, 2)
            else:
                illnesses[illness] += round(float(symptom[2]) / 100, 2)
            illnesses[illness] = round(illnesses[illness], 2)
            
    diseases = []
    for i in illnesses.keys():
        diseases.append([i, str(float(illnesses[i]) / sum(illnesses.values()) * 100) + '%'])
        print(i, str(float(illnesses[i]) / sum(illnesses.values()) * 100) + '%')
    
    return render_template('prediction.html', title='CheckApp', diseases=diseases)

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
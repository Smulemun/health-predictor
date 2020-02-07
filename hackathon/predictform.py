from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from illnessmodel import IllnessModel
from symptommodel import SymptomModel
from db import DB
 
symptoms_db = DB('symptoms.db')
symptoms_init = SymptomModel(symptoms_db.get_connection())
symptoms_init.init_table()

symptom_model = SymptomModel(symptoms_db.get_connection())
data = symptom_model.get_all() 
choice = []
 
for i in data:
    choice.append((i[1], i[1]))
    
choice.sort()
 
class PredictForm(FlaskForm):
       
    
    symptom1 = SelectField('Symptom #1', choices=choice)
    symptom2 = SelectField('Symptom #2', choices=choice)
    symptom3 = SelectField('Symptom #3', choices=choice)
    symptom4 = SelectField('Symptom #4', choices=choice)
    symptom5 = SelectField('Symptom #5', choices=choice)
    submit = SubmitField('Submit')
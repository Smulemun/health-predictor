from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from illnessmodel import IllnessModel
from db import DB
 
illnesses_db = DB('illnesses.db')
illnesses_init = IllnessModel(illnesses_db.get_connection())
illnesses_init.init_table()

illness_model = IllnessModel(illnesses_db.get_connection())
data = illness_model.get_all() 
choice = []
 
for i in data:
    choice.append((i[1], i[1]))
    
choice.sort()
 
class SymptomAddForm(FlaskForm):
       
    
    symptom = StringField('Symptom', validators=[DataRequired()])
    illness = SelectField('Illness', choices=choice)
    submit = SubmitField('Submit')
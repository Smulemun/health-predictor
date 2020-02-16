import sqlite3
 
class SymptomModel():
    def __init__(self, connection):
        self.connection = connection
        
    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS symptoms 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             symptom VARCHAR(50),
                             sensitivity VARCHAR(50),
                             illness_id VARCHAR(50))''')
        cursor.close()
        self.connection.commit()
     
    def insert(self, symptom, illness, sensitivity, illness_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO symptoms 
                          (symptom, sensitivity, illness_id) 
                          VALUES (?,?,?)''', (symptom, sensitivity, illness_id))
        cursor.close()
        self.connection.commit()     
        
    def exists(self, symptom):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM symptoms WHERE symptom = ?", (symptom,))
        row = cursor.fetchall()
        return row
    
    def get(self, symptom_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM symptoms WHERE id = ?", (str(symptom_id),))
        row = cursor.fetchone()
        return row
    
    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM symptoms")
        rows = cursor.fetchall()
        return rows    
import sqlite3  

class IllnessModel():
    def __init__(self, connection):
        self.connection = connection
        
    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS illnesses
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             illness VARCHAR(50))''')
        cursor.close()
        self.connection.commit()
     
    def insert(self, illness):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO illnesses 
                          (illness) 
                          VALUES (?)''', (illness))
        cursor.close()
        self.connection.commit()     
        
    def exists(self, illness):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM illnesses WHERE illness = ?", (illness,))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)
    
    def get(self, illness_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM illnesses WHERE id = ?", (int(illness_id),))
        row = cursor.fetchone()
        return row[1]     
    
    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM illnesses")
        rows = cursor.fetchall()
        return rows    
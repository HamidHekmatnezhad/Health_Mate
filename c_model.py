import face_recognition
import numpy as np
import face_recognition_models
import sql_infos
import mysql.connector as DB

class FaceRec:

    def __init__(self, model_loc='hog', model_encode='small', num_jitters=1):
        """
        model_loc: 'hog' or 'cnn'
        num_jitters: How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
        model_encode: Optional - which model to use. “large” or “small” (default) which only returns 5 points but is faster.
        """
        self.face_data = []
        self.id_data = []

        self.model_loc = model_loc # 'hog' & 'cnn'
        self.model_encode = model_encode # 'small' or 'large'
        self.num_jitters = num_jitters # 1 to 100 ...

        self.HOSTNAME = sql_infos.HOSTNAME
        self.USER = sql_infos.USER
        self.PASSWORD = sql_infos.PASSWORD
        self.DATABASE = "sql_personal_data"

    def write_data(self, img, codeid: int, fname=None, lname=None, birth_date=None, gender=None):
        """
        insert face id with code id in to database and ...
        one person in a photo.

        img: numpy array,
        codeid: int,
        """
        try: 
            loc = face_recognition.face_locations(img, model=self.model_loc)
            encode = face_recognition.face_encodings(face_image=img, known_face_locations=loc, num_jitters=self.num_jitters, model=self.model_encode)[0]

            temp = []
            for x in encode:
                temp.append(float(x))

            temp_str = str()

            for s in temp:
                temp_str += str(s) + ', '

            sql_item = 'codeid, face_id'
            sql_value = f'{codeid}, "{temp_str}"'

            if fname:
                sql_item += ', first_name'
                sql_value += f', "{fname}"'

            if lname:
                sql_item += ', last_name'
                sql_value += f', "{lname}"'

            if birth_date:
                sql_item += ', birth_date'
                sql_value += f', "{birth_date}"'

            if gender:
                sql_item += ', gender'
                sql_value += f', "{gender}"'

            con = DB.connect(
                        host=self.HOSTNAME,
                        user=self.USER,
                        password=self.PASSWORD,
                        database=self.DATABASE
                            )
            
            cur = con.cursor()
            cur.execute(f'INSERT INTO personal_data ({sql_item}) VALUES ({sql_value})')
            con.commit()
            cur.close()
            con.close()
            return True
        
        except:
            print('Error in write_data')
            return False
              
    def raed_face_id_data(self): # read_data
        """read face id from database."""
        
        self.id_data.clear()
        self.face_data.clear()

        con = DB.connect(
                    host=self.HOSTNAME,
                    user=self.USER,
                    password=self.PASSWORD,
                    database=self.DATABASE
                        )
        cur = con.cursor()

        cur.execute("SELECT client_id, face_id FROM personal_data")
        records = cur.fetchall()
        cur.close()
        con.close()

        for record in records:

            p_id = record[0]
            row = record[1]
            row = row.split(', ')
            row.pop()
            row = [float(x) for x in row]
            face_id = np.array(row)

            self.id_data.append(p_id)
            self.face_data.append(face_id)

    def recognize_face(self, img):
        """img: numpy array
        return: id, loc, temp
        temp -> distance
        """

        loc = face_recognition.face_locations(img, model=self.model_loc)

        if len(loc) == 1:
            loc = loc[0]
            encode = face_recognition.face_encodings(face_image=img, known_face_locations=[loc], num_jitters=self.num_jitters, model=self.model_encode)[0]

            isSame = face_recognition.compare_faces(self.face_data, encode)
            dist = face_recognition.face_distance(self.face_data, encode)

            temp = 1

            for i in range(len(isSame)):
                if isSame[i]:
                    if dist[i] < temp:
                        temp = dist[i]
                        result = i

            return self.id_data[result], loc, temp
            
    def query(self, id):
        """
        for test
        """

        con = DB.connect(
                    host=self.HOSTNAME,
                    user=self.USER,
                    password=self.PASSWORD,
                    database=self.DATABASE
                        )
        cur = con.cursor()

        cur.execute("SELECT person_id, code_id FROM person WHERE person_id = ?", (id,))
        record = cur.fetchall()
        cur.close()
        con.close()

        return record[0][0], record[0][1]

    def check_data(self, codeid):
        """codeid: id
        check in Database
        return: True, False
        True -> id is NOT in Database
        False -> id is in Database"""

        con = DB.connect(
                    host=self.HOSTNAME,
                    user=self.USER,
                    password=self.PASSWORD,
                    database=self.DATABASE
                        )
        
        cur = con.cursor()

        cur.execute("SELECT codeid FROM personal_data WHERE codeid = ?", (codeid,))
        record = cur.fetchone()
        cur.close()
        con.close()

        if record == None:
            return True
        else:
            return False




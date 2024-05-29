import face_recognition
import numpy as np
import face_recognition_models
import sqlite3

class FaceRec:

    def __init__(self, model_loc='hog', model_encode='small', num_jitters=1):
        """
        model_loc: can be 'hog' or 'cnn'
        num_jitters: How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
        model_encode: Optional - which model to use. “large” or “small” (default) which only returns 5 points but is faster.
        """
        self.face_data = []
        self.id_data = []

        self.model_loc = model_loc # 'hog' & 'cnn'
        self.model_encode = model_encode # 'small' or 'large'
        self.num_jitters = num_jitters # 1 to 100 ...

    def collect_data(self, img, person_id):
        """
        one person must be in a photo.

        img: must a numpy array,
        person_id: must be a integer,
        """

        loc = face_recognition.face_locations(img, model=self.model_loc)
        encode = face_recognition.face_encodings(face_image=img, known_face_locations=[loc], num_jitters=self.num_jitters, model=self.model_encode)

        check = self.insert_data(encode=encode, person_id=person_id)
        if check:
            print('Data Inserted')
        else:
            print('Data Not Inserted, have a problem')

    def insert_data(self, encode, person_id):
        """ insert face id with code id in to database."""
        try: 
            temp = [float(x) for x in encode]
            temp_str = str()

            for s in temp:
                temp_str += str(s) + ', '

            con = sqlite3.connect('db/faceid.db')
            cur = con.cursor()
            cur.execute("INSERT INTO faceid (code_id, face_code) VALUES (?, ?)", (person_id, temp_str))
            con.commit()
            con.close()
            return True
        
        except:
            return False
        
    def get_data(self):
        """get data from database."""
        con = sqlite3.connect('db/faceid.db')
        cur = con.cursor()

        cur.execute("SELECT person_id, face_code FROM person")
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

    def recognize_face(self, img, req_loc=False):
        """img: numpy array
        return: id person
        return: if req_loc == True return id person and location of face in image"""

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

            if req_loc:
                return self.id_data[result], loc
            else:
                return self.id_data[result]
            
    def query(self, id):
        """for test
        return; id, code_id person"""

        con = sqlite3.connect('db/faceid.db')
        cur = con.cursor()

        cur.execute("SELECT person_id, code_id FROM person WHERE person_id = ?", (id,))
        record = cur.fetchall()
        cur.close()
        con.close()

        return record[0][0], record[0][1]





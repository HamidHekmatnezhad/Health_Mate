import face_recognition
import numpy as np
import face_recognition_models
import sqlite3

class FaceRec:

    def __init__(self):
        pass

    def collect_data(self, img, person_id, model_loc='hog', model_encode='small', num_jitters=1):
        """
        one person must be in a photo.

        img: must a numpy array,
        person_id: must be a integer,
        model_loc: can be 'hog' or 'cnn'
        num_jitters: How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
        model_encode: Optional - which model to use. “large” or “small” (default) which only returns 5 points but is faster.
        """

        loc = face_recognition.face_locations(img, model=model_loc)
        encode = face_recognition.face_encodings(face_image=img, known_face_locations=[loc], num_jitters=num_jitters, model=model_encode)

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
        
    def recognize_face(self):
        pass




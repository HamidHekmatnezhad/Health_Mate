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

            sql_item = 'codeid, face_id, date_added'
            sql_value = f'{codeid}, "{temp_str}", NOW()'

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
              
    def update_faces_ids(self): 
        """read face id from database."""

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

        self.id_data.clear()
        self.face_data.clear()

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
            check_exist = False

            for i in range(len(isSame)):
                if isSame[i]:
                    check_exist = True
                    if dist[i] < temp:
                        temp = dist[i]
                        result = i
            if check_exist:
                return self.id_data[result], loc, temp
            else: 
                return False, False, False
        else:
            return False, False, False

    def check_flag(self): 
        """
        check flag
        return: record
        """

        con = DB.connect(
                    host=self.HOSTNAME,
                    user=self.USER,
                    password=self.PASSWORD,
                    database=self.DATABASE
                        )
        
        cur = con.cursor()

        # read FLAG
        cur.execute(f'SELECT * FROM control_send ORDER BY f_id DESC LIMIT 1;')
        flag = cur.fetchone()

        # read row data
        if flag[1] == 0:
            # chenged row_hd  to log
            cur.execute(f'SELECT * FROM log ORDER BY id DESC LIMIT 1;')
            record = cur.fetchone()
            # if record[1] and record[2] and record[3] and record[4]:
            if record:
                cur.close()
                con.close()
                return record

        else:
            cur.close()
            con.close()
            return None

    def write_health_record(self, id, record):
            """submit buttom"""
            try:
                con = DB.connect(
                        host=self.HOSTNAME,
                        user=self.USER,
                        password=self.PASSWORD,
                        database=self.DATABASE
                            )
            
                cur = con.cursor()
                # recv = id, timestamp, hearthbeat, oxygen, weight_kg, temperatur, -
                # index=  0,   1,          2,          3,        4,        5,       6
                print(record)
                cur.execute(f'INSERT INTO health_record (client_id, hearthbeat, oxygen, weight_kg, temperature, date_added) VALUES ({id}, {record[-4]}, {record[-3]}, {record[-2]}, {record[-1]}, NOW());')
                con.commit()

                cur.execute(f'DELETE FROM row_hd WHERE r_id = {record[0]};')
                con.commit()

                cur.close()
                con.close()
                return True
            
            except:
                return False

    def query_one_client_info(self, id):
        """
        querry data from personal_data all record for one client
        """

        con = DB.connect(
                    host=self.HOSTNAME,
                    user=self.USER,
                    password=self.PASSWORD,
                    database=self.DATABASE
                        )
        
        cur = con.cursor()

        cur.execute(f"SELECT * FROM personal_data WHERE client_id = {id}")
        records = cur.fetchone()
        cur.close()
        con.close()

        return records

    def query_one_client_hr(self, id): 
        """
        querry data from health_record all record for one client
        """

        con = DB.connect(
                    host=self.HOSTNAME,
                    user=self.USER,
                    password=self.PASSWORD,
                    database=self.DATABASE
                        )
        
        cur = con.cursor()

        cur.execute(f"SELECT * FROM health_record WHERE client_id = {id}")
        records = cur.fetchall()
        cur.close()
        con.close()

        return records

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

        cur.execute(f"SELECT client_id FROM personal_data WHERE codeid = {codeid}")
        record = cur.fetchone()
        cur.close()
        con.close()

        if record == None:
            return True
        else:
            return False

    def read_id(self, codeid):
        """read client_id from Database"""

        con = DB.connect(
                    host=self.HOSTNAME,
                    user=self.USER,
                    password=self.PASSWORD,
                    database=self.DATABASE
                        )
        
        cur = con.cursor()

        cur.execute(f"SELECT client_id FROM personal_data WHERE codeid = {codeid}")
        record = cur.fetchone()
        cur.close()
        con.close()
        if record == None:
            return False
        else:
            return record[0]

    def edit_data(self, id, codeid, fname, lname, birth_date, gender):
            """update data from personal_data"""
        # try:
            sql = ''

            if (codeid != None):
                sql += f' codeid={codeid},'
            if (fname != None):
                sql += f' first_name="{fname}",'
            if (lname != None):
                sql += f' last_name="{lname}",'
            if (birth_date != None):
                sql += f' birth_date="{birth_date}",'
            if (gender != None):
                sql += f' gender="{gender}",'
            
            sql = sql[:-1] 

            con = DB.connect(
                        host=self.HOSTNAME,
                        user=self.USER,
                        password=self.PASSWORD,
                        database=self.DATABASE
                            )
            
            cur = con.cursor()

            cur.execute(f'UPDATE personal_data SET {sql} WHERE client_id = {id}')
            con.commit()
            cur.close()
            con.close()
            return True
        
        # except:
        #     return False

    def set_flag(self, flag):
        """"""
        try:
            con = DB.connect(
                            host=self.HOSTNAME,
                            user=self.USER,
                            password=self.PASSWORD,
                            database=self.DATABASE
                                )
                
            cur = con.cursor()

            cur.execute(f'INSERT INTO control_send (flag) VALUES ({flag});')
            con.commit()
            cur.close()
            con.close()
            return True
            
        except:
            return False

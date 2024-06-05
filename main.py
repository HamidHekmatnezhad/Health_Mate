import streamlit as st
import time
import datetime
from c_model import FaceRec
import pandas as pd
import numpy as np
from PIL import Image
import face_recognition

#                   0         1             2              3            4            5
list_of_tasks = ['Help','Enrollment', 'Health Mate', 'Show Record', 'Settings', 'Edit Info']
option = list_of_tasks[0]
check_run = ''
heartbeat = []
oxygen = []
weight_kg = []
temperature = []
date_added = []

def edit_info_data():

    app, id, check_run = entry_optional()

    if check_run:
        info = app.query_one_client_info(id)
        id_p = st.text_input(label='ID', help='please enter id. example= 1234567890', placeholder=str(info[1]))
        col = []
        col = st.columns(2)
        fname = col[0].text_input(label='First Name', placeholder=info[2])
        lname = col[1].text_input(label='Last Name', placeholder=info[3])
        col2 = st.columns(2)
        gender = col2[0].selectbox('Gedner', {info[6], 'None', 'Male', 'Female'})
        birth_date = col2[1].date_input("Your Birthday", value=info[5], min_value=datetime.datetime(1900, 1, 1))

        subcheck = st.button(label="Submit", type="primary", use_container_width=True)

        if (int(id_p) == info[1]) or (id_p == ''):
            id_p = None
        if (gender == 'None') or (gender == info[6]):
            gender = None
        if (fname == info[2]) or (fname == ''):
            fname = None
        if (lname == '') or (lname == info[3]):
            lname = None
        if (birth_date == info[5]) or (birth_date == ''):
            birth_date = None

        check_update = app.edit_data(id, int(id_p), fname, lname, birth_date, gender)

        if check_update:
            st.success('### Successfully Updated')
            st.balloons()
        else:
            st.error('### Failed to Update')

    elif (check_run == False):
        st.error('### NOT Found')

def print_infos(info_data):
    client_id = info_data[0]
    codeid = info_data[1]
    first_name = info_data[2]
    last_name = info_data[3]
    face_id = info_data[4]
    if face_id:
        face_id = 'True'
    gender = info_data[5]
    birth_date = info_data[6]
    date_added = info_data[7]

    df = pd.DataFrame({'ID': [codeid], 'First Name': [first_name], 'Last Name': [last_name], 'Gender': [gender], 'Birth Date': [birth_date], 'Date Added': [date_added]})
    st.dataframe(df)
    
    st.write(f'''
            |ID*|First Name|Last Name|Birth Date|Gender|Date Added|
            |--|--|--|--|--|--|
            |{str(codeid)}|{first_name}|{last_name}|{str(birth_date)}|{gender}|{str(date_added)}|
             ''')

def print_hr(hr_data):
    if len(hr_data) == 0:
        st.write('no Health Record')

    elif len(hr_data) != 0:
        heartbeat.clear()
        oxygen.clear()
        weight_kg.clear()
        temperature.clear()
        date_added.clear()
        
        for record in hr_data:
            heartbeat.append(record[2])
            oxygen.append(record[3])
            weight_kg.append(record[4])
            temperature.append(record[5])
            date_added.append(record[6])
        
        df = pd.DataFrame({'Heartbeat': heartbeat, 'Oxygen': oxygen, 'Weight (kg)': weight_kg, 'Temperature': temperature, 'Date Added': date_added})
        st.dataframe(df)

def entry_optional():
    global check_run
    app = FaceRec()
    switch = st.radio('Switch: ', ['Picture', 'ID'])

    if switch == 'ID':
        id = st.text_input(label='ID', help='please enter id. example= 1234567890', placeholder='*1234567890')
        btn = st.button(label="Submit", type="primary")
        if btn or id:
            id = int(id)
            id = app.read_id(id)
            check_id = app.check_data(id)
            if check_id:
                check_run = False
                st.error('### id is not exist')
            else:
                check_run = True

    elif switch == 'Picture':
        pic = st.camera_input('take a picture')

        if pic:
            img = Image.open(pic)
            img_array = np.array(img)

            app.update_faces_ids()
            id, loc, dist = app.recognize_face(img_array)
    
            if (id == None):
                return app, id, False
                st.error('### face NOT found!!!')
            
            else: 
                return app, id, True

def page_help():
    st.write('in ***development***...')
    
def page_enrollment():

    id_p = st.text_input(label='ID', help='please enter id. example= 1234567890', placeholder='*1234567890')
    col = []
    col = st.columns(2)
    fname = col[0].text_input(label='First Name', placeholder='hamid')
    lname = col[1].text_input(label='Last Name', placeholder='hekmat')
    col2 = st.columns(2)
    gender = col2[0].selectbox('Gedner', ['None', 'Male', 'Female'], )
    birth_date = col2[1].date_input("Your Birthday", value=None, min_value=datetime.datetime(1900, 1, 1))

    subcheck = st.button(label="Submit", type="primary", use_container_width=True)

    if gender == 'None':
        gender = None
    if fname == '':
        fname = None
    if lname == '':
        lname = None

    if subcheck and id_p:

        st.write(f'''
             |ID*|first name|last name|Gender|Birth Date|
             |---|---|---|---|---|
             |{id_p}|{fname}|{lname}|{gender}|{birth_date}|
             ''')
        
        app = FaceRec()
        check = app.check_data(int(id_p))

        if check: 
            pic = st.camera_input('take a picture')

            if pic:
                subpic = st.button(label="SEND PHOTO", type="primary", use_container_width=True)

                if subpic:
                    img = Image.open(pic)
                    img_array = np.array(img)

                    check = app.write_data(img_array, int(id_p), fname, lname, birth_date, gender)
        
                    if check:
                        st.success('Data inserted, done!')
                        st.balloons()

                    else:
                        st.error('Data not inserted, try again!')

        else:
            st.error('### id is exist')

def page_health_mate():

    app, id, check_run = entry_optional()

    if check_run:
        info_data = app.query_one_client_info(id)
        print_infos(info_data)

        cid = info_data[0]
        while True:
            hr = app.check_flag()
            if hr != None:
                break

        check_hr = app.write_health_record(cid, hr)
        
        if check_hr and (type(check_hr) == bool):
            st.success('Data inserted, done!')
            st.balloons()

            df = pd.DataFrame({'Heartbeat': [hr[1]], 'Oxygen': [hr[2]], 'Weight (KG)': [hr[3]], 'Temperature': [hr[4]]})
            st.dataframe(df)
            check_run = ''
            
        elif ((type(check_hr) == bool) and (check_hr == False)):
            st.error('Data not inserted, try again!')
        

    elif (check_run == False):
        st.error('### NOT Found')

def page_show_record():
    
    app, id, check_run = entry_optional()

    if check_run:
        info_data = app.query_one_client_info(id)
        health_data = app.query_one_client_hr(id)

        print_infos(info_data)
        
        if health_data != None:
            print_hr(health_data)

    elif (check_run == False):
        st.error('### NOT Found')

def page_settings():
    st.write('in ***development***...')

# region main
option = st.selectbox('switch slide: ', list_of_tasks)

st.title(option.upper())

if option == list_of_tasks[0]:
    page_help()

elif option == list_of_tasks[1]:
    page_enrollment()

elif option == list_of_tasks[2]:
    page_health_mate()

elif option == list_of_tasks[3]:
    page_show_record()

elif option == list_of_tasks[4]:
    page_settings()

elif option == list_of_tasks[5]:
    edit_info_data()

# endregion
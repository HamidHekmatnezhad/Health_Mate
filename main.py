import streamlit as st
import time
import datetime
from c_model import FaceRec
import pandas as pd
import numpy as np
from PIL import Image
import face_recognition
import random
import matplotlib.pyplot as plt


#                   0         1             2              3            4            5
list_of_tasks = ['Help','Enrollment', 'Health Mate', 'Show Record', 'Settings', 'Edit Info']
option = list_of_tasks[0]
check_run, id, app = False, False, False
heartbeat = []
oxygen = []
weight_kg = []
temperature = []
date_added = []

def edit_info_data():

    app, id, check_run = entry_optional()
    check_update = 0
    id_p = '0'
    if check_run:
        info = app.query_one_client_info(id)
        
        df = pd.DataFrame({'ID': [info[1]], 'First Name': [info[2]], 'Last Name': [info[3]], 'Gender': [info[6]], 'Birth Date': [info[5]]})
        st.dataframe(df, hide_index=True, use_container_width=True)
        inx = ["None", "Male", "Female"]
        xx = inx.index(info[6])

        id_p = st.number_input(label='ID', help='please enter id. example= 1234567890', value=info[1])
        col = []
        col = st.columns(2)
        fname = col[0].text_input(label='First Name', value=info[2])
        lname = col[1].text_input(label='Last Name', value=info[3])
        col2 = st.columns(2)
        gender = col2[0].selectbox('Gedner', ['None', 'Male', 'Female'], index=xx)
        birth_date = col2[1].date_input("Your Birthday", value=info[5], min_value=datetime.datetime(1900, 1, 1))
        

        if (id_p == info[1]) or (id_p == ''):
            id_p = None
        if (gender == 'None') or (gender == info[6]):
            gender = None
        if (fname == info[2]) or (fname == ''):
            fname = None
        if (lname == '') or (lname == info[3]):
            lname = None
        if (birth_date == info[5]) or (birth_date == ''):
            birth_date = None
    
            subcheck = st.button(label="Submit", type="primary", use_container_width=True)
            if subcheck:
                check_update = app.edit_data(id, id_p, fname, lname, birth_date, gender)

            if check_update:
                st.success('### Successfully Updated')
                st.balloons()
            else:
                if (type(check_update) == bool):
                    st.error('### Failed to Update')

    elif (check_run == False) and (id == 0):
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
    st.dataframe(df, hide_index=True, use_container_width=True)
    
def print_hr(hr_data):
    if len(hr_data) == 0:
        st.write('## no Health Record')

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

        import numpy as np
        df = pd.DataFrame({'Heartbeat': heartbeat, 'Oxygen': oxygen, 'Weight (kg)': weight_kg, 'Temperature': temperature, 'Date Added': date_added})
        st.dataframe(df, use_container_width=True)

        for t in range(len(temperature)):
            weight_kg[t] = int(weight_kg[t])
            temperature[t] = int(temperature[t])
        df = pd.DataFrame({'Heartbeat': heartbeat, 'Oxygen': oxygen, 'Weight (kg)': weight_kg, 'Temperature': temperature, 'Date Added': date_added, "col3": ["A", "B", "C", "D", "E"], "Time": [0,1,2,3,4], "e": "A"})
        st.line_chart(df,  y=['Heartbeat', 'Oxygen', 'Weight (kg)', 'Temperature'])
        
        list_style = ['default', 'bmh', 'dark_background', 'Solarize_Light2', 'grayscale', 'seaborn-pastel', 'classic']
        col = st.columns(2)
        style_s = col[0].selectbox('Select a style', list_style, index=0)
        plt.style.use(style_s)
        plt.grid(False)
        fig, axs = plt.subplots(1)
        fig.suptitle('Health Record')
        axs.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)

        axs.plot([x for x in range(len(heartbeat))], heartbeat, label='Heartbeat', linestyle='--')
        axs.plot([x for x in range(len(heartbeat))], oxygen, label='Oxygen', linestyle='-.')
        axs.plot([x for x in range(len(heartbeat))], weight_kg, label='Weight (kg)', linestyle=':')
        axs.plot([x for x in range(len(heartbeat))], temperature, label='Temperature', linestyle='-')
        axs.legend(loc='upper left')
        st.pyplot(fig)

        

def entry_optional():
    global check_run
    id = 0
    app = FaceRec()
    switch = st.radio('Switch: ', ['Picture', 'ID'])

    if switch == 'ID':
        id = st.number_input(label='ID', help='please enter id. example= 1234567890', value=0)
        # btn = st.button(label="Submit", type="primary")
        if id:
            id = app.read_id(id)
            check_id = app.check_data(id)
            if check_id:
                check_run = False
            else:
                check_run = True

    elif switch == 'Picture':
        pic = st.camera_input('take a picture')

        if pic:
            img = Image.open(pic)
            img_array = np.array(img)

            app.update_faces_ids()
            id, loc, dist = app.recognize_face(img_array)
    
    if (id != 0):
        return app, id, True
    
    else:
        if (id == False):
            return app, 0, False

def page_help():
    st.write('in ***development***...')
    
def page_enrollment():

    id_p = st.number_input(label='ID', help='please enter id. example= 1234567890', value=0)
    col = []
    col = st.columns(2)
    fname = col[0].text_input(label='First Name', placeholder='hamid')
    lname = col[1].text_input(label='Last Name', placeholder='hekmat')
    col2 = st.columns(2)
    gender = col2[0].selectbox('Gedner', ['None', 'Male', 'Female'], )
    birth_date = col2[1].date_input("Your Birthday", value=None, min_value=datetime.datetime(1900, 1, 1))

    # subcheck = st.button(label="Submit", type="primary", use_container_width=True)

    if gender == 'None':
        gender = None
    if fname == '':
        fname = None
    if lname == '':
        lname = None

    if id_p:
        
        df = pd.DataFrame({'ID': [id_p], 'First Name': [fname], 'Last Name': [lname], 'Gender': [gender], 'Birth Date': [birth_date]})
        st.dataframe(df, hide_index=True, use_container_width=True)
        
        app = FaceRec()
        check = app.check_data(int(id_p))

        if check: 
            pic = st.camera_input('take a picture')

            if pic:
                subpic = st.button(label="SEND PHOTO", type="primary", use_container_width=True)

                if subpic:
                    img = Image.open(pic)
                    img_array = np.array(img)

                    check = app.write_data(img_array, id_p, fname, lname, birth_date, gender)
        
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
            st.dataframe(df, use_container_width=True)
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
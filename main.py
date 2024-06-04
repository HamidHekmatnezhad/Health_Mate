import streamlit as st
import time
from c_model import FaceRec
import numpy as np
from PIL import Image
import face_recognition


list_of_tasks = ['main','input data', 'output', 'settings']
option = 'main'
option = st.selectbox('switch slide: ', list_of_tasks)

st.title(option.upper())

if option == 'main':
    st.write('in ***development***...')

elif option == 'input data':
    st.write('''
        input **id** and get photo.
             ''')

    id_p = st.text_input(label='input id', help='please enter id. example= 1234567890', placeholder='*1234567890')
    col = []
    col = st.columns(2)
    fname = col[0].text_input(label='first name', placeholder='hamid')
    lname = col[1].text_input(label='last name', placeholder='hekmat')

    app = FaceRec()
    check = app.check_data(id_p)
    if (check and id_p): 
        st.write(f'### id: {id_p}')
        pic = st.camera_input('take a picture')

        img = Image.open(pic)
        img_array = np.array(img)

        check = app.write_data(img_array, id_p)
        
        if check:
            st.success('Data inserted, done!')
        else:
            st.error('Data not inserted, try again!')

    else:
        st.error('### id is exist')

elif option == 'output':

    pic = st.camera_input('take a picture')

    if pic:
        img = Image.open(pic)
        img_array = np.array(img)

        app = FaceRec()
        app.raed_face_id_data()
        id, loc, dist = app.recognize_face(img_array, req_loc=True)

        st.write(f'## recognized') 
        st.write(f'### id: {id}')

        


# with st.spinner('in development...'):
#     time.sleep(5)
# st.success('Done!')
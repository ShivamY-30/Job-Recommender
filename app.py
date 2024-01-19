import pickle
import requests
import pandas as pd
import streamlit as st
from streamlit.components.v1 import iframe
from streamlit_option_menu import option_menu

#CUSTOM CSS
hide_btn = """
         <style> 
    
         .st-emotion-cache-6q9sum, .ef3psqc4 {visibility : hidden;}
         .st-emotion-cache-1wbqy5l, .e17vllj40 {visibility : hidden;}
         
         </style>

"""

st.markdown(hide_btn , unsafe_allow_html=True)
def about_us():
    st.title("Welcome to our innovative job recommendation algorithm!")
    st.divider()

    st.write("Our algorithm leverages advanced machine learning techniques to analyze your selected skills "
             "and predict potential job options that align with your expertise. By considering your unique skill set, "
             "we provide tailored recommendations, ensuring you explore opportunities that match your capabilities. "
             "Unlock a world of career possibilities with our cutting-edge algorithm, guiding you towards fulfilling "
             "and rewarding professional paths. Elevate your career journey with precision and personalized recommendations.")
    st.divider()
    st.divider()

st.sidebar.image("logo.png",width=150, use_column_width=False)

with st.sidebar:
       selected = st.selectbox(
            "Navigate",
            ["Home", "About Us"]
        )


if selected == "About Us":
    about_us()





#FUNCTIONS SECTION


def find_des(title):
    job_index = jobs[jobs['jobtitle'] == title].index[0]
    print(job_index)
    text = jobs.jobdescription[job_index]
    return text




def recommend(skill):
    a = 0
    job_index = jobs[jobs['skills'] == skill].index[0]
    distances = similarity[job_index]
    job_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    job_output = []
    try:
        for i in job_list:
            if a < 4:
                job_output.append(jobs.iloc[i[0]].jobtitle)
                a = a + 1
            else:
                break
    except IndexError:
        print("")
    return job_output


# TITLE SECTION

st.header('Job recommendation system')
st.divider()

#IMPORTING FILES
job_dict = pickle.load(open('job_recommend.pkl', 'rb'))
jobs = pd.DataFrame(job_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


#SELECTBOX SECTION
Selected_skill = st.selectbox(
    'Enter or  Select Your skill',
    jobs['skills'].values)
st.write('You selected skill :', Selected_skill)

# FETCH AND OUTPUT SECTION
if st.button('Recommend?', type="primary"):
    container = st.container(border=True)
    container.write('And below are the closest Job Options you can pursue : ')
    try:
        recomendations = recommend(Selected_skill)
        num_elements = len(recomendations)

            # Calculate the number of columns per row (you can adjust this based on your preference)
        columns_per_row = 2

        # Calculate the number of rows
        num_rows = (num_elements + columns_per_row - 1) // columns_per_row

        # Generate rows and columns dynamically
        rows = [st.columns(columns_per_row) for _ in range(num_rows)]

        # Iterate through recommendations and display in dynamically generated rows and columns
        element_counter = 0
        n = 20
        for row in rows:
            for col in row:
                if element_counter < num_elements:
                    text = find_des(recomendations[element_counter])
                    x =  str(text)
                    type(x)
                    result_list = x.split()[:n]
                    result_str = " ".join(result_list)
                     # input_str = "Python is a programming language and we can develop applications using it"


                    col.write(

                        f'<div style="border: 2px solid red; padding:10px 10px; margin: 5px; border-radius:8px">Job Title/Position : {recomendations[element_counter]} <br>Job Description : {result_str}...</div>',
                        unsafe_allow_html=True
                    )
                    element_counter += 1
    except IndexError:
        st.write("⚠️ Sorry At current time we are not having enough Information regarding your inputs, to suggest you your desired output! Please try again later ")

    # # Calculate the number of columns per row (you can adjust this based on your preference)
    # columns_per_row = 2
    #
    # # Calculate the number of rows
    # num_rows = (num_elements + columns_per_row - 1) // columns_per_row
    #
    # # Generate rows and columns dynamically
    # rows = [st.columns(columns_per_row) for _ in range(num_rows)]
    #
    # # Iterate through recommendations and display in dynamically generated rows and columns
    # element_counter = 0
    # n = 20
    # for row in rows:
    #     for col in row:
    #         if element_counter < num_elements:
    #             text = find_des(recomendations[element_counter])
    #             x =  str(text)
    #             type(x)
    #             result_list = x.split()[:n]
    #             result_str = " ".join(result_list)
    #              # input_str = "Python is a programming language and we can develop applications using it"
    #
    #
    #             col.write(
    #
    #                 f'<div style="border: 2px solid red; padding:10px 10px; margin: 5px; border-radius:8px">Job Title/Position : {recomendations[element_counter]} <br>Job Description : {result_str}...</div>',
    #                 unsafe_allow_html=True
    #             )
    #             element_counter += 1
    #

# Footer
footer_html = """
    <style>
        .footer {
            margin-top:50px;
            background-color:  rgb(14, 17, 23);
            color:yellow;
            padding: 10px;
            text-align: center;
        }
    </style>

    <div class="footer">
        <p>© EduSync 2024. All rights reserved.</p>
        <p>Contact us: yadavshivamp90671@gmail.com</p>
    </div>
"""

st.markdown(footer_html, unsafe_allow_html=True)



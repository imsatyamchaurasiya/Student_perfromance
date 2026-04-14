import pickle
import numpy as np
import streamlit as st
import warnings
warnings.filterwarnings("ignore")
import pandas as pd

# for background color
st.markdown("""
<style>
.stApp {
    background-color: #dbeafe;  /* Light Blue */
}
</style>
""", unsafe_allow_html=True)

# For sidebar background color
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #1e1e2f;
}
</style>
""", unsafe_allow_html=True)
st.title("Student Marks Prediction and Analysis")


# Load the dataset
df = pd.read_csv("student_dataset_advanced.csv")
st.subheader("Student performance analysis")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students",df['Student_ID'].count())
col2.metric("Total Passed", df[df['Final_Score']>=33].shape[0]) 
col3.metric("Total Failed", df[df['Final_Score']<33].shape[0])
col4.metric("Average Score", round(df['Final_Score'].mean(), 2))
# Filter the dataset in categorical section with the help of selectbox
st.subheader("Filter students based on categorical features")

# Search Students name
st.subheader("Search Student by Name")
search = st.text_input("Search Student Name")
df = df[df["Name"].str.contains(search, case=False)]

# Marks Select and you can select the marks and it will show the students who got that marks
marks = st.slider("Select Marks Range", 0, 100, (0, 100))
df = df[(df['Final_Score'] >= marks[0]) & (df['Final_Score'] <= marks[1])]





# Parental level of education
st.subheader("Parental Level of Education")
education_level=st.selectbox("Select Parental Education Level",df['Parental_Education'].unique())
filtered_education_df=df[df['Parental_Education']==education_level]
st.write("Filtered Data",filtered_education_df)

# Section wise filter
st.sidebar.title("Filters")
Section = st.sidebar.selectbox("Select Section", df["Section"].unique())
filtered_section_df = df[df["Section"] == Section]

# Grade wise filter
st.subheader("Grade Wise Filter")
grade=st.selectbox("Select Grade",df['Grade'].unique())
filtered_grade_df=df[df['Grade']==grade]
st.write("Filtered Data",filtered_grade_df)



# Some rough analysis of the dataset
student_name = st.selectbox("Select Student", df["Name"].unique())

# Showing Scorecard
if st.button("View Scorecard"):
    st.session_state["student"] = student_name
    st.session_state["page"] = "scorecard"
    st.rerun()

if st.session_state.get("page") == "scorecard":
    import pages.Scorecard
    
# Deploying the model for predicting score
st.title("Student marks prediction")
Sleep_Hours = st.number_input("Enter Sleep Hours", min_value=0, max_value=24, value=7)
Study_Hours = st.number_input("Enter Study Hours", min_value=0, max_value=24, value=2)
Attendence = st.number_input("Enter Attendance Percentage", min_value=0, max_value=100, value=90)
btn=st.button("Predict Marks")
if btn:
    Rf = pickle.load(open("spd.pkl", "rb"))
    result = Rf.predict([[Sleep_Hours, Study_Hours, Attendence]])
    st.success(f"Your predicted marks are {result[0]}")

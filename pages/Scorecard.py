import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

# Page config
st.set_page_config(page_title="Student Scorecard", layout="wide")

# Load dataset
df = pd.read_csv("student_dataset_advanced.csv")

# Get selected student from session
student_name = st.session_state.get("student")

# If no student selected
if student_name is None:
    st.warning("⚠️ Please select a student from main page")
    st.stop()

# Get student data
student = df[df["Name"] == student_name].iloc[0]

# 🎨 Background color (blue theme)
st.markdown("""
<style>
.stApp {
    background-color: #e0f2fe;
}
</style>
""", unsafe_allow_html=True)

# 🎓 Title
st.title("📊 Student Scorecard")

# 👤 Student Info
st.subheader(f"👤 {student['Name']}")
st.write("Section:", student["Section"])
st.write("Parental Education:", student["Parental_Education"])

st.divider()

# 📊 KPI Cards
col1, col2, col3 = st.columns(3)

col1.metric("Final Score", student["Final_Score"])
col2.metric("Result", student["Result"])
col3.metric("Grade", student["Grade"])

st.divider()

# 📚 Subject Marks
st.subheader("📚 Subject Marks")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Math", student["Math_Marks"])
col2.metric("Science", student["Science_Marks"])
col3.metric("English", student["English_Marks"])
col4.metric("Hindi", student["Hindi_Marks"])
col5.metric("SST", student["SST_Marks"])

st.divider()

# 📈 Chart
marks_data = {
    "Subject": ["Math", "Science", "English", "Hindi", "SST"],
    "Marks": [
        student["Math_Marks"],
        student["Science_Marks"],
        student["English_Marks"],
        student["Hindi_Marks"],
        student["SST_Marks"]
    ]
}

fig = px.bar(marks_data, x="Subject", y="Marks", title="Subject-wise Marks")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# 🧠 Extra Info
st.subheader("📊 Additional Info")

col1, col2, col3 = st.columns(3)

col1.write(f"📖 Study Hours: {student['Study_Hours_per_Day']}")
col2.write(f"😴 Sleep Hours: {student['Sleep_Hours']}")
col3.write(f"📅 Attendance: {student['Attendance_Percentage']}")

# 🎯 Result Highlight
if student["Result"] == "Pass":
    st.success("🎉 Student Passed Successfully")
else:
    st.error("❌ Student Failed - Needs Improvement")

# 🔙 Back button
if st.button("⬅️ Back to Dashboard"):
    st.switch_page("stmp.py")

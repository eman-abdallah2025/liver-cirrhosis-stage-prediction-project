
import streamlit as st
import sqlite3
import re
from reportlab.lib.utils import ImageReader
import pandas as pd
from fpdf import FPDF
import pdfkit
import joblib
import datetime
import numpy as np
from reportlab.lib.utils import simpleSplit
import markdown2
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import cv2
import tensorflow as tf
from tensorflow.keras.utils import img_to_array

#st.set_page_config(page_title="Healthcare System", layout="wide")
st.set_page_config(page_title="Hospmind Clinics", page_icon="🏥", layout="wide")

 # Sidebar contents
with st.sidebar:
    st.image("hos.png", width=150)
    st.title("HOSPMIND")

    st.markdown("### Departments")
    if st.button("Home"):
        st.success("You opened Home Page!")

    if st.button("Cardiology "):
        st.success("You opened Cardiology Page!")

    if st.button("Neurology "):
       st.success("You opened Neurology Page!")
    if st.button("Pulmonology"):
        st.success("You opened Pulmonology Page!")
    if st.button("Hepatology "):
       st.success("You opened Hepatology Page!")
report_txt =None
table = "hepatology_patients"
result =None
# Connect to the database
conn = sqlite3.connect("liver.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS hepatology_patients (
        national_id TEXT PRIMARY KEY,
        name TEXT,
        mobile TEXT,
        gender TEXT,
        age INTEGER,
        department TEXT,

        report_pdf TEXT,
        report_date TEXT
    )
""")
conn.commit()



 # Streamlit page
col1,col2 =st.columns([1,9])
with col1:
  st.image("hos.png")
with col2:
  st.title("Liver Cirrhosis Stage Prediction")

# Load the model, scaler, and label encoder

def load_model_and_scaler():
    model = joblib.load("Gradient Boosting_model.pkl")
    scaler = joblib.load("scaler.pkl")
    label_encoder = joblib.load("label_encoder.pkl")
    return model, scaler, label_encoder

model, scaler, label_encoder = load_model_and_scaler()


def liver_report(first_name, last_name, national_id, mobile, gender, stage_label):

        report_text = "## Comprehensive AI Medical Report\n\n"

        # Patient Information
        report_text += f"####  Patient Information\n"
        report_text += f"- *Name:* {first_name} {last_name if last_name else ''}\n"
        report_text += f"- *National ID:* {national_id}\n"
        report_text += f"- *Mobile:* {mobile if mobile else 'Not Provided'}\n"
        report_text += f"- *Gender:* {gender if gender else 'Not Specified'}\n\n"
        report_text += "---\n"
          #  Symptoms
        report_text += "### Symptoms\n\n"
        if symptoms:
            report_text += ",".join(symptoms)
            report_text += "\n\n"
        else:
            report_text += "No significant symptoms\n\n"
        report_text += "### 🔍 Classification\n"
        report_text += f"The Chest X ray was classified into the *{prediction}* category."


        report_text += "---\n"


        # Prediction Section
        report_text +="🔍 Prediction Result\n"
        report_text +="The model predicts the **stage of cirrhosis** based on the inputs provided.\n"
        stage_label = str(stage_label)

        if stage_label.lower() in ["no", "no cirrhosis"]:
          report_text +="🟢 No Cirrhosis Detected\n"
          report_text += "**What This Means:**\n"
          report_text +="- The model predicts that the patient's liver is **healthy**.\n"
          report_text +="- However, regular medical check-ups are recommended.\n"

        elif stage_label.lower() in ["early"]:
           report_text +="🟡 Early-stage Cirrhosis Detected\n"
           report_text +="**What This Means:**\n"
           report_text +="- The patient may have **early liver scarring**.\n"
           report_text +="- **Lifestyle changes & medical intervention** can help slow down progression.\n"

        else:
          report_text +="🔴 Advanced Cirrhosis Detected\n"
          report_text += "**What This Means:**\n"
          report_text +="- The liver shows significant **damage and scarring**.\n"
          report_text +="- Immediate medical attention is advised.\n"


         # Disclaimer
        report_text += "---\n"
        report_text += "### 🔍 Additional Notes\n"
        report_text += "This report provides an *initial assessment* based on the patient's input data and does not constitute a final diagnosis. A specialist consultation is recommended for a thorough medical evaluation.\n"


        return report_text
def convert_markdown_to_pdf(report_markdown, national_id):
        os.makedirs("reports", exist_ok=True)  # Ensure the reports directory exists
        output_path = os.path.join("reports", f"liver_report_{national_id}.pdf")

        # Create a new PDF file with A4 size
        c = canvas.Canvas(output_path, pagesize=letter)
        c.setFont("Helvetica", 12)
        y_position = 750

        # Regex patterns for markdown formatting
        image_pattern = re.compile(r"!(.*?)(.*?)")
        bold_pattern = re.compile(r"\*\*(.*?)\*\*")
        italic_pattern = re.compile(r"\*(.*?)\*")
        bold_italic_pattern = re.compile(r"\*\*\*(.*?)\*\*\*")

        for line in report_markdown.split("\n"):
            image_match = image_pattern.search(line)
            if image_match:
                image_path = image_match.group(2)
                try:
                    img = ImageReader(image_path)
                    c.drawImage(img, 100, y_position - 100, width=100, height=100)
                    y_position -= 120
                except Exception as e:
                    print(f"⚠ Error loading image: {e}")

            elif line.startswith("# "):
                c.setFont("Helvetica-Bold", 16)
                c.drawString(100, y_position, line.replace("# ", ""))
            elif line.startswith("## "):
                c.setFont("Helvetica-Bold", 14)
                c.drawString(100, y_position, line.replace("## ", ""))
            elif line.startswith("### "):
                c.setFont("Helvetica-Bold", 12)
                c.drawString(100, y_position, line.replace("### ", ""))
            elif line.startswith("#### "):
                c.setFont("Helvetica-Bold", 10)
                c.drawString(100, y_position, line.replace("#### ", ""))
            else:
                # Apply markdown styles
                line = bold_italic_pattern.sub(r"\1", line)  # Apply bold italic
                line = bold_pattern.sub(r"\1", line)  # Apply bold
                line = italic_pattern.sub(r"\1", line)  # Apply italic

                c.setFont("Helvetica", 12)
                c.drawString(100, y_position, line)

            y_position -= 20

        c.save()
        return output_path

  # Apply Dark Theme using custom CSS
dark_theme_css = """
  <style>
    body, .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }

    section[data-testid="stSidebar"] {
        background-color: #161a24;
    }

    h1, h2, h3, h4 {
        color: #ffffff;
    }

    .stTextInput > div > div > input,
    .stNumberInput input,
    .stSelectbox > div > div,
    .stButton button {
        background-color: #21262d;
        color: #ffffff;
        border: 1px solid #30363d;
    }

    .stButton button {
        background-color: #238636;
        color: white;
        border-radius: 0.4rem;
    }

    .stButton button:hover {
        background-color: #2ea043;
        color: white;
    }

    a {
        color: #58a6ff;
    }

    .stSuccess {
        background-color: #1d2b1f;
        color: #a3f7bf;
    }
  </style>
    """
st.markdown(dark_theme_css, unsafe_allow_html=True)
st.title("Personel information")
col3, col4 = st.columns(2)

with col3:

        first_name = st.text_input("First Name (required)", key="first_name")
        last_name = st.text_input("Last Name (required)", key="last_name")
        national_id = st.text_input("National ID (required)", key="patient-national_id")
with col4:
        mobile = st.text_input("Mobile Number (optional)", key='mobile')
        gender = st.selectbox("Gender (optional)", ["Male", "Female"], key='gender')
        age = st.number_input("Age (optional)", min_value=0, step=1, key='age')
patient_name = first_name + " " + last_name
save_patient = st.button("Save Patient", key="save_patient")
if save_patient:
        if national_id and patient_name :
            st.write(national_id)
            cursor.execute("""
            INSERT OR REPLACE INTO hepatology_patients
            (national_id, name, mobile, gender, age,department, report_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (national_id, patient_name, mobile, gender, age, "hepatology",
              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            st.success(f"Saved {patient_name} information Successfully!")
        else:
            st.warning("Please complete patient personal information")
# User Input Section
st.header("📝 Enter Patient Details")

hepatomegaly_input = st.selectbox("Hepatomegaly (Liver Enlargement)", ["No", "Yes"])
edema_input = st.selectbox("Edema (Swelling)", ["No", "Yes", "Severe"])
bilirubin = st.number_input("Bilirubin Level (mg/dL)", min_value=0.0, max_value=50.0, value=1.0)
albumin = st.number_input("Albumin Level (g/dL)", min_value=0.0, max_value=10.0, value=4.0)
platelets = st.number_input("Platelets Count (x10^3/uL)", min_value=0.0, max_value=1000.0, value=250.0)
prothrombin = st.number_input("Prothrombin Time (sec)", min_value=0.0, max_value=20.0, value=10.0)
N_Years = st.number_input("Years of Follow-up", min_value=0.0, max_value=50.0, value=1.0)


  # Convert categorical inputs to numeric
hepatomegaly = 1 if hepatomegaly_input == "Yes" else 0
edema = {"No": 0, "Yes": 1, "Severe": 2}[edema_input]

  # Symptoms selection
symptoms = st.multiselect("Select Symptoms",
                               [ "Jaundice (yellowing of the skin and eyes)",
                                  "Abdominal pain (especially in the upper right side)",
                                 "Swelling in the abdomen (ascites)",
                                 "Fatigue",
                                 "Nausea",
                                 "Vomiting",
                                 "Loss of appetite",
                                 "Dark urine",
                                 "Pale or clay-colored stool",
                                 "Itchy skin",
                                 "Unexplained weight loss",
                                 "Bruising easily",
                                 "Confusion or memory problems (hepatic encephalopathy)",
                                 "Swelling in the legs and ankles",
                                 "Fever (in case of infection or inflammation)"
                                     ])

  # Prediction Section
input_data = pd.DataFrame([[hepatomegaly, edema, bilirubin, albumin, platelets, prothrombin, N_Years]],
                               columns=["Hepatomegaly", "Edema", "Bilirubin", "Albumin", "Platelets", "Prothrombin", "N_Years"])

scaled_input = scaler.transform(input_data)
prediction = model.predict(scaled_input)[0]
stage_label = label_encoder.inverse_transform([prediction])[0]
report_txt = liver_report(first_name, last_name, national_id, mobile, gender, stage_label)

col5,col6 =st.columns(2)
with col5:
   if st.button("Predict", key="predict_btn"):

    #show the report in markdown
    st.header( "🔍 Prediction Result")
    st.markdown("The model predicts the **stage of cirrhosis** based on the inputs provided.",unsafe_allow_html= True)
    report_txt =f"<div style = 'color : white;'>{report_txt}</div>"
    st.markdown(report_txt, unsafe_allow_html=True)




    st.markdown("\n🔢 **Patient Data Entered:**")
    st.dataframe(input_data.style.set_properties(**{"background-color": "#1E1E1E", "color": "#FFFFFF"}))
with col6:
     # Button to save Chest X ray report
      save_report = st.button("Save AI Report", key="save_report")
      if save_report:
         if national_id  and patient_name and report_txt  :

                report_file = convert_markdown_to_pdf(report_txt, national_id)

                # insert patient information and ECG REport in Cardiology table
                cursor.execute("""
                           INSERT OR REPLACE INTO hepatology_patients
                           (national_id, name, mobile, gender, age,department,report_pdf, report_date)
                            VALUES (?, ?, ?, ?, ?, ?, ?,?)
                            """, (national_id, patient_name, mobile, gender, age, "hepatology",report_file,
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

                conn.commit()
                st.success(f" Report saved successfuly at :{report_file}")

         else:
                  st.warning("please complete required data")

st.markdown('<h2 >🔍 Search for a Patien</h2>', unsafe_allow_html=True)

search_id = st.text_input("Enter Patient ID to Retrieve Data",key ="search_id")

liver_search = st.button("download AI Report", key="liver_search")
if liver_search:
    if search_id:

     cursor.execute(f"SELECT report_pdf FROM {table} WHERE national_id=?", (search_id,))
     result = cursor.fetchone()
     st.write("Debug: result =", result[0])
     st.write("Debug: path =",  os.path.exists(result[0]))
     if result is not None and os.path.exists(result[0]) is True :
            with open(result[0], "rb") as file:
                st.download_button(label="📄 Download Report", data=file,file_name=f"liver_report_{search_id}.pdf", mime="application/pdf")

     else :
        st.warning("No patient found fot this ID")
    else:
        st.warning("Please enter PatientID")

 # Button for deleting patient
if st.button("🗑 Delete Patient"):
    if search_id:

      cursor.execute(f"SELECT report_pdf FROM {table} WHERE national_id=?", (search_id,))
      result = cursor.fetchone()
      st.write("Debug: result =", result[0])

      if result is not None:
          liver_path = result[0]

          if os.path.exists(liver_path) is pd.notnull and result is not None:
                # Delete the PDF file
                os.remove(liver_path)

                # Delete patient from database
                cursor.execute(f"DELETE FROM {table} WHERE national_id=?", (search_id,))
                conn.commit()
                st.success("✅ Patient record deleted successfully!")
      else:
         st.error("❌ No patient found!")
    else:
            st.warning("Please enter PatientID")

# Add buttons to return to Clinics or Main
st.markdown("---")
col9, col10 ,col11= st.columns(3)
with col11:
    if st.button(" 🏠 Go to home"):
        st.success("You opened  Home Page!")















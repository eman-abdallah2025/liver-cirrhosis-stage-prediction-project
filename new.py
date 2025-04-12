
import streamlit as st
import pandas as pd
import numpy as np
import joblib  # تم استبدال pickle بـ joblib

# Streamlit page config
st.set_page_config(page_title="Liver Cirrhosis Prediction", page_icon="🩺", layout="wide")
st.title("🩺 Liver Cirrhosis Stage Prediction")

# Load the model, scaler, and label encoder
@st.cache_resource
def load_model_and_scaler():
    model = joblib.load("models/Gradient Boosting_model.pkl")
    scaler = joblib.load("models/scaler.pkl")
    label_encoder = joblib.load("models/label_encoder.pkl")
    return model, scaler, label_encoder

model, scaler, label_encoder = load_model_and_scaler()

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

# Prediction Section
st.subheader("🔍 Prediction Result")
st.markdown("The model predicts the **stage of cirrhosis** based on the inputs provided.")

if st.button("Predict", key="predict_btn"):
    input_data = pd.DataFrame([[hepatomegaly, edema, bilirubin, albumin, platelets, prothrombin, N_Years]],
                               columns=["Hepatomegaly", "Edema", "Bilirubin", "Albumin", "Platelets", "Prothrombin", "N_Years"])
    
    scaled_input = scaler.transform(input_data)
    prediction = model.predict(scaled_input)[0]
    stage_label = label_encoder.inverse_transform([prediction])[0]

    if stage_label.lower() in ["no", "no cirrhosis"]:
        st.success("🟢 No Cirrhosis Detected")
        st.markdown("""
        **What This Means:**
        - The model predicts that the patient's liver is **healthy**.
        - However, regular medical check-ups are recommended.
        """)
    elif "early" in stage_label.lower():
        st.warning("🟡 Early-stage Cirrhosis Detected")
        st.markdown("""
        **What This Means:**
        - The patient may have **early liver scarring**.
        - **Lifestyle changes & medical intervention** can help slow down progression.
        """)
    else:
        st.error("🔴 Advanced Cirrhosis Detected")
        st.markdown("""
        **What This Means:**
        - The liver shows significant **damage and scarring**.
        - Immediate medical attention is advised.
        """)

    st.markdown("\n🔢 **Patient Data Entered:**")
    st.dataframe(input_data.style.set_properties(**{"background-color": "#1E1E1E", "color": "#FFFFFF"}))

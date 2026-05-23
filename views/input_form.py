import streamlit as st
import pandas as pd

st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <h2 style="font-size: 36px; margin-bottom: 8px; color: var(--text-main) !important;">📋 Student Profile Setup</h2>
    <p style="color: var(--text-muted); font-size: 16px;">Load a pre-configured template or orchestrate your parameters manually below.</p>
</div>
""", unsafe_allow_html=True)

MOCK_PROFILES = {
    "Custom Profile (Use Interface Controls)": None,
    "Alex Rivera (High Risk of Attrition)": {
        'gpa': 1.6, 'attendance': 0.58, 'engagement': 0.32, 'income_proxy': 18000,
        'low_gpa_flag': 1, 'low_engagement_flag': 1, 'risk_score': 0.82,
        'Unemployment rate': 8.5, 'Age at enrollment': 23, 'Gender': 1
    },
    "Chloe Chen (Stellar Academic Standing)": {
        'gpa': 3.9, 'attendance': 0.98, 'engagement': 0.95, 'income_proxy': 65000,
        'low_gpa_flag': 0, 'low_engagement_flag': 0, 'risk_score': 0.08,
        'Unemployment rate': 4.2, 'Age at enrollment': 18, 'Gender': 0
    },
    "Jordan Smith (Borderline Warning)": {
        'gpa': 2.3, 'attendance': 0.76, 'engagement': 0.55, 'income_proxy': 32000,
        'low_gpa_flag': 0, 'low_engagement_flag': 0, 'risk_score': 0.48,
        'Unemployment rate': 5.8, 'Age at enrollment': 21, 'Gender': 1
    }
}

selected_preset = st.selectbox(
    "👤 Load a Pre-configured Student Profile for Quick Demo:",
    options=list(MOCK_PROFILES.keys())
)

preset_values = MOCK_PROFILES[selected_preset]
def get_val(key, default):
    if preset_values is not None and key in preset_values:
        return preset_values[key]
    return default

# Elegant Main Screen Grid Layout
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("### 📊 Academic Records")
    gpa = st.number_input('Current GPA', min_value=0.0, max_value=4.0, value=float(get_val('gpa', 3.0)), step=0.01, help="The student's overall grade point average out of 4.0")
    attendance = st.slider('Attendance Percentage', min_value=0.0, max_value=1.0, value=float(get_val('attendance', 0.85)), format="%.0f%%", help="What percentage of classes has the student attended so far?")

with col2:
    st.markdown("### 💻 Engagement Triggers")
    engagement_val = float(get_val('engagement', 0.55))
    default_eng_idx = 0 if engagement_val >= 0.8 else (1 if engagement_val >= 0.5 else (2 if engagement_val >= 0.25 else 3))
    
    engagement_desc = st.selectbox(
        'Online Course Activity',
        options=[
            "Very Active (Daily logins, completes quizzes)",
            "Moderately Active (Logs in weekly)",
            "Rarely Active (Logs in infrequently)",
            "Inactive (Hardly ever logs in)"
         ], index=default_eng_idx,
         help="How often does the student log into the online portal, view materials, or submit assignments?"
    )
    engagement = 0.85 if "Very Active" in engagement_desc else (0.55 if "Moderately Active" in engagement_desc else (0.28 if "Rarely Active" in engagement_desc else 0.12))
    risk_score = st.slider("Counselor's Initial Concern", min_value=0.0, max_value=1.0, value=float(get_val('risk_score', 0.30)), help="Your personal gut-feeling or initial assessment of the student's risk level before running the AI")

with col3:
    st.markdown("### 👥 Demographic Metrics")
    income_proxy = st.number_input('Estimated Family Income ($)', min_value=0, max_value=500000, value=int(get_val('income_proxy', 40000)))
    unemployment_rate = st.number_input('Local Unemployment Rate (%)', min_value=0.0, max_value=100.0, value=float(get_val('Unemployment rate', 5.0)), help="The unemployment rate in the student's home city/region")
    age = st.number_input('Starting Age', min_value=15, max_value=90, value=int(get_val('Age at enrollment', 20)))
    gender = st.selectbox('Student Gender', options=[0, 1], index=int(get_val('Gender', 0)), format_func=lambda x: "Male" if x == 1 else "Female")

st.markdown("<br/>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    if st.button("🚀 Execute Predictive Analytics", type="primary", use_container_width=True):
        st.session_state.selected_preset_name = selected_preset
        st.session_state.student_data = {
            'gpa': gpa, 'attendance': attendance, 'engagement': engagement, 'income_proxy': income_proxy,
            'low_gpa_flag': 1 if gpa < 2.0 else 0, 'low_engagement_flag': 1 if engagement < 0.4 else 0,
            'risk_score': risk_score, 'Unemployment rate': unemployment_rate, 'Age at enrollment': age, 'Gender': gender
        }
        st.switch_page("views/dashboard.py")

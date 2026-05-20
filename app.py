import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pickle
import os
import shap
import lime
import lime.lime_tabular
import matplotlib.pyplot as plt

# Global Feature Display Names for XAI
feature_display_names = {
    'gpa': 'Cumulative GPA',
    'attendance': 'Attendance Rate',
    'engagement': 'VLE Engagement Score',
    'income_proxy': 'Household Income',
    'low_gpa_flag': 'Low GPA Alert Flag',
    'low_engagement_flag': 'Low Engagement Alert Flag',
    'risk_score': 'Institutional Risk Index',
    'Unemployment rate': 'Regional Unemployment',
    'Age at enrollment': 'Age at Enrollment',
    'Gender': 'Gender Code'
}

# ----------------------------------------------------
# Page Configuration & Styling
# ----------------------------------------------------
st.set_page_config(
    page_title="EduSafe AI - Student Success Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium UI Theme using Vanilla CSS
st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    h1, h2, h3, .title-text {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: var(--text-color);
    }

    /* Background and Layout */
    .main {
        background-color: var(--background-color);
    }
    
    /* Premium Cards adapting dynamically to Dark/Light themes */
    .premium-card {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 24px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.15);
    }
    
    /* Custom Badges */
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-danger {
        background-color: rgba(239, 68, 68, 0.15);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
    
    .badge-warning {
        background-color: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    
    .badge-success {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    /* Metric Layouts */
    .metric-value {
        font-size: 36px;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .metric-label {
        font-size: 14px;
        font-weight: 600;
        color: var(--text-color);
        opacity: 0.7;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Custom Linear Risk Bar */
    .risk-bar-container {
        width: 100%;
        background-color: rgba(128, 128, 128, 0.2);
        border-radius: 9999px;
        height: 12px;
        margin: 12px 0;
        overflow: hidden;
    }
    
    .risk-bar-fill {
        height: 100%;
        border-radius: 9999px;
        transition: width 0.6s ease-in-out;
    }
    
    /* Recommendation Cards */
    .rec-card {
        border-left: 5px solid #3B82F6;
        background-color: rgba(59, 130, 246, 0.1);
        color: var(--text-color);
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    
    .rec-card.high-priority {
        border-left-color: #EF4444;
        background-color: rgba(239, 68, 68, 0.1);
    }
    
    .rec-card.medium-priority {
        border-left-color: #F59E0B;
        background-color: rgba(245, 158, 11, 0.1);
    }

    /* Custom Tooltips & Descriptions */
    .info-text {
        font-size: 13px;
        color: var(--text-color);
        opacity: 0.75;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# Data & Model Loaders
# ----------------------------------------------------
@st.cache_resource
def load_models():
    models = {}
    models_dir = 'models'
    
    # Best Model (often Random Forest or XGBoost)
    try:
        models['best'] = joblib.load(os.path.join(models_dir, 'best_model.pkl'))
    except Exception:
        try:
            with open(os.path.join(models_dir, 'best_model.pkl'), 'rb') as f:
                models['best'] = pickle.load(f)
        except Exception:
            st.error("⚠️ Failed to load Best Model.")

    # Random Forest Model
    try:
        models['rf'] = joblib.load(os.path.join(models_dir, 'random_forest_model.pkl'))
    except Exception:
        st.error("⚠️ Failed to load Random Forest Model.")

    # XGBoost Model
    try:
        models['xgboost'] = joblib.load(os.path.join(models_dir, 'xgboost_model.pkl'))
    except Exception:
        try:
            with open(os.path.join(models_dir, 'xgboost_model.pkl'), 'rb') as f:
                models['xgboost'] = pickle.load(f)
        except Exception:
            st.error("⚠️ Failed to load XGBoost Model.")

    # Scaler
    try:
        models['scaler'] = joblib.load(os.path.join(models_dir, 'scaler.pkl'))
    except Exception:
        st.error("⚠️ Failed to load Scaler.")
        
    return models

models = load_models()

FEATURES = ['gpa', 'attendance', 'engagement', 'income_proxy', 'low_gpa_flag', 
            'low_engagement_flag', 'risk_score', 'Unemployment rate', 
            'Age at enrollment', 'Gender']

# Predefined Mock Student Profiles for quick-select demonstration
MOCK_PROFILES = {
    "Custom Profile (Use Sidebar Sliders)": None,
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

# ----------------------------------------------------
# Main Dashboard Header
# ----------------------------------------------------
st.markdown("""
<div style='display: flex; align-items: center; gap: 16px; margin-bottom: 24px;'>
    <div style='background-color: #3B82F6; padding: 12px; border-radius: 12px; color: white;'>
        <h2 style='margin: 0; font-size: 32px;'>🎓</h2>
    </div>
    <div>
        <h1 style='margin: 0; font-size: 28px; color: #1E293B;'>EduSafe AI™ — Student Success Portal</h1>
        <p style='margin: 0; color: #64748B; font-size: 14px;'>Predictive early warning & explainable intervention system</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Profile Quick Selector & Sidebar Configuration
# ----------------------------------------------------
col_selector, col_spacer = st.columns([2, 2])
with col_selector:
    selected_preset = st.selectbox(
        "👤 Load a Pre-configured Student Profile for Quick Demo:",
        options=list(MOCK_PROFILES.keys())
    )

st.sidebar.markdown("### 📝 Profile Configuration")
preset_values = MOCK_PROFILES[selected_preset]

# Initialize values with preset or default values
def get_val(key, default):
    if preset_values is not None and key in preset_values:
        return preset_values[key]
    return default

# Sliders and selectors grouped in premium collapsible expanders
with st.sidebar.expander("📈 Academic Performance", expanded=True):
    gpa = st.number_input(
        'Cumulative GPA (0.00 - 4.00)',
        min_value=0.0,
        max_value=4.0,
        value=float(get_val('gpa', 3.0)),
        step=0.01,
        format="%.2f",
        help="Type or select the student's cumulative grade point average."
    )
    
    attendance = st.slider(
        'Class Attendance Rate',
        min_value=0.0,
        max_value=1.0,
        value=float(get_val('attendance', 0.85)),
        step=0.01,
        format="%.0f%%",
        help="Percentage of scheduled lectures, labs, and tutorials attended."
    )

with st.sidebar.expander("💻 Institutional Engagement", expanded=True):
    # Map engagement float to descriptive category for the preset loader
    engagement_val = float(get_val('engagement', 0.70))
    if engagement_val >= 0.8:
        default_eng_index = 0
    elif engagement_val >= 0.5:
        default_eng_index = 1
    elif engagement_val >= 0.3:
        default_eng_index = 2
    else:
        default_eng_index = 3
        
    engagement_desc = st.selectbox(
        'VLE Digital Engagement Level',
        options=[
            "High Engagement (Active Daily & Quizzes) [0.85]",
            "Medium Engagement (Regular Weekly Logs) [0.55]",
            "Low Engagement (Infrequent Activity) [0.28]",
            "Critical Neglect (Rarely Logs In) [0.12]"
         ],
        index=default_eng_index,
        help="Recorded interaction level with the Virtual Learning Environment."
    )
    
    # Parse qualitative engagement back to decimal for the model
    if "High" in engagement_desc:
        engagement = 0.85
    elif "Medium" in engagement_desc:
        engagement = 0.55
    elif "Low" in engagement_desc:
        engagement = 0.28
    else:
        engagement = 0.12

    risk_score = st.slider(
        'Internal Advisor Risk Score',
        min_value=0.0,
        max_value=1.0,
        value=float(get_val('risk_score', 0.30)),
        step=0.01,
        help="Subjective risk score assigned during advisor check-ins."
    )

with st.sidebar.expander("👥 Demographic & Socio-Economic", expanded=False):
    income_proxy = st.number_input(
        'Household Income Proxy ($)',
        min_value=0,
        max_value=500000,
        value=int(get_val('income_proxy', 40000)),
        step=1000,
        format="%d",
        help="Estimated family household income proxy metric."
    )
    
    unemployment_rate = st.number_input(
        'Regional Unemployment Rate (%)',
        min_value=0.0,
        max_value=100.0,
        value=float(get_val('Unemployment rate', 5.0)),
        step=0.1,
        format="%.1f",
        help="Current unemployment rate in the student's home district."
    )
    
    age = st.number_input(
        'Age at Enrollment',
        min_value=15,
        max_value=90,
        value=int(get_val('Age at enrollment', 20)),
        step=1,
        help="Age of the student when they matriculated into the program."
    )
    
    gender = st.selectbox(
        'Gender Identity Code',
        options=[0, 1],
        index=int(get_val('Gender', 0)),
        format_func=lambda x: "Male" if x == 1 else "Female",
        help="Gender code matched with model training definition."
    )

# Flags automatically computed
low_gpa_flag = 1 if gpa < 2.0 else 0
low_engagement_flag = 1 if engagement < 0.4 else 0

# Assemble input DataFrame
input_data = {
    'gpa': gpa,
    'attendance': attendance,
    'engagement': engagement,
    'income_proxy': income_proxy,
    'low_gpa_flag': low_gpa_flag,
    'low_engagement_flag': low_engagement_flag,
    'risk_score': risk_score,
    'Unemployment rate': unemployment_rate,
    'Age at enrollment': age,
    'Gender': gender
}
input_df = pd.DataFrame(input_data, index=[0])

# Preprocess using the Scaler
if 'scaler' in models:
    input_scaled = pd.DataFrame(models['scaler'].transform(input_df), columns=FEATURES)
else:
    input_scaled = input_df

# ----------------------------------------------------
# Predictions Core
# ----------------------------------------------------
preds = {}
for name, model_key in [("Best Ensemble Model", "best"), ("Random Forest Classifier", "rf"), ("XGBoost Predictor", "xgboost")]:
    if model_key in models:
        try:
            proba = models[model_key].predict_proba(input_scaled)[0][1]
            preds[name] = proba
        except Exception:
            preds[name] = 0.5 # fallback

# Select active model for explanation
st.sidebar.markdown("### ⚙️ Analysis Parameters")
selected_explain_model_name = st.sidebar.radio("Active Explanation Model:", list(preds.keys()))
model_mapping = {
    "Best Ensemble Model": "best",
    "Random Forest Classifier": "rf",
    "XGBoost Predictor": "xgboost"
}
active_model_key = model_mapping[selected_explain_model_name]
active_model = models[active_model_key]
active_proba = preds[selected_explain_model_name]

# ----------------------------------------------------
# Row 1: High Level Student Scoreboard
# ----------------------------------------------------
c1, c2, c3 = st.columns([1.5, 2, 1.5])

with c1:
    st.markdown(f"""<div class="premium-card">
<div class="metric-label">Student Profile Summary</div>
<div style='margin-top: 12px;'>
<div style='font-size: 20px; font-weight: 700; color: var(--text-color);'>{selected_preset.split(" (")[0]}</div>
<div style='color: var(--text-color); opacity: 0.7; font-size: 13px;'>Age: {age} | Gender: {"Male" if gender == 1 else "Female"}</div>
<hr style='border: 0; border-top: 1px solid rgba(128, 128, 128, 0.2); margin: 12px 0;'/>
<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 8px;'>
<div><span style='color: var(--text-color); opacity: 0.7; font-size: 11px;'>GPA</span><br/><strong style='color: var(--text-color);'>{gpa:.2f}</strong></div>
<div><span style='color: var(--text-color); opacity: 0.7; font-size: 11px;'>ATTENDANCE</span><br/><strong style='color: var(--text-color);'>{attendance:.1%}</strong></div>
<div><span style='color: var(--text-color); opacity: 0.7; font-size: 11px;'>ENGAGEMENT</span><br/><strong style='color: var(--text-color);'>{engagement:.1%}</strong></div>
<div><span style='color: var(--text-color); opacity: 0.7; font-size: 11px;'>HOUSEHOLD INC.</span><br/><strong style='color: var(--text-color);'>${income_proxy:,}</strong></div>
</div>
</div>
</div>""", unsafe_allow_html=True)

with c2:
    if active_proba > 0.65:
        badge_html = '<span class="badge badge-danger">⚠️ Critical At-Risk</span>'
        bar_color = '#EF4444'
    elif active_proba > 0.35:
        badge_html = '<span class="badge badge-warning">⚡ Moderate Concern</span>'
        bar_color = '#F59E0B'
    else:
        badge_html = '<span class="badge badge-success">✅ Stable / Successful</span>'
        bar_color = '#10B981'
        
    st.markdown(f"""<div class="premium-card">
<div class="metric-label">Predictive Dropout Risk Score</div>
<div style='display: flex; justify-content: space-between; align-items: baseline; margin-top: 8px;'>
<div class="metric-value" style='color: {bar_color};'>{active_proba:.1%}</div>
<div>{badge_html}</div>
</div>
<div class="risk-bar-container">
<div class="risk-bar-fill" style="width: {active_proba*100}%; background-color: {bar_color};"></div>
</div>
<div class="info-text">
This is the estimated likelihood of student attrition. This score is generated in real-time by the selected <strong>{selected_explain_model_name}</strong>.
</div>
</div>""", unsafe_allow_html=True)

with c3:
    comp_html = f"""<div class="premium-card">
<div class="metric-label">Cross-Model Comparison</div>
<div style='margin-top: 12px;'>"""
    
    for name, p_val in preds.items():
        sub_color = '#10B981' if p_val < 0.35 else ('#F59E0B' if p_val < 0.65 else '#EF4444')
        bold_style = "font-weight: 700;" if name == selected_explain_model_name else ""
        bg_highlight = "background-color: rgba(128, 128, 128, 0.1); border-radius: 6px; padding: 4px 8px;" if name == selected_explain_model_name else ""
        comp_html += f"""
<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; {bg_highlight}'>
<span style='font-size: 12px; color: var(--text-color); {bold_style}'>{name.split(" ")[0]} Model</span>
<span style='font-size: 13px; font-weight: 600; color: {sub_color};'>{p_val:.1%}</span>
</div>"""
        
    comp_html += """
</div>
</div>"""
    st.markdown(comp_html, unsafe_allow_html=True)

# # ----------------------------------------------------
# Row 2: Unifed Live XAI & Advisory Engine
# ----------------------------------------------------
st.markdown("### 🔍 Live Decision Driver & Intervention Engine")

# Active XAI Selector
xai_method = st.radio(
    "Active Model Explanation Engine:",
    ["💡 Live SHAP (Local Feature Attribution)", "🔬 Live LIME (Local Surrogacy Boundaries)"],
    horizontal=True,
    help="Select the XAI model to analyze the active prediction."
)

col_exp_left, col_exp_right = st.columns([3, 2])

# Custom prediction hook for XAI models that automatically scales the input
def xai_predict_proba(x_raw):
    x_df = pd.DataFrame(x_raw, columns=FEATURES)
    x_scaled = models['scaler'].transform(x_df) if 'scaler' in models else x_df
    return active_model.predict_proba(x_scaled)

with col_exp_left:
    card_left_html = f"""<div class="premium-card">
<div class="metric-label">⚡ Active Predictive Weights</div>
<p style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-top: 8px;'>This shows which specific inputs are pushing the student toward attrition (red) or pulling them to safety (green).</p>
<div style='margin-top: 16px;'>"""
    
    # ------------------------------------------------
    # SHAP Logic
    # ------------------------------------------------
    if "SHAP" in xai_method:
        attributions = []
        try:
            # Attempt to run native SHAP
            X_train_data = pd.read_csv('models/X_train_sample.csv')
            # Use tree-based model proxy for ensemble predictions to ensure stable, non-zero attributions
            explainer_model_key = active_model_key if active_model_key in ['rf', 'xgboost'] else 'rf'
            explainer_model = models[explainer_model_key]
            
            explainer = shap.TreeExplainer(explainer_model)
            shap_vals = explainer.shap_values(input_scaled)
            
            # Handle binary classification lists vs multi-output arrays
            if isinstance(shap_vals, list):
                sv = shap_vals[1][0]
            elif len(shap_vals.shape) == 3:
                sv = shap_vals[0, :, 1]
            elif len(shap_vals.shape) == 2:
                sv = shap_vals[0]
            else:
                sv = shap_vals

            # Combine and sort
            for feat, weight in zip(FEATURES, sv):
                attributions.append({
                    'name': feature_display_names[feat],
                    'value': input_df[feat].values[0],
                    'feature': feat,
                    'weight': weight
                })
                
        except Exception as e:
            card_left_html += f"<div style='color: #EF4444;'>XAI Engine Initialization Error: {e}</div>"
            attributions = []

        # Render SHAP Attributions
        attributions = sorted(attributions, key=lambda x: abs(x['weight']), reverse=True)
        for attr in attributions:
            if abs(attr['weight']) < 0.005:
                continue
                
            color = '#EF4444' if attr['weight'] > 0 else '#10B981'
            direction_label = "Increases Risk" if attr['weight'] > 0 else "Lowers Risk"
            val_pct = min(100, int(abs(attr['weight']) * 200))
            
            # Formatting values for clean look
            if attr['feature'] in ['attendance', 'engagement']:
                val_str = f"{attr['value']:.1%}"
            elif attr['feature'] == 'income_proxy':
                val_str = f"${attr['value']:,}"
            elif attr['feature'] == 'Gender':
                val_str = "Male" if attr['value'] == 1 else "Female"
            else:
                val_str = f"{attr['value']}"
                
            card_left_html += f"""
<div style='margin-bottom: 14px;'>
<div style='display: flex; justify-content: space-between; font-size: 13px; font-weight: 600;'>
<span>{attr['name']} <span style='font-weight: 400; opacity: 0.7;'>({val_str})</span></span>
<span style='color: {color};'>{direction_label} ({attr['weight']:+.2f})</span>
</div>
<div style='width: 100%; background-color: rgba(128, 128, 128, 0.15); height: 8px; border-radius: 4px; overflow: hidden; margin-top: 4px;'>
<div style='background-color: {color}; width: {val_pct}%; height: 100%; border-radius: 4px;'></div>
</div>
</div>"""

    # ------------------------------------------------
    # LIME Logic
    # ------------------------------------------------
    else:
        try:
            X_train_data = pd.read_csv('models/X_train_sample.csv')
            lime_explainer = lime.lime_tabular.LimeTabularExplainer(
                training_data=np.array(X_train_data),
                feature_names=FEATURES,
                class_names=['Stay', 'Dropout'],
                mode='classification',
                random_state=42
            )
            
            exp = lime_explainer.explain_instance(
                data_row=input_df.values[0],
                predict_fn=xai_predict_proba
            )
            
            lime_list = exp.as_list()
            
            for rule, weight in lime_list:
                if abs(weight) < 0.005:
                    continue
                color = '#EF4444' if weight > 0 else '#10B981'
                direction_label = "Increases Risk" if weight > 0 else "Lowers Risk"
                val_pct = min(100, int(abs(weight) * 200))
                
                card_left_html += f"""
<div style='margin-bottom: 14px;'>
<div style='display: flex; justify-content: space-between; font-size: 13px; font-weight: 600;'>
<span style='font-size: 12px;'>{rule}</span>
<span style='color: {color};'>{direction_label} ({weight:+.2f})</span>
</div>
<div style='width: 100%; background-color: rgba(128, 128, 128, 0.15); height: 8px; border-radius: 4px; overflow: hidden; margin-top: 4px;'>
<div style='background-color: {color}; width: {val_pct}%; height: 100%; border-radius: 4px;'></div>
</div>
</div>"""
                
        except Exception as e:
            card_left_html += f"<div style='color: #EF4444;'>LIME Engine Initialization Error: {e}</div>"

    card_left_html += """
</div>
</div>"""
    st.markdown(card_left_html, unsafe_allow_html=True)

with col_exp_right:
    card_right_html = f"""<div class="premium-card" style="height: 100%;">
<div class="metric-label">🎯 Smart Advisory & Intervention Plan</div>
<p style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-top: 8px;'>AI-generated recommendations tailored to the student's primary risk vectors.</p>
<div style='margin-top: 16px;'>"""
    
    recommendations_generated = 0
    
    # Check High At-Risk Factors
    if attendance < 0.75:
        card_right_html += """
<div class="rec-card high-priority">
<h5 style='margin: 0 0 4px 0; color: #EF4444;'>Attendance Recovery Protocol</h5>
<p style='margin: 0; font-size: 12px; opacity: 0.85;'>
The student is missing over 25% of classes. Schedule immediate academic counselor outreach and assign a peer-mentor buddy.
</p>
</div>"""
        recommendations_generated += 1
        
    if gpa < 2.0:
        card_right_html += """
<div class="rec-card high-priority">
<h5 style='margin: 0 0 4px 0; color: #EF4444;'>GPA Restoration Program</h5>
<p style='margin: 0; font-size: 12px; opacity: 0.85;'>
GPA is below academic probation threshold. Auto-enroll in weekly subject tutoring and diagnostic evaluation sessions.
</p>
</div>"""
        recommendations_generated += 1
        
    if engagement < 0.5:
        card_right_html += """
<div class="rec-card medium-priority">
<h5 style='margin: 0 0 4px 0; color: #F59E0B;'>VLE Engagement Optimization</h5>
<p style='margin: 0; font-size: 12px; opacity: 0.85;'>
Low activity in the digital learning environment. Set up automated LMS notifications to trigger daily dashboard logs.
</p>
</div>"""
        recommendations_generated += 1
        
    if income_proxy < 25000:
        card_right_html += """
<div class="rec-card medium-priority">
<h5 style='margin: 0 0 4px 0; color: #F59E0B;'>Financial Assistance Review</h5>
<p style='margin: 0; font-size: 12px; opacity: 0.85;'>
Estimated income proxy suggests potential financial friction. Refer to the Student Grants & emergency support portal.
</p>
</div>"""
        recommendations_generated += 1

    if recommendations_generated == 0:
        card_right_html += """
<div class="rec-card" style="border-left-color: #10B981; background-color: rgba(16, 185, 129, 0.1);">
<h5 style='margin: 0 0 4px 0; color: #10B981;'>Maintain Current Track</h5>
<p style='margin: 0; font-size: 12px; opacity: 0.85;'>
Student is performing beautifully across all academic and financial metrics. Continue standard academic milestones tracking.
</p>
</div>"""
        
    card_right_html += """
</div>
</div>"""
    st.markdown(card_right_html, unsafe_allow_html=True)

# ----------------------------------------------------
# Optional Collapsible Advanced Diagnostic Plots
# ----------------------------------------------------
with st.expander("🛠️ Advanced Technical Diagnostics (Original Plots)"):
    tab_diag1, tab_diag2 = st.tabs(["🔥 Raw SHAP Force Diagram", "🔬 Raw LIME Perturbation Chart"])
    
    with tab_diag1:
        try:
            explainer = shap.TreeExplainer(active_model)
            shap_values = explainer.shap_values(input_scaled)
            fig, ax = plt.subplots(figsize=(10, 4))
            if isinstance(shap_values, list):
                shap.force_plot(explainer.expected_value[1], shap_values[1], input_df, matplotlib=True, show=False)
            else:
                shap.summary_plot(shap_values, input_df, plot_type="bar", show=False)
            st.pyplot(plt.gcf(), clear_figure=True)
        except Exception as e:
            st.info("💡 Standard Tree Explainer plot is available for Tree/Forest models only. Use the dynamic real-time driver bars above for general models.")
            
    with tab_diag2:
        try:
            X_train_data = pd.read_csv('models/X_train_sample.csv')
            lime_explainer = lime.lime_tabular.LimeTabularExplainer(
                training_data=np.array(X_train_data),
                feature_names=FEATURES,
                class_names=['Stay', 'Dropout'],
                mode='classification'
            )
            exp = lime_explainer.explain_instance(
                data_row=input_df.values[0],
                predict_fn=xai_predict_proba
            )
            fig = exp.as_pyplot_figure()
            st.pyplot(fig, clear_figure=True)
        except Exception as e:
            st.info(f"💡 Advanced LIME plot requires aligned training data coordinates: {e}")

# Footer
st.markdown("""
<hr style='border: 0; border-top: 1px solid rgba(128, 128, 128, 0.2); margin: 40px 0 20px 0;'/>
<div style='display: flex; justify-content: space-between; align-items: center; color: #94A3B8; font-size: 12px;'>
    <span>Powered by Advanced Explainable Machine Learning (XAI)</span>
    <span>© 2026 EduSafe AI Platform. All Rights Reserved.</span>
</div>
""", unsafe_allow_html=True)

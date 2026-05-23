import streamlit as st
import os
import joblib
import pickle

# Must be the very first Streamlit command executed
st.set_page_config(
    page_title="EduSafe AI - Student Success Portal",
    page_icon="school",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global Configuration
if "student_data" not in st.session_state:
    st.session_state.student_data = None
if "selected_preset_name" not in st.session_state:
    st.session_state.selected_preset_name = "Custom Profile (Use Interface Controls)"

# Premium UI Theme using Vanilla CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    h1, h2, h3, .title-text { font-family: 'Outfit', sans-serif; font-weight: 700; }
    
    .premium-card {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 24px;
    }
    .badge {
        display: inline-block; padding: 6px 12px; border-radius: 9999px;
        font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;
    }
    .badge-danger { background-color: rgba(239, 68, 68, 0.15); color: #EF4444; border: 1px solid rgba(239, 68, 68, 0.4); }
    .badge-warning { background-color: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.4); }
    .badge-success { background-color: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.4); }
    .metric-value { font-size: 36px; font-weight: 700; letter-spacing: -0.02em; }
    .metric-label { font-size: 14px; font-weight: 600; opacity: 0.7; text-transform: uppercase; letter-spacing: 0.05em; }
    .risk-bar-container { width: 100%; background-color: rgba(128, 128, 128, 0.2); border-radius: 9999px; height: 12px; margin: 12px 0; overflow: hidden; }
    .risk-bar-fill { height: 100%; border-radius: 9999px; transition: width 0.6s ease-in-out; }
    .rec-card { border-left: 5px solid #3B82F6; background-color: rgba(59, 130, 246, 0.1); color: var(--text-color); padding: 16px; border-radius: 8px; margin-bottom: 12px; }
    .rec-card.high-priority { border-left-color: #EF4444; background-color: rgba(239, 68, 68, 0.1); }
    .rec-card.medium-priority { border-left-color: #F59E0B; background-color: rgba(245, 158, 11, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# Cache resource allocation across page loads
@st.cache_resource
def load_models():
    models = {}
    models_dir = 'models'
    for key, filename in [('best', 'best_model.pkl'), ('rf', 'random_forest_model.pkl'), ('xgboost', 'xgboost_model.pkl'), ('scaler', 'scaler.pkl')]:
        filepath = os.path.join(models_dir, filename)
        try:
            models[key] = joblib.load(filepath)
        except Exception:
            try:
                with open(filepath, 'rb') as f:
                    models[key] = pickle.load(f)
            except Exception:
                st.error(f"[WARNING] Failed to load system model: {filename}")
    return models

st.session_state.models = load_models()

# Core Navigation Definitions
landing_page = st.Page("views/landing.py", title="System Welcome", icon="home", default=True)
form_page = st.Page("views/input_form.py", title="Student Profile Setup", icon="description")
dashboard_page = st.Page("views/dashboard.py", title="Analytics & Interventions", icon="analytics")

pg = st.navigation({
    "Navigation": [landing_page, form_page, dashboard_page]
})
pg.run()

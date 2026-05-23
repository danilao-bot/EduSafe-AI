import streamlit as st
import streamlit.components.v1 as components
import os
import joblib
import pickle
import warnings
warnings.filterwarnings('ignore')

# Must be the very first Streamlit command executed
st.set_page_config(
    page_title="EduSafe AI - Student Success Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global Configuration
if "student_data" not in st.session_state:
    st.session_state.student_data = None
if "selected_preset_name" not in st.session_state:
    st.session_state.selected_preset_name = "Custom Profile (Use Interface Controls)"

# Premium Dark Glassmorphism Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg-color: #0F172A;
        --card-bg: rgba(30, 41, 59, 0.7);
        --text-main: #F8FAFC;
        --text-muted: #94A3B8;
        --accent: #3B82F6;
        --border-color: rgba(255, 255, 255, 0.1);
    }
    
    /* Overall Background */
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-main);
    }
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    h1, h2, h3, h4, h5, .title-text { font-family: 'Outfit', sans-serif; font-weight: 700; color: var(--text-main) !important; }
    p, span, div { color: var(--text-main); }
    
    .premium-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 24px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .premium-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
    }
    
    .badge {
        display: inline-block; padding: 6px 12px; border-radius: 9999px;
        font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;
    }
    .badge-danger { background-color: rgba(239, 68, 68, 0.2); color: #FCA5A5; border: 1px solid rgba(239, 68, 68, 0.5); }
    .badge-warning { background-color: rgba(245, 158, 11, 0.2); color: #FCD34D; border: 1px solid rgba(245, 158, 11, 0.5); }
    .badge-success { background-color: rgba(16, 185, 129, 0.2); color: #6EE7B7; border: 1px solid rgba(16, 185, 129, 0.5); }
    
    .metric-value { font-size: 36px; font-weight: 700; letter-spacing: -0.02em; color: var(--text-main); }
    .metric-label { font-size: 14px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }
    
    .risk-bar-container { width: 100%; background-color: rgba(255, 255, 255, 0.1); border-radius: 9999px; height: 12px; margin: 12px 0; overflow: hidden; }
    .risk-bar-fill { height: 100%; border-radius: 9999px; transition: width 1s cubic-bezier(0.4, 0, 0.2, 1); }
    
    .rec-card { border-left: 5px solid var(--accent); background: rgba(59, 130, 246, 0.15); padding: 16px; border-radius: 8px; margin-bottom: 12px; backdrop-filter: blur(4px); }
    .rec-card.high-priority { border-left-color: #EF4444; background: rgba(239, 68, 68, 0.15); }
    .rec-card.medium-priority { border-left-color: #F59E0B; background: rgba(245, 158, 11, 0.15); }
    
    /* Responsive stacking for custom flex layouts */
    @media (max-width: 768px) {
        .responsive-flex {
            flex-direction: column !important;
            gap: 16px !important;
        }
        .responsive-flex > div {
            width: 100% !important;
        }
        .premium-card {
            padding: 16px;
        }
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--bg-color) !important;
        border-right: 1px solid var(--border-color);
    }
    </style>
    """, unsafe_allow_html=True)

# Inject Open Graph Meta Tags for SEO/Social Sharing
components.html("""
<script>
    if(!document.querySelector("meta[property='og:title']")) {
        const ogTitle = document.createElement('meta');
        ogTitle.setAttribute('property', 'og:title');
        ogTitle.setAttribute('content', 'EduSafe AI - Student Success Portal');
        document.head.appendChild(ogTitle);

        const ogDesc = document.createElement('meta');
        ogDesc.setAttribute('property', 'og:description');
        ogDesc.setAttribute('content', 'Identify at-risk students before they drop out. Predictive AI built for advisors.');
        document.head.appendChild(ogDesc);
        
        const ogType = document.createElement('meta');
        ogType.setAttribute('property', 'og:type');
        ogType.setAttribute('content', 'website');
        document.head.appendChild(ogType);
    }
</script>
""", height=0, width=0)

# Cache resource allocation across page loads
@st.cache_resource
def load_models():
    models = {}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, 'models')
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
landing_page = st.Page("views/landing.py", title="System Welcome", icon="🏠", default=True)
form_page = st.Page("views/input_form.py", title="Student Profile Setup", icon="📋")
dashboard_page = st.Page("views/dashboard.py", title="Analytics & Interventions", icon="📊")

pg = st.navigation({
    "Navigation": [landing_page, form_page, dashboard_page]
})
pg.run()

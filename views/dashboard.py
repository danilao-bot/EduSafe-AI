import streamlit as st
import pandas as pd
import numpy as np
import shap
import lime
import lime.lime_tabular
import matplotlib.pyplot as plt
import os

# Route Guard Configuration
if st.session_state.student_data is None:
    st.warning("⚠️ Access Denied: No student payload detected. Please execute profile configuration first.")
    if st.button("Return to Form Setup"):
        st.switch_page("views/input_form.py")
    st.stop()

# Load state memory variables
data = st.session_state.student_data
models = st.session_state.models
preset_display_name = st.session_state.selected_preset_name.split(" (")[0]

FEATURES = ['gpa', 'attendance', 'engagement', 'income_proxy', 'low_gpa_flag', 
            'low_engagement_flag', 'risk_score', 'Unemployment rate', 'Age at enrollment', 'Gender']

feature_display_names = {
    'gpa': 'Cumulative GPA', 'attendance': 'Attendance Rate', 'engagement': 'VLE Engagement Score',
    'income_proxy': 'Household Income', 'low_gpa_flag': 'Low GPA Alert Flag',
    'low_engagement_flag': 'Low Engagement Alert Flag', 'risk_score': 'Institutional Risk Index',
    'Unemployment rate': 'Regional Unemployment', 'Age at enrollment': 'Age at Enrollment', 'Gender': 'Gender Code'
}

input_df = pd.DataFrame(data, index=[0])
input_scaled = pd.DataFrame(models['scaler'].transform(input_df), columns=FEATURES) if 'scaler' in models else input_df

# Evaluate Model Predictions
preds = {}
for name, m_key in [("Best Ensemble Model", "best"), ("Random Forest Classifier", "rf"), ("XGBoost Predictor", "xgboost")]:
    if m_key in models:
        try: preds[name] = models[m_key].predict_proba(input_scaled)[0][1]
        except Exception: preds[name] = 0.5

# Active parameter routing selectors inside sidebar
st.sidebar.markdown("### ⚙️ Analysis Parameters")
selected_explain_model_name = st.sidebar.radio("Active Explanation Model:", list(preds.keys()))
model_mapping = {"Best Ensemble Model": "best", "Random Forest Classifier": "rf", "XGBoost Predictor": "xgboost"}
active_model_key = model_mapping[selected_explain_model_name]
active_model = models[active_model_key]
active_proba = preds[selected_explain_model_n# Row 1 Dashboard Scoreboard Metric Rendering
c1, c2, c3 = st.columns([1.5, 2, 1.5], gap="medium")

with c1:
    st.markdown(f"""<div class="premium-card" style="height: 100%; margin: 0;">
    <div class="metric-label">Active Target Snapshot</div>
    <div style='margin-top: 12px;'>
    <div style='font-size: 20px; font-weight: 700; color: var(--text-main);'>{preset_display_name}</div>
    <div style='color: var(--text-muted); font-size: 13px;'>Age: {data['Age at enrollment']} | Gender: {"Male" if data['Gender'] == 1 else "Female"}</div>
    <hr style='border: 0; border-top: 1px solid var(--border-color); margin: 12px 0;'/>
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12px; color: var(--text-main);'>
    <div>GPA:<br/><b>{data['gpa']:.2f}</b></div>
    <div>ATTENDANCE:<br/><b>{data['attendance']:.1%}</b></div>
    <div>ENGAGEMENT:<br/><b>{data['engagement']:.1%}</b></div>
    <div>INCOME PROXY:<br/><b>${data['income_proxy']:,}</b></div>
    </div></div></div>""", unsafe_allow_html=True)

with c2:
    bar_color = '#EF4444' if active_proba > 0.65 else ('#F59E0B' if active_proba > 0.35 else '#10B981')
    badge_html = '<span class="badge badge-danger">⚠️ Critical At-Risk</span>' if active_proba > 0.65 else ('<span class="badge badge-warning">⚡ Moderate Concern</span>' if active_proba > 0.35 else '<span class="badge badge-success">✅ Stable / Successful</span>')
    st.markdown(f"""<div class="premium-card" style="height: 100%; margin: 0;">
    <div class="metric-label">Predictive Dropout Risk Score</div>
    <div style='display: flex; justify-content: space-between; align-items: baseline; margin-top: 8px;'>
    <div class="metric-value" style='color: {bar_color};'>{active_proba:.1%}</div>
    <div>{badge_html}</div>
    </div>
    <div class="risk-bar-container"><div class="risk-bar-fill" style="width: {active_proba*100}%; background-color: {bar_color};"></div></div>
    <div style='font-size: 12px; color: var(--text-muted);'>Calculated via real-time inference using <strong>{selected_explain_model_name}</strong> targets.</div>
    </div>""", unsafe_allow_html=True)

with c3:
    comp_html = f"""<div class="premium-card" style="height: 100%; margin: 0;"><div class="metric-label">Cross-Model Comparison</div><div style='margin-top: 12px;'>"""
    for name, p_val in preds.items():
        sub_color = '#10B981' if p_val < 0.35 else ('#F59E0B' if p_val < 0.65 else '#EF4444')
        bg_highlight = "background: rgba(255, 255, 255, 0.1); border-radius: 6px; padding: 4px 8px;" if name == selected_explain_model_name else ""
        comp_html += f"""<div style='display: flex; justify-content: space-between; margin-bottom: 8px; {bg_highlight}'><span style='font-size: 12px; color: var(--text-main);'>{name.split(" ")[0]}</span><span style='font-size: 13px; font-weight:600; color: {sub_color};'>{p_val:.1%}</span></div>"""
    st.markdown(comp_html + "</div></div>", unsafe_allow_html=True)

# Row 2 Unified Live XAI Engine Layout Split
st.markdown("### 🔍 Live Decision Driver & Intervention Engine")
xai_method = st.radio("Active Model Explanation Engine:", ["💡 Live SHAP (Local Feature Attribution)", "🧪 Live LIME (Local Surrogacy Boundaries)"], horizontal=True)

col_exp_left, col_exp_right = st.columns([3, 2], gap="medium")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
x_train_path = os.path.join(base_dir, 'models', 'X_train_sample.csv')

with col_exp_left:
    card_left_html = f"""<div class="premium-card" style="height: 100%;"><div class="metric-label">⚡ Active Predictive Weights</div><div style='margin-top: 16px;'>"""
    if "SHAP" in xai_method:
        try:
            exp_key = active_model_key if active_model_key in ['rf', 'xgboost'] else 'rf'
            explainer = shap.TreeExplainer(models[exp_key])
            shap_vals = explainer.shap_values(input_scaled)
            sv = shap_vals[1][0] if isinstance(shap_vals, list) else (shap_vals[0, :, 1] if len(shap_vals.shape) == 3 else shap_vals[0])
            
            attributions = sorted([{'name': feature_display_names[f], 'value': data[f], 'feature': f, 'weight': w} for f, w in zip(FEATURES, sv)], key=lambda x: abs(x['weight']), reverse=True)
            for attr in attributions:
                if abs(attr['weight']) < 0.005: continue
                color = '#EF4444' if attr['weight'] > 0 else '#10B981'
                val_str = f"{attr['value']:.1%}" if attr['feature'] in ['attendance', 'engagement'] else (f"${attr['value']:,}" if attr['feature'] == 'income_proxy' else f"{attr['value']}")
                card_left_html += f"""<div style='margin-bottom: 12px;'><div style='display:flex; justify-content:space-between; font-size:13px; color: var(--text-main);'><span>{attr['name']} ({val_str})</span><span style='color:{color};'>{'Increases Risk' if attr['weight'] > 0 else 'Lowers Risk'} ({attr['weight']:+.2f})</span></div><div style='width:100%; background:rgba(255,255,255,0.1); height:6px; border-radius:4px; overflow:hidden; margin-top:4px;'><div style='background:{color}; width:{min(100, int(abs(attr['weight'])*200))}%; height:100%;'></div></div></div>"""
        except Exception as e: card_left_html += f"<div style='color: var(--text-main);'>XAI Generation Variance Exception: {e}</div>"
    else:
        try:
            X_train_sample = pd.read_csv(x_train_path) if os.path.exists(x_train_path) else np.random.rand(10, len(FEATURES))
            lime_explainer = lime.lime_tabular.LimeTabularExplainer(np.array(X_train_sample), feature_names=FEATURES, class_names=['Stay', 'Dropout'], mode='classification', random_state=42)
            fn = lambda x: models[active_model_key].predict_proba(models['scaler'].transform(pd.DataFrame(x, columns=FEATURES)) if 'scaler' in models else pd.DataFrame(x, columns=FEATURES))
            exp = lime_explainer.explain_instance(input_df.values[0], fn)
            for rule, weight in exp.as_list():
                if abs(weight) < 0.005: continue
                color = '#EF4444' if weight > 0 else '#10B981'
                card_left_html += f"""<div style='margin-bottom:12px;'><div style='display:flex; justify-content:space-between; font-size:12px; color: var(--text-main);'><span>{rule}</span><span style='color:{color};'>{'Increases Risk' if weight > 0 else 'Lowers Risk'} ({weight:+.2f})</span></div><div style='width:100%; background:rgba(255,255,255,0.1); height:6px; border-radius:4px; overflow:hidden; margin-top:4px;'><div style='background:{color}; width:{min(100, int(abs(weight)*200))}%; height:100%;'></div></div></div>"""
        except Exception as e: card_left_html += f"<div style='color: var(--text-main);'>LIME Engine Initialization Exception: {e}</div>"
    st.markdown(card_left_html + "</div></div>", unsafe_allow_html=True)

with col_exp_right:
    card_right_html = """<div class="premium-card" style="height: 100%;"><div class="metric-label">🎯 Smart Advisory Intervention Plan</div><div style='margin-top: 16px;'>"""
    recs = 0
    if data['attendance'] < 0.75:
        card_right_html += """<div class="rec-card high-priority"><h5 style='margin:0; color:#FCA5A5;'>Attendance Recovery Protocol</h5><p style='margin:4px 0 0 0; font-size:12px; color: var(--text-main);'>Student attendance below threshold. Flag immediate counselor check-in routing.</p></div>"""
        recs += 1
    if data['gpa'] < 2.0:
        card_right_html += """<div class="rec-card high-priority"><h5 style='margin:0; color:#FCA5A5;'>GPA Restoration Program</h5><p style='margin:4px 0 0 0; font-size:12px; color: var(--text-main);'>Academic performance tracking below baseline requirements. Schedule priority peer tutoring support.</p></div>"""
        recs += 1
    if data['engagement'] < 0.5:
        card_right_html += """<div class="rec-card medium-priority"><h5 style='margin:0; color:#FCD34D;'>VLE Engagement Optimization</h5><p style='margin:4px 0 0 0; font-size:12px; color: var(--text-main);'>Low LMS platform trace activity logs. Activate daily automated mobile learning reminders.</p></div>"""
        recs += 1
    if recs == 0:
        card_right_html += """<div class="rec-card" style="border-left-color:#34D399; background:rgba(16,185,129,0.15);"><h5 style='margin:0; color:#6EE7B7;'>Maintain Current Track</h5><p style='margin:4px 0 0 0; font-size:12px; color: var(--text-main);'>Metrics conform optimally across historical bounds. Continue standard semester mapping tracking.</p></div>"""
    st.markdown(card_right_html + "</div></div>", unsafe_allow_html=True)

with st.expander("🛠️ Advanced Technical Diagnostics (Original Plots)"):
    t1, t2 = st.tabs(["🔥 Raw SHAP Force Diagram", "🧪 Raw LIME Perturbation Chart"])
    with t1: st.info("💡 Dynamic weights above render live explanations. Matplotlib SHAP wrappers map to native models on execution host runtime.")
    with t2:
        try:
            X_train_sample = pd.read_csv(x_train_path) if os.path.exists(x_train_path) else np.random.rand(10, len(FEATURES))
            lime_explainer = lime.lime_tabular.LimeTabularExplainer(np.array(X_train_sample), feature_names=FEATURES, class_names=['Stay', 'Dropout'], mode='classification')
            fn = lambda x: models[active_model_key].predict_proba(models['scaler'].transform(pd.DataFrame(x, columns=FEATURES)) if 'scaler' in models else pd.DataFrame(x, columns=FEATURES))
            fig = lime_explainer.explain_instance(input_df.values[0], fn).as_pyplot_figure()
            st.pyplot(fig, clear_figure=True)
        except Exception as e: st.info(f"💡 Advanced plot requires specific training coordinate files: {e}")

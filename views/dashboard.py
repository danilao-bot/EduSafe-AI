import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import streamlit.components.v1 as components

# Add parent directory to path to import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import convert_usd_to_naira, convert_naira_to_usd, format_naira, employment_status_display

# ── Route Guard ───────────────────────────────────────────────────────────────
if not st.session_state.get("student_data"):
    st.markdown("""
    <div class="premium-card" style="text-align:center; padding:48px;">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-bottom:16px;">
            <rect x="5" y="10" width="14" height="10" rx="2" stroke="#93C5FD" stroke-width="1.5"/>
            <path d="M9 10V7C9 5.34 10.34 4 12 4C13.66 4 15 5.34 15 7V10" stroke="#93C5FD" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <h2 style="color:var(--text-main);">No Student Profile Loaded</h2>
        <p style="color:var(--text-muted);">Please fill in the student profile form before viewing the dashboard.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Student Profile Form", type="primary", use_container_width=False):
        st.switch_page("views/input_form.py")
    st.stop()

# ── Safe Imports ──────────────────────────────────────────────────────────────
try:
    import shap
    SHAP_AVAILABLE = True
except Exception:
    SHAP_AVAILABLE = False

try:
    import lime
    import lime.lime_tabular
    LIME_AVAILABLE = True
except Exception:
    LIME_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    MPL_AVAILABLE = True
except Exception:
    MPL_AVAILABLE = False

# ── Load State ────────────────────────────────────────────────────────────────
data    = st.session_state.student_data
models  = st.session_state.get("models", {})
preset_display_name = st.session_state.get("selected_preset_name", "Custom Profile").split(" (")[0]

FEATURES = ['gpa', 'attendance', 'engagement', 'income_proxy', 'low_gpa_flag',
            'low_engagement_flag', 'risk_score', 'Unemployment rate', 'Age at enrollment', 'Gender']

feature_display_names = {
    'gpa': 'GPA', 'attendance': 'Attendance', 'engagement': 'Online Engagement',
    'income_proxy': 'Family Income', 'low_gpa_flag': 'Low GPA Flag',
    'low_engagement_flag': 'Low Engagement Flag', 'risk_score': "Counselor's Concern",
    'Unemployment rate': 'Employment Status', 'Age at enrollment': 'Enrollment Age', 'Gender': 'Gender'
}

# ── Safe Data Preparation ─────────────────────────────────────────────────────
try:
    input_df = pd.DataFrame(data, index=[0])
except Exception as e:
    st.error(f"Could not read student data: {e}")
    st.stop()

try:
    if 'scaler' in models:
        input_scaled = pd.DataFrame(models['scaler'].transform(input_df), columns=FEATURES)
    else:
        input_scaled = input_df.copy()
        st.toast("Scaler not available — using raw values for inference.", icon="ℹ")
except Exception as e:
    st.warning(f"Feature scaling failed — falling back to raw input values. ({e})")
    input_scaled = input_df.copy()

# ── Header Row ────────────────────────────────────────────────────────────────
col_title, col_export = st.columns([3, 1], gap="medium")
with col_title:
    st.markdown("## Analytics & Interventions Dashboard")
with col_export:
    st.download_button(
        label="Export Report (CSV)",
        data=input_df.to_csv(index=False),
        file_name=f"edusafe_report_age{data.get('Age at enrollment', 'unknown')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ── Safe Model Inference ──────────────────────────────────────────────────────
preds = {}
pred_errors = []
for name, m_key in [("Best Ensemble Model", "best"), ("Random Forest Classifier", "rf"), ("XGBoost Predictor", "xgboost")]:
    if m_key not in models:
        pred_errors.append(f"Model '{name}' was not loaded — skipping.")
        continue
    try:
        preds[name] = models[m_key].predict_proba(input_scaled)[0][1]
    except Exception as e:
        pred_errors.append(f"Inference failed for '{name}': {e}")
        preds[name] = 0.5  # safe neutral fallback

if pred_errors:
    with st.expander("Inference Warnings (click to expand)", expanded=False):
        for err in pred_errors:
            st.warning(err)

if not preds:
    st.error("No predictive models could run. Please check that model files exist in the `/models` directory and redeploy.")
    st.stop()

# ── Sidebar Controls ──────────────────────────────────────────────────────────
st.sidebar.markdown("### Analysis Parameters")
selected_explain_model_name = st.sidebar.radio("Active Explanation Model:", list(preds.keys()))
model_mapping = {"Best Ensemble Model": "best", "Random Forest Classifier": "rf", "XGBoost Predictor": "xgboost"}
active_model_key = model_mapping.get(selected_explain_model_name, "rf")
active_model     = models.get(active_model_key)
active_proba     = preds.get(selected_explain_model_name, 0.5)

# ── Row 1: Metric Cards ───────────────────────────────────────────────────────
st.markdown("""
<style>
    @media (max-width: 640px) {
        .metric-cards-row { display: grid; grid-template-columns: 1fr; gap: 16px; }
        .metric-card-item { min-height: 280px; }
    }
    @media (min-width: 641px) and (max-width: 1024px) {
        .metric-cards-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    }
    @media (min-width: 1025px) {
        .metric-cards-row { display: grid; grid-template-columns: 1.5fr 2fr 1.5fr; gap: 16px; }
    }
</style>
""", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1.5, 2, 1.5], gap="medium")

with c1:
    att_display = f"{data['attendance']:.0%}" if data.get('attendance') is not None else "N/A"
    st.markdown(f"""<div class="premium-card" style="height:100%; margin:0;">
    <div class="metric-label">Active Target Snapshot</div>
    <div style='margin-top:12px;'>
        <div style='font-size:20px; font-weight:700; color:var(--text-main);'>{preset_display_name}</div>
        <div style='color:var(--text-muted); font-size:13px;'>Age: {data.get('Age at enrollment','N/A')} &nbsp;|&nbsp; Gender: {"Male" if data.get('Gender')==1 else "Female"}</div>
        <hr style='border:0; border-top:1px solid var(--border-color); margin:12px 0;'/>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:12px; color:var(--text-main);'>
            <div>GPA:<br/><b>{data.get('gpa', 0):.2f}</b></div>
            <div>ATTENDANCE:<br/><b>{att_display}</b></div>
            <div>ENGAGEMENT:<br/><b>{data.get('engagement', 0):.1%}</b></div>
            <div>INCOME:<br/><b>{format_naira(convert_usd_to_naira(data.get('income_proxy', 0)))}</b></div>
        </div>
    </div></div>""", unsafe_allow_html=True)

with c2:
    bar_color  = '#EF4444' if active_proba > 0.65 else ('#F59E0B' if active_proba > 0.35 else '#10B981')
    badge_html = (
        '<span class="badge badge-danger">⚠️ Critical At-Risk</span>' if active_proba > 0.65 else
        '<span class="badge badge-warning">⚡ Moderate Concern</span>' if active_proba > 0.35 else
        '<span class="badge badge-success">✅ Stable & Progressing</span>'
    )
    st.markdown(f"""<div class="premium-card" style="height:100%; margin:0;">
    <div class="metric-label">Predictive Dropout Risk Score</div>
    <div style='display:flex; justify-content:space-between; align-items:baseline; margin-top:8px;'>
        <div class="metric-value" style='color:{bar_color};'>{active_proba:.1%}</div>
        <div>{badge_html}</div>
    </div>
    <div class="risk-bar-container"><div class="risk-bar-fill" style="width:{active_proba*100:.1f}%; background-color:{bar_color};"></div></div>
    <div style='font-size:12px; color:var(--text-muted);'>Calculated via <strong>{selected_explain_model_name}</strong></div>
    </div>""", unsafe_allow_html=True)

with c3:
    comp_html = """<div class="premium-card" style="height:100%; margin:0;"><div class="metric-label">Cross-Model Comparison</div><div style='margin-top:12px;'>"""
    for name, p_val in preds.items():
        sub_color    = '#10B981' if p_val < 0.35 else ('#F59E0B' if p_val < 0.65 else '#EF4444')
        bg_highlight = "background:rgba(255,255,255,0.1); border-radius:6px; padding:4px 8px;" if name == selected_explain_model_name else ""
        short_name   = name.replace(" Model","").replace(" Classifier","").replace(" Predictor","")
        comp_html   += f"<div style='display:flex; justify-content:space-between; margin-bottom:8px; {bg_highlight}'><span style='font-size:12px; color:var(--text-main);'>{short_name}</span><span style='font-size:13px; font-weight:600; color:{sub_color};'>{p_val:.1%}</span></div>"
    st.markdown(comp_html + "</div></div>", unsafe_allow_html=True)

# ── Row 2: XAI Engine ────────────────────────────────────────────────────────
st.markdown("### Live Decision Driver & Intervention Engine")
xai_method = st.radio("Explanation Engine:", ["SHAP (Feature Attribution)", "LIME (Surrogate Boundaries)"], horizontal=True)

base_dir     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
x_train_path = os.path.join(base_dir, 'models', 'X_train_sample.csv')

col_exp_left, col_exp_right = st.columns([3, 2], gap="medium")

with col_exp_left:
    card_html = """<div class="premium-card"><div class="metric-label">Active Predictive Weights</div><div style='margin-top:16px;'>"""

    if "SHAP" in xai_method:
        if not SHAP_AVAILABLE:
            st.warning("SHAP library is not installed. Please add `shap` to your `requirements.txt`.")
        elif active_model is None:
            st.warning("The selected model could not be loaded. SHAP cannot run.")
        else:
            try:
                exp_key    = active_model_key if active_model_key in ['rf', 'xgboost'] else 'rf'
                explainer  = shap.TreeExplainer(models[exp_key])
                shap_vals  = explainer.shap_values(input_scaled)
                sv         = shap_vals[1][0] if isinstance(shap_vals, list) else (shap_vals[0, :, 1] if len(shap_vals.shape) == 3 else shap_vals[0])
                attributions = sorted(
                    [{'name': feature_display_names.get(f, f), 'value': data.get(f), 'feature': f, 'weight': w} for f, w in zip(FEATURES, sv)],
                    key=lambda x: abs(x['weight']), reverse=True
                )
                for attr in attributions:
                    if abs(attr['weight']) < 0.005:
                        continue
                    color   = '#EF4444' if attr['weight'] > 0 else '#10B981'
                    val     = attr['value']
                    if attr['feature'] in ['attendance', 'engagement']:
                        val_str = f"{val:.1%}" if val is not None else "N/A"
                    elif attr['feature'] == 'income_proxy':
                        val_str = format_naira(convert_usd_to_naira(val)) if val is not None else "N/A"
                    elif attr['feature'] == 'Unemployment rate':
                        val_str = employment_status_display(val) if val is not None else "N/A"
                    else:
                        val_str = str(val) if val is not None else "N/A"
                    bar_w = min(100, int(abs(attr['weight']) * 200))
                    card_html += f"""
                    <div style='margin-bottom:12px;'>
                        <div style='display:flex; justify-content:space-between; font-size:13px; color:var(--text-main);'>
                            <span>{attr['name']} ({val_str})</span>
                            <span style='color:{color};'>{'↑ Increases Risk' if attr['weight'] > 0 else '↓ Lowers Risk'} ({attr['weight']:+.2f})</span>
                        </div>
                        <div style='width:100%; background:rgba(255,255,255,0.1); height:6px; border-radius:4px; overflow:hidden; margin-top:4px;'>
                            <div style='background:{color}; width:{bar_w}%; height:100%;'></div>
                        </div>
                    </div>"""
            except Exception as e:
                card_html += f"<div style='color:#FCA5A5;'>SHAP could not run for this model configuration.<br/><small style='color:var(--text-muted);'>{e}</small></div>"

    else:  # LIME
        if not LIME_AVAILABLE:
            st.warning("LIME library is not installed. Please add `lime` to your `requirements.txt`.")
        elif active_model is None:
            st.warning("The selected model could not be loaded. LIME cannot run.")
        else:
            try:
                if os.path.exists(x_train_path):
                    X_train_sample = pd.read_csv(x_train_path).values
                else:
                    X_train_sample = np.random.rand(50, len(FEATURES))
                    st.toast("X_train_sample.csv not found — using synthetic background data for LIME.", icon="ℹ")

                lime_explainer = lime.lime_tabular.LimeTabularExplainer(
                    X_train_sample, feature_names=FEATURES,
                    class_names=['Stay', 'Dropout'], mode='classification', random_state=42
                )
                def lime_predict_fn(x):
                    df_x = pd.DataFrame(x, columns=FEATURES)
                    if 'scaler' in models:
                        df_x = pd.DataFrame(models['scaler'].transform(df_x), columns=FEATURES)
                    return models[active_model_key].predict_proba(df_x)

                exp = lime_explainer.explain_instance(input_df.values[0], lime_predict_fn)
                for rule, weight in exp.as_list():
                    if abs(weight) < 0.005:
                        continue
                    color = '#EF4444' if weight > 0 else '#10B981'
                    bar_w = min(100, int(abs(weight) * 200))
                    card_html += f"""
                    <div style='margin-bottom:12px;'>
                        <div style='display:flex; justify-content:space-between; font-size:12px; color:var(--text-main);'>
                            <span>{rule}</span>
                            <span style='color:{color};'>{'↑ Risk' if weight > 0 else '↓ Risk'} ({weight:+.2f})</span>
                        </div>
                        <div style='width:100%; background:rgba(255,255,255,0.1); height:6px; border-radius:4px; overflow:hidden; margin-top:4px;'>
                            <div style='background:{color}; width:{bar_w}%; height:100%;'></div>
                        </div>
                    </div>"""
            except Exception as e:
                card_html += f"<div style='color:#FCA5A5;'>LIME could not run for this model configuration.<br/><small style='color:var(--text-muted);'>{e}</small></div>"

    st.markdown(card_html + "</div></div>", unsafe_allow_html=True)

with col_exp_right:
    card_right = """<div class="premium-card"><div class="metric-label">Smart Advisory Intervention Plan</div><div style='margin-top:16px;'>"""
    recs = 0
    if data.get('attendance', 1.0) < 0.75:
        card_right += """<div class="rec-card high-priority"><h5 style='margin:0; color:#FCA5A5;'>Attendance Recovery Protocol</h5><p style='margin:4px 0 0; font-size:12px; color:var(--text-main);'>Attendance is below the 75% threshold. Flag for an immediate counsellor check-in.</p></div>"""
        recs += 1
    if data.get('gpa', 4.0) < 2.0:
        card_right += """<div class="rec-card high-priority"><h5 style='margin:0; color:#FCA5A5;'>GPA Restoration Program</h5><p style='margin:4px 0 0; font-size:12px; color:var(--text-main);'>GPA below minimum baseline. Schedule priority peer tutoring and academic support.</p></div>"""
        recs += 1
    if data.get('engagement', 1.0) < 0.5:
        card_right += """<div class="rec-card medium-priority"><h5 style='margin:0; color:#FCD34D;'>Online Engagement Boost</h5><p style='margin:4px 0 0; font-size:12px; color:var(--text-main);'>Low portal activity detected. Enable automated daily mobile learning reminders.</p></div>"""
        recs += 1
    if recs == 0:
        card_right += """<div class="rec-card" style="border-left-color:#34D399; background:rgba(16,185,129,0.15);"><h5 style='margin:0; color:#6EE7B7;'>✅ All Metrics in Good Standing</h5><p style='margin:4px 0 0; font-size:12px; color:var(--text-main);'>No immediate interventions required. Continue standard semester tracking.</p></div>"""
    st.markdown(card_right + "</div></div>", unsafe_allow_html=True)

# ── Advanced Diagnostics Expander ─────────────────────────────────────────────
with st.expander("Advanced Technical Diagnostics"):
    t1, t2 = st.tabs(["SHAP Force Diagram", "LIME Perturbation Chart"])
    with t1:
        if not SHAP_AVAILABLE:
            st.warning("SHAP library is not installed.")
        elif active_model is None:
            st.warning("The selected model could not be loaded for SHAP plotting.")
        else:
            try:
                exp_key = active_model_key if active_model_key in ['rf', 'xgboost'] else 'rf'
                explainer = shap.TreeExplainer(models[exp_key])
                shap_vals = explainer.shap_values(input_scaled)
                
                if isinstance(shap_vals, list):
                    sv = shap_vals[1][0]
                    ev = explainer.expected_value[1]
                else:
                    sv = shap_vals[0, :, 1] if len(shap_vals.shape) == 3 else shap_vals[0]
                    ev = explainer.expected_value
                    if isinstance(ev, (list, np.ndarray)):
                        ev = ev[-1]
                        
                fig = shap.force_plot(ev, sv, input_scaled.iloc[0,:], feature_names=FEATURES)
                shap_html = f"<head>{shap.getjs()}</head><body>{fig.html()}</body>"
                components.html(shap_html, height=200)
            except Exception as e:
                st.warning(f"SHAP plot could not be generated. ({e})")
    with t2:
        if not LIME_AVAILABLE or not MPL_AVAILABLE:
            st.warning("LIME or Matplotlib is not available in this environment.")
        elif active_model is None:
            st.warning("The selected model could not be loaded for LIME plotting.")
        else:
            try:
                if os.path.exists(x_train_path):
                    X_train_sample = pd.read_csv(x_train_path).values
                else:
                    X_train_sample = np.random.rand(50, len(FEATURES))
                lime_exp = lime.lime_tabular.LimeTabularExplainer(
                    X_train_sample, feature_names=FEATURES, class_names=['Stay', 'Dropout'], mode='classification'
                )
                def lime_plot_fn(x):
                    df_x = pd.DataFrame(x, columns=FEATURES)
                    if 'scaler' in models:
                        df_x = pd.DataFrame(models['scaler'].transform(df_x), columns=FEATURES)
                    return models[active_model_key].predict_proba(df_x)
                fig = lime_exp.explain_instance(input_df.values[0], lime_plot_fn).as_pyplot_figure()
                st.pyplot(fig, clear_figure=True)
            except Exception as e:
                st.warning(f"LIME plot could not be generated in this environment. ({e})")

# EduSafe AI™ — Student Success Early Warning Portal

EduSafe AI™ is a state-of-the-art, interactive student dropout early warning system and explainable intervention dashboard. It uses Machine Learning, SHAP, and LIME to help academic advisors identify students at risk, explain the driving factors, and suggest recovery actions.

---

## Features

- **Risk Prediction Dashboard:** Visual risk gauge with Safe, Warning, and Critical states.
- **Explainable AI:**
  - **SHAP attributions** for exact feature contributions.
  - **LIME explanations** for local interpretability.
- **Advisory Playbooks:** Tailored suggestions for interventions such as attendance recovery, GPA support, and financial aid checks.
- **Interactive Profiles:** Use sample student profiles or test custom inputs in real time.

---

## Project Structure

```text
EduSafe-AI/
 ├── app.py
 ├── inspect_model.py
 ├── README.md
 ├── requirements.txt
 ├── .gitignore
 ├── models/
 │    └── X_train_sample.csv
 └── views/
      ├── dashboard.py
      ├── input_form.py
      └── landing.py
```

---

## Local Installation & Upgrade

### 1. Prerequisites
- Python 3.9 or newer
- `pip` available in your environment

### 2. Install or Upgrade Dependencies
From the project root, run:
```bash
pip install -r requirements.txt
```

If you are upgrading an existing install, re-running this command will install the latest required packages from `requirements.txt`.

### 3. Run the App
Start the Streamlit app:
```bash
streamlit run app.py
```
Then open:
http://localhost:8501

---

## Notes

- If installation is still running, wait until `pip install -r requirements.txt` finishes successfully.
- If you see package version errors, try upgrading pip first:
```bash
python -m pip install --upgrade pip
```

---

## Git Setup (master branch)

Use these commands when your repository uses `master` as the default branch:
```bash
git init
git add .
git commit -m "feat: initial commit of EduSafe AI"
git branch -M master
git remote add origin  https://github.com/danilao-bot/EduSafe-AI.git
git push -u origin master
```

If your remote already exists, replace `git remote add origin ...` with:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
``` 

---

## Deployment

### Streamlit Community Cloud
1. Push the repo to GitHub.
2. Create a new app on Streamlit Cloud.
3. Set the main file path to `app.py`.

> If your repository uses the `master` branch instead of `main`, use `master` when configuring GitHub or deployment settings.

### Docker (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## Quick Tip
When you update `requirements.txt`, run:
```bash
pip install -r requirements.txt
```
again to apply the new package versions.

---

*Built to support student success with explainable machine learning.*

import pickle
import pandas as pd
import os
import joblib

models_dir = 'models'
model_files = [
    'best_model.pkl',
    'logistic_regression_model.pkl',
    'random_forest_model.pkl',
    'scaler.pkl',
    'xgboost_model.pkl'
]

for file in model_files:
    path = os.path.join(models_dir, file)
    if os.path.exists(path):
        print(f"\n--- Inspecting {file} ---")
        obj = None
        try:
            with open(path, 'rb') as f:
                obj = pickle.load(f)
            print("Loaded with pickle")
        except Exception as e:
            print(f"Pickle load error: {e}")
            try:
                obj = joblib.load(path)
                print("Loaded with joblib")
            except Exception as e2:
                print(f"Joblib load error: {e2}")
        
        if obj is not None:
            print(f"Type: {type(obj)}")
            if hasattr(obj, 'feature_names_in_'):
                print(f"Features: {obj.feature_names_in_}")
            elif hasattr(obj, 'n_features_in_'):
                print(f"Number of features: {obj.n_features_in_}")
            
            if 'scaler' in file:
                if hasattr(obj, 'mean_'):
                    print(f"Scaler has mean_ for {len(obj.mean_)} features")
    else:
        print(f"{file} not found.")

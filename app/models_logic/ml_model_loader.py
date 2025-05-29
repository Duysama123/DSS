# health_diagnosis_expert_system/app/models_logic/ml_model_loader.py

import joblib
import os
import pandas as pd
import numpy as np

# Define base directory to locate model and data files相對
# Assuming ml_model_loader.py is in app/models_logic/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_DIR = os.path.join(BASE_DIR, 'models')
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed') # Path to processed data

ml_model = None
label_encoder = None
MODEL_LOADED = False

# This list will hold the feature column names in the correct order for the model
# It should be populated by load_ml_components()
FEATURE_COLUMNS = []


def load_ml_components(symptoms_list_from_routes=None): # Added parameter
    global ml_model, label_encoder, MODEL_LOADED, FEATURE_COLUMNS
    
    if MODEL_LOADED:
        return

    # Update with your actual best model file name if different
    model_path = os.path.join(MODEL_DIR, 'logistic_regression_primitive_model.pkl') # OR 'logistic_regression_primitive_model.pkl'
    encoder_path = os.path.join(MODEL_DIR, 'disease_label_encoder_filtered.pkl')
    
    # Attempt to load feature column names from X_train_filtered.csv (preferred method)
    x_train_cols_path = os.path.join(PROCESSED_DATA_DIR, 'X_train_filtered.csv')
    
    try:
        if os.path.exists(x_train_cols_path):
            df_train_cols = pd.read_csv(x_train_cols_path, nrows=0) # Read only header
            FEATURE_COLUMNS = df_train_cols.columns.tolist()
            print(f"Successfully loaded {len(FEATURE_COLUMNS)} feature column names from: {x_train_cols_path}")
        elif symptoms_list_from_routes: # Fallback to list passed from routes.py
            FEATURE_COLUMNS = symptoms_list_from_routes
            print(f"Using {len(FEATURE_COLUMNS)} feature column names passed from routes.py (fallback).")
        else:
            print(f"CRITICAL WARNING: Could not find {x_train_cols_path} and no fallback symptom list provided. FEATURE_COLUMNS will be empty.")
            FEATURE_COLUMNS = [] 
    except Exception as e:
        print(f"Error loading feature column names: {e}")
        FEATURE_COLUMNS = []


    try:
        if os.path.exists(model_path):
            ml_model = joblib.load(model_path)
            print(f"ML Model loaded successfully from: {model_path}")
        else:
            print(f"ERROR: Model file not found at {model_path}")
            ml_model = None # Ensure it's None if not loaded

        if os.path.exists(encoder_path):
            label_encoder = joblib.load(encoder_path)
            print(f"LabelEncoder loaded successfully from: {encoder_path}")
        else:
            print(f"ERROR: LabelEncoder file not found at {encoder_path}")
            label_encoder = None # Ensure it's None if not loaded
        
        if ml_model and label_encoder and FEATURE_COLUMNS: # Check if FEATURE_COLUMNS is also populated
            MODEL_LOADED = True
            print("ML components are ready.")
        else:
            MODEL_LOADED = False # Explicitly set to False
            print("Failed to load all necessary ML components (model, encoder, or feature columns).")

    except Exception as e:
        print(f"Error during loading of model or encoder: {e}")
        MODEL_LOADED = False


def predict_disease_ml(symptom_input_dict):
    """
    Predicts disease based on an input dictionary of symptoms.
    symptom_input_dict: e.g., {'symptom_A': 1, 'symptom_B': 0, ...}
                        or only symptoms present: {'symptom_A': 1, 'symptom_C': 1}
    """
    if not MODEL_LOADED:
        # Attempt to load components if not already loaded.
        # Pass None for symptoms_list_from_routes as this function is called at runtime,
        # initial_setup in routes.py should have already called load_ml_components with a list.
        # If called directly without initial_setup, FEATURE_COLUMNS might rely on X_train_filtered.csv.
        print("ML components not loaded. Attempting to load now (this might indicate an issue in app startup flow).")
        load_ml_components(symptoms_list_from_routes=None) 

    if not ml_model or not label_encoder or not FEATURE_COLUMNS:
        error_msg = "ML Model, LabelEncoder, or Feature Columns not loaded. Cannot make predictions."
        print(f"ERROR in predict_disease_ml: {error_msg}")
        return [{"error": error_msg}]

    # Create a one-row DataFrame with the correct columns and order, initialized to 0
    try:
        input_vector = pd.DataFrame(0, index=[0], columns=FEATURE_COLUMNS)
    except Exception as e:
        error_msg = f"Error creating input vector DataFrame. FEATURE_COLUMNS might be problematic. Error: {e}"
        print(f"ERROR in predict_disease_ml: {error_msg}")
        return [{"error": error_msg}]
    
    # Set 1 for symptoms present in the input_dict
    for symptom, value in symptom_input_dict.items():
        if symptom in input_vector.columns:
            input_vector.loc[0, symptom] = value # Typically 1 if symptom is present
        # else:
        #     print(f"Warning: Symptom '{symptom}' from input is not in the model's feature list.")

    try:
        # Attempt to get probabilities
        # Ensure your model was trained with probability=True or supports predict_proba
        # For LogisticRegression, probability=True is not a direct param; it's inherent.
        # For SVC, you need to set probability=True during training.
        # If you used joblib.dump(best_estimator_from_GridSearchCV), it should retain this.
        if hasattr(ml_model, 'predict_proba'):
            probabilities = ml_model.predict_proba(input_vector)[0]
            
            # Get top N predictions (e.g., top 3)
            # Ensure there are at least N classes in the model
            num_classes_in_model = len(ml_model.classes_)
            top_n = min(3, num_classes_in_model) # Get top 3 or fewer if less than 3 classes

            top_n_indices = np.argsort(probabilities)[-top_n:][::-1]
            
            results = []
            for i in top_n_indices:
                # ml_model.classes_ gives the original encoded labels
                disease_name = label_encoder.inverse_transform([ml_model.classes_[i]])[0]
                prob = probabilities[i]
                if prob > 0.005: # Display if probability is somewhat significant
                    results.append({'disease': disease_name, 'probability': f"{prob*100:.2f}%"})
            
            if not results and num_classes_in_model > 0: # If all probabilities were too low but there are classes
                top_index = np.argmax(probabilities)
                disease_name = label_encoder.inverse_transform([ml_model.classes_[top_index]])[0]
                prob = probabilities[top_index]
                results.append({'disease': disease_name, 'probability': f"{prob*100:.2f}% (highest, but low overall confidence)"})
            elif not results and num_classes_in_model == 0:
                results.append({'info': 'No classes found in the model.'})


            return results if results else [{"info": "No confident predictions from ML model."}]

        else: # Fallback to predict() if predict_proba is not available
            print("Model does not support predict_proba. Using predict() instead.")
            prediction_encoded = ml_model.predict(input_vector)
            disease_name = label_encoder.inverse_transform(prediction_encoded)[0]
            return [{'disease': disease_name, 'probability': 'N/A (predict only)'}]
            
    except Exception as e:
        print(f"Error during ML prediction: {e}")
        return [{"error": f"Error during ML prediction: {str(e)}"}]

# Optional: Call load_ml_components() when the module is first imported
# This ensures components are loaded when the app starts if this module is imported.
# However, it's better to control this الصين from initial_setup in routes.py to pass parameters.
# load_ml_components() 
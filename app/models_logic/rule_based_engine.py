# health_diagnosis_expert_system/app/models_logic/rule_based_engine.py
import json
import os

# Điều chỉnh đường dẫn này cho chính xác
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Đặt tên file luật của bạn ở đây
RULES_FILE_NAME = 'flexible_rules_from_DiseaseAndSymptoms.csv.json' 
RULES_FILE_PATH = os.path.join(BASE_DIR, 'data', 'knowledge_base', RULES_FILE_NAME)

RULES = []
RULES_LOADED = False

def load_rules_from_file():
    global RULES, RULES_LOADED
    if RULES_LOADED:
        return

    try:
        if not os.path.exists(os.path.dirname(RULES_FILE_PATH)):
            os.makedirs(os.path.dirname(RULES_FILE_PATH), exist_ok=True) # Tạo thư mục nếu chưa có

        if os.path.exists(RULES_FILE_PATH):
            with open(RULES_FILE_PATH, 'r', encoding='utf-8') as f:
                RULES = json.load(f)
            RULES_LOADED = True
            print(f"Successfully loaded {len(RULES)} rules from: {RULES_FILE_PATH}")
        else:
            print(f"ERROR: Rules file not found at {RULES_FILE_PATH}. Rule engine will have no rules.")
            RULES = []
            RULES_LOADED = False # Đảm bảo là False nếu không tải được
            
    except json.JSONDecodeError:
        print(f"ERROR: Rules file {RULES_FILE_PATH} is not in a valid JSON format.")
        RULES = []
        RULES_LOADED = False
    except Exception as e:
        print(f"An unexpected error occurred while loading rules: {e}")
        RULES = []
        RULES_LOADED = False

def apply_rules_from_file(symptom_vector_dict):
    if not RULES_LOADED:
        # Cố gắng tải lại một lần nếu chưa được tải (có thể không cần thiết nếu initial_setup gọi)
        print("Rules not loaded. Attempting to load now (this might indicate an issue in app startup flow).")
        load_rules_from_file() 
    
    if not RULES: # Kiểm tra lại sau khi có thể đã thử tải lại
        print("No rules available to apply.")
        return [], [], []

    triggered_diagnoses = []
    triggered_explanations = []
    triggered_confidences = []

    for rule in RULES:
        conditions_met = False

        if "if_symptoms_list" in rule and "min_symptoms_match" in rule:
            symptoms_to_check = rule.get("if_symptoms_list", [])
            min_match_count = rule.get("min_symptoms_match", 1)
            matched_symptoms_count = 0
            for symptom_in_rule in symptoms_to_check:
                if symptom_vector_dict.get(symptom_in_rule) == 1:
                    matched_symptoms_count += 1
            if matched_symptoms_count >= min_match_count:
                conditions_met = True
        
        elif "if_symptoms" in rule: # Cấu trúc luật cũ (AND tất cả)
            all_simple_conditions_met = True
            if_conditions_simple = rule.get('if_symptoms', {})
            if not if_conditions_simple:
                all_simple_conditions_met = False
            for symptom, required_value in if_conditions_simple.items():
                if symptom_vector_dict.get(symptom, 0) != required_value:
                    all_simple_conditions_met = False
                    break
            if all_simple_conditions_met:
                conditions_met = True
        
        # (Tùy chọn) Xử lý if_symptoms_must_have
        if conditions_met and "if_symptoms_must_have" in rule:
            must_have_conditions = rule.get("if_symptoms_must_have", {})
            for symptom, required_value in must_have_conditions.items():
                if symptom_vector_dict.get(symptom, 0) != required_value:
                    conditions_met = False
                    break
        
        if conditions_met:
            if 'then_disease' in rule:
                triggered_diagnoses.append(rule['then_disease'])
            elif 'then_alert' in rule:
                triggered_diagnoses.append(f"ALERT: {rule['then_alert']}")
            
            triggered_explanations.append(rule.get('explanation', 'No explanation provided for this rule.'))
            triggered_confidences.append(rule.get('confidence', 0.5)) # Mặc định nếu không có

    return triggered_diagnoses, triggered_explanations, triggered_confidences

# Không cần tự động gọi load_rules_from_file() ở đây nữa,
# việc này sẽ được thực hiện trong initial_setup của routes.py
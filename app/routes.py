from flask import render_template, request, redirect, url_for,session, jsonify # jsonify có thể chưa dùng đến ngay
from datetime import datetime # Để lưu thời gian chẩn đoán
from app import app
import pandas as pd
import os
import json # <<<< THÊM DÒNG NÀY
import re

# Thêm vào đầu file routes.py
import requests
import urllib.parse # Để xử lý encoding tên bệnh cho URL

# Import các module logic
from .models_logic import ml_model_loader
from .models_logic import nlp_processor # Import NLP processor
from .models_logic.rule_based_engine import apply_rules_from_file, load_rules_from_file as load_rb_rules

# Thêm định nghĩa biến mặc định ở đây
DEFAULT_USERNAME = "user"
DEFAULT_PASSWORD = "password"

def get_wikipedia_info(disease_name_standardized):
    """
    Lấy thông tin tóm tắt và link từ Wikipedia cho một bệnh.
    disease_name_standardized: Tên bệnh đã được chuẩn hóa (ví dụ: "common cold", "seasonal allergies")
    """
    session = requests.Session()
    api_url = "https://en.wikipedia.org/w/api.php" # API tiếng Anh

    # Tên bệnh để tìm kiếm và tạo URL Wikipedia
    search_term = disease_name_standardized.replace('_', ' ') # Đảm bảo dùng khoảng trắng
    
    # Bước 1: Tìm kiếm trang Wikipedia tương ứng với tên bệnh để lấy title chính xác
    params_search = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": search_term,
        "srlimit": 1, # Chỉ lấy kết quả tìm kiếm phù hợp nhất
        "utf8": 1
    }
    
    page_title = None
    try:
        response_search = session.get(url=api_url, params=params_search, timeout=10)
        response_search.raise_for_status() # Kiểm tra lỗi HTTP
        data_search = response_search.json()
        
        if data_search.get("query", {}).get("search"):
            page_title = data_search["query"]["search"][0]["title"]
            print(f"WIKI API - Found page title: {page_title} for search: {search_term}")
        else:
            print(f"WIKI API - No page title found for search: {search_term}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"WIKI API - Error during search request: {e}")
        return None
    except ValueError as e: # Lỗi JSONDecodeError
        print(f"WIKI API - Error decoding JSON from search: {e}")
        return None

    if not page_title:
        return None

    # Bước 2: Lấy phần giới thiệu (extract/intro) của trang đã tìm được
    params_extract = {
        "action": "query",
        "format": "json",
        "titles": page_title,
        "prop": "extracts",
        "exintro": True,       # Lấy phần giới thiệu
        "explaintext": True,   # Lấy dưới dạng văn bản thuần (loại bỏ HTML)
        "redirects": 1,        # Tự động theo các trang redirect
        "utf8": 1
    }

    try:
        response_extract = session.get(url=api_url, params=params_extract, timeout=10)
        response_extract.raise_for_status()
        data_extract = response_extract.json()
        
        pages = data_extract.get("query", {}).get("pages", {})
        if not pages:
            print(f"WIKI API - No pages found in extract response for title: {page_title}")
            return None

        page_id = list(pages.keys())[0] # Lấy page ID (thường là số, hoặc -1 nếu không tìm thấy)
        
        if page_id != "-1" and "extract" in pages[page_id] and pages[page_id]["extract"]:
            summary = pages[page_id]["extract"]
            # Giới hạn độ dài tóm tắt một cách đơn giản
            summary_sentences = summary.split('.')
            # Lấy tối đa 3 câu đầu hoặc ít hơn nếu tóm tắt ngắn
            num_sentences_to_take = min(3, len(summary_sentences))
            short_summary = ". ".join(summary_sentences[:num_sentences_to_take])
            if num_sentences_to_take > 0 and not short_summary.endswith('.'): # Đảm bảo kết thúc bằng dấu chấm nếu có nội dung
                short_summary += "."
            
            # Tạo URL Wikipedia đầy đủ
            wiki_page_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(page_title.replace(' ', '_'))}"
            
            return {
                "source": "Wikipedia",
                "title": page_title,
                "summary": short_summary if short_summary else "No summary available.",
                "url": wiki_page_url
            }
        else:
            print(f"WIKI API - No extract found for page_id: {page_id}, title: {page_title}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"WIKI API - Error during extract request: {e}")
        return None
    except ValueError as e: # Lỗi JSONDecodeError
        print(f"WIKI API - Error decoding JSON from extract: {e}")
        return None
def normalize_disease_name_for_details_key(raw_name):
    if not raw_name:
        return None
    name_part = raw_name.split(' (')[0] # Loại bỏ phần trong ngoặc
    name_part = name_part.lower()       # Chuyển về chữ thường
    name_part = name_part.replace('-', ' ') # Thay gạch ngang bằng khoảng trắng trước
    name_part = re.sub(r'[^\w\s]', '', name_part) # Loại bỏ các ký tự đặc biệt khác (giữ lại chữ, số, khoảng trắng)
    name_part = re.sub(r'\s+', '_', name_part.strip()) # Thay thế một hoặc nhiều khoảng trắng bằng một gạch dưới
    return name_part

# Biến toàn cục để lưu danh sách triệu chứng cho UI (nếu vẫn muốn hiển thị checkbox làm fallback/debug)
# Hoặc chỉ để biết các triệu chứng mà hệ thống có thể xử lý
SYMPTOMS_AVAILABLE_FOR_UI = [] 
DISEASE_DETAILS_DATA = {} # Biến toàn cục để lưu trữ thông tin chi tiết bệnh

def initial_setup():
    global SYMPTOMS_AVAILABLE_FOR_UI, DISEASE_DETAILS_DATA # Thêm DISEASE_DETAILS_DATA

    print("--- Starting Initial Setup ---")

    # 1. Tải các thành phần ML (bao gồm FEATURE_COLUMNS)
    # Truyền None ban đầu vì chúng ta muốn ml_model_loader ưu tiên tải từ file X_train_filtered.csv
    ml_model_loader.load_ml_components(symptoms_list_from_routes=None)

    if ml_model_loader.FEATURE_COLUMNS:
        SYMPTOMS_AVAILABLE_FOR_UI = sorted(ml_model_loader.FEATURE_COLUMNS)
        print(f"Successfully initialized SYMPTOMS_AVAILABLE_FOR_UI from ML model features ({len(SYMPTOMS_AVAILABLE_FOR_UI)} symptoms).")
        
        # 2. Khởi tạo NLP Processor SAU KHI FEATURE_COLUMNS đã có
        print("\nLoading NLP Lexicon and known symptoms...")
        # Xác định đường dẫn đến file lexicon từ thư mục gốc của dự án
        current_file_dir_of_routes = os.path.dirname(os.path.abspath(__file__)) # D:\health_dss\app
        project_root_dir = os.path.dirname(current_file_dir_of_routes)         # D:\health_dss

        lexicon_file_name = "your_english_symptom_lexicon.json" # Đảm bảo tên file này đúng
        lexicon_full_path = os.path.join(project_root_dir, 'data', 'knowledge_base', lexicon_file_name)
        print(f"DEBUG ROUTES.PY - lexicon_full_path BEFORE CALL: '{lexicon_full_path}'") # Dòng print này
        
        nlp_processor.load_lexicon_and_known_symptoms(
            feature_columns_from_model=ml_model_loader.FEATURE_COLUMNS,
            lexicon_file_path=lexicon_full_path
        )
    else:
        print("CRITICAL ERROR: ml_model_loader.FEATURE_COLUMNS is empty. Cannot proceed with NLP or ML setup.")
        # Trong trường hợp này, SYMPTOMS_AVAILABLE_FOR_UI có thể thử tải từ raw_data_file_path như code cũ của bạn
        # nhưng đó chỉ là giải pháp tạm thời và không đảm bảo khớp với model.
        # Tốt nhất là đảm bảo X_train_filtered.csv có và được đọc đúng.
        try:
            raw_data_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'synthetic_disease_symptoms.csv')
            if os.path.exists(raw_data_file_path):
                df_for_columns = pd.read_csv(raw_data_file_path, nrows=1)
                SYMPTOMS_AVAILABLE_FOR_UI = sorted([col for col in df_for_columns.columns if col.lower() != 'disease'])
                print(f"Fallback: Loaded {len(SYMPTOMS_AVAILABLE_FOR_UI)} symptoms from raw CSV for UI.")
            else: SYMPTOMS_AVAILABLE_FOR_UI = ["fallback_symptom_1", "fallback_symptom_2"]
        except Exception as e:
            print(f"Error in fallback symptom loading: {e}")
            SYMPTOMS_AVAILABLE_FOR_UI = ["error_symptom_1"]


    # 3. Tải luật Rule-Based
    print("\nLoading Rule-Based Engine rules...")
    load_rb_rules()
    
     # 4. Tải thông tin chi tiết bệnh
    print("\nLoading Disease Details...")
    try:
        # Sử dụng CÙNG project_root_dir cho disease_details
        details_file_path = os.path.join(project_root_dir, 'data', 'knowledge_base', 'disease_details.json')
        
        if os.path.exists(details_file_path):
            with open(details_file_path, 'r', encoding='utf-8') as f:
                DISEASE_DETAILS_DATA = json.load(f)
            print(f"Successfully loaded {len(DISEASE_DETAILS_DATA)} disease details from {details_file_path}.")
        else:
            print(f"WARNING: Disease details file not found at {details_file_path}.")
    except Exception as e:
        print(f"ERROR loading disease details: {e}")
    print("\n--- Initial Setup Complete ---")

initial_setup() # Chạy một lần khi ứng dụng khởi động



@app.route('/')
def index():
    if 'user_id' in session:
        # Lấy lịch sử chẩn đoán từ session, mặc định là list rỗng nếu chưa có
        user_history = session.get('diagnosis_history', [])
        # Lấy 2 mục lịch sử gần nhất
        recent_activity = user_history[-2:] # Lấy 2 mục cuối cùng (gần nhất)
        # Truyền dữ liệu hoạt động gần đây đến template home_loggedin.html
        return render_template('home_loggedin.html', recent_activity=recent_activity)
    return render_template('home_public.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Biến để lưu thông báo lỗi
    error = None
    print(f"DEBUG LOGIN - Request Method: {request.method}") # Debug print
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(f"DEBUG LOGIN - Received Username: '{username}'") # Debug print
        print(f"DEBUG LOGIN - Received Password: '{password}'") # Debug print
        print(f"DEBUG LOGIN - Expected Username: '{DEFAULT_USERNAME}'") # Debug print
        print(f"DEBUG LOGIN - Expected Password: '{DEFAULT_PASSWORD}'") # Debug print

        # Kiểm tra thông tin đăng nhập
        if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
            print("DEBUG LOGIN - Credentials Match!") # Debug print
            # Đăng nhập thành công
            session['user_id'] = username # Lưu ID người dùng vào session (có thể dùng username làm tạm)
            session['username'] = username # Lưu tên người dùng vào session
            print(f"DEBUG LOGIN - Session User ID Set: {session.get('user_id')}") # Debug print
            print(f"User '{username}' logged in successfully.")
            # Chuyển hướng đến trang AI Diagnosis
            return redirect(url_for('ai_diagnosis'))
        else:
            print("DEBUG LOGIN - Credentials Mismatch.") # Debug print
            # Đăng nhập thất bại
            error = 'Invalid Credentials. Please try again.'
            print(f"Failed login attempt for username: '{username}'")

    # Render trang login.html, truyền thông báo lỗi (nếu có)
    return render_template('login.html', error=error)

@app.route('/before-login')
def before_login():
    return render_template('before-login.html')

@app.route('/ai-diagnosis')
def ai_diagnosis():
    # Removed login check to allow public access
    # if 'user_id' not in session:
    #     return redirect(url_for('login'))
    return render_template('ai_diagnosis.html', symptoms_list=SYMPTOMS_AVAILABLE_FOR_UI)

@app.route('/ai-diagnosis-results')
def ai_diagnosis_results():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('ai_diagnosis_results.html')

@app.route('/diagnosis-history')
def diagnosis_history():
    if 'user_id' not in session:
        # Nếu chưa đăng nhập, chuyển hướng về trang login
        return redirect(url_for('login'))
    
    # Lấy lịch sử chẩn đoán từ session, mặc định là list rỗng nếu chưa có
    user_history = session.get('diagnosis_history', [])
    
    # Truyền dữ liệu lịch sử đến template
    return render_template('diagnosis_history.html', history_data=user_history)

@app.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('settings.html')

@app.route('/support')
def support():
    return render_template('support.html')

# ... other imports and code ...

@app.route('/chatbot', methods=['POST'])
def chatbot():
    print("DEBUG: Chatbot endpoint hit!") # Add this line
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'response': 'Error: No message provided.'}), 400

    # ... rest of the chatbot function code ...

    # Replace with your actual OpenRouter API key
    OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY") # It's recommended to use environment variables
    if not OPENROUTER_API_KEY:
         # Using a placeholder message for now. Replace with actual API call.
         print("OPENROUTER_API_KEY not set. Using placeholder response.")
         bot_response = f"You said: {user_message}. (OpenRouter API key not configured)"
    else:
        # --- Placeholder for OpenRouter API call ---
        # You will need to replace this section with code to call the OpenRouter API.
        # Example using requests library:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "meta-llama/llama-3-8b-instruct",  # Specify Llama 3 8B model
                    "messages": [{"role": "user", "content": user_message}],
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            )
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            api_response_data = response.json()
            # Adjust according to the actual API response structure
            bot_response = api_response_data['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            print(f"Error calling OpenRouter API: {e}")
            bot_response = "Sorry, I couldn't connect to the AI service right now."
        # --- End Placeholder ---

    return jsonify({'response': bot_response})

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    # TODO: Redirect to login page
    # CORRECTED: Redirect to the login page after logging out
    return redirect(url_for('login'))

@app.route('/diagnose', methods=['POST'])
def diagnose():
    if request.method == 'POST':
        user_text_input = request.form.get('symptom_description', '').strip()
        selected_symptoms_from_checkbox = request.form.getlist('symptoms_selected')
        
        print(f"DEBUG ROUTES.PY - User Text Input: '{user_text_input}'")
        print(f"DEBUG ROUTES.PY - Checkbox values received: {selected_symptoms_from_checkbox}")

        processed_symptoms_list = []
        if user_text_input:
            processed_symptoms_list = nlp_processor.extract_symptoms_from_text_english(user_text_input)
        if selected_symptoms_from_checkbox:
            valid_checkbox_symptoms = [symptom for symptom in selected_symptoms_from_checkbox if symptom in ml_model_loader.FEATURE_COLUMNS]
            for symptom in valid_checkbox_symptoms:
                if symptom not in processed_symptoms_list:
                    processed_symptoms_list.append(symptom)
        
        print(f"--- Final processed_symptoms_list for engines: {processed_symptoms_list} ---")

        if not processed_symptoms_list:
            # ... (xử lý lỗi input rỗng như cũ) ...
            results_payload = {
                "user_text_input": user_text_input or "N/A (Checkboxes may have been selected)",
                "extracted_symptoms_for_display": ["No valid symptoms were processed."],
                "error_message": "Please describe your symptoms or select valid symptoms from the list."
            }
            return render_template('results.html', title='Input Error', results_data=results_payload)

        symptom_input_for_engines = {
            symptom: 1 if symptom in processed_symptoms_list else 0 
            for symptom in ml_model_loader.FEATURE_COLUMNS
        }
        if not ml_model_loader.FEATURE_COLUMNS: # Kiểm tra lại ở đây
            print("ERROR: Model feature columns (ml_model_loader.FEATURE_COLUMNS) not loaded.")
            results_payload = { "user_text_input": user_text_input, "error_message": "System error: Model features not available."}
            return render_template('results.html', title='Diagnosis Error', results_data=results_payload)


        # --- Diagnosis Orchestrator Logic ---
        ml_results_raw = ml_model_loader.predict_disease_ml(symptom_input_for_engines)
        rb_diagnoses_raw, rb_explanations_raw, rb_confidences_raw = apply_rules_from_file(symptom_input_for_engines)

        orchestrated_results = []
        primary_disease_for_guidance = None
        source_of_primary_diagnosis = "No definitive source"

        if rb_diagnoses_raw:
            source_of_primary_diagnosis = "Rule-Based System"
            for i, disease_name in enumerate(rb_diagnoses_raw):
                disease_name_std = nlp_processor.standardize_name(disease_name) if hasattr(nlp_processor, 'standardize_name') else disease_name.lower().replace(' ','_')
                orchestrated_results.append({
                    "type": "rule", "disease": disease_name_std,
                    "confidence": f"{rb_confidences_raw[i]*100:.0f}%" if isinstance(rb_confidences_raw[i], float) else str(rb_confidences_raw[i]),
                    "explanation": rb_explanations_raw[i]
                })
                if not primary_disease_for_guidance and not disease_name.startswith("ALERT:"):
                    primary_disease_for_guidance = disease_name_std
        elif ml_results_raw and not any(res.get("error") for res in ml_results_raw):
            source_of_primary_diagnosis = "AI Model (Machine Learning)"
            for pred in ml_results_raw:
                if pred.get("disease"):
                    orchestrated_results.append({"type": "ml", "disease": pred['disease'], "probability": pred['probability']})
            if orchestrated_results:
                primary_disease_for_guidance = orchestrated_results[0]['disease']
        else:
            orchestrated_results.append({"info": "No specific diagnosis could be determined by AI or Rules."})

        # --- Process orchestrated_results for template details ---
        orchestrated_results_with_details = []

        if orchestrated_results:
            # Kiểm tra xem orchestrated_results có phải là list chứa dict không, và không phải là message info/error
            is_structured_results = isinstance(orchestrated_results, list) and \
                                    all(isinstance(item, dict) for item in orchestrated_results) and \
                                    not (orchestrated_results and (orchestrated_results[0].get('info') or orchestrated_results[0].get('error')))

            if is_structured_results:
                for item in orchestrated_results:
                    detail = {
                        'disease': item.get('disease', 'Unknown Disease'),
                        'type': item.get('type', 'unknown')
                    }
                    if item.get('type') == 'ml' and 'probability' in item:
                        try:
                            prob_str = str(item['probability']).strip('%').strip()
                            prob_numeric = float(prob_str)
                            # Giới hạn giá trị từ 0 đến 100 cho thanh bar
                            prob_numeric_capped = min(max(prob_numeric, 0.1), 100) # 0.1 để thanh luôn hiển thị 1 chút

                            detail['probability_display'] = f"{prob_numeric:.2f}"
                            detail['probability_numeric'] = prob_numeric_capped
                        except ValueError:
                            detail['probability_display'] = item['probability'] # Hiển thị nguyên gốc nếu không parse được
                            detail['probability_numeric'] = 0
                    elif item.get('type') == 'rule':
                        detail['confidence'] = item.get('confidence', 'N/A')
                        detail['explanation'] = item.get('explanation')

                    orchestrated_results_with_details.append(detail)
            # Nếu orchestrated_results là message info/error, không cần gán vào orchestrated_results_with_details
            # template sẽ tự xử lý phần `else` của `if results_data.orchestrated_results_with_details`

        # --- Lấy thông tin bổ sung (KHÔNG CÓ PRECAUTIONS NỮA) ---
        guidance_package = {"details": None, "wikipedia": None} # Bỏ "precautions"
        if primary_disease_for_guidance:
            print(f"ORCHESTRATOR: Primary diagnosis for guidance: {primary_disease_for_guidance}")
            
            # 1. Lấy Disease Details (giữ nguyên)
            normalized_key_for_details = normalize_disease_name_for_details_key(primary_disease_for_guidance)
            if normalized_key_for_details in DISEASE_DETAILS_DATA:
                guidance_package["details"] = DISEASE_DETAILS_DATA[normalized_key_for_details]
                if "display_name" not in guidance_package["details"]:
                     guidance_package["details"]["display_name"] = primary_disease_for_guidance.replace('_', ' ').title()

            # 2. Lấy Wikipedia Info (giữ nguyên)
            wiki_search_term = primary_disease_for_guidance.split(' (')[0].strip()
            guidance_package["wikipedia"] = get_wikipedia_info(wiki_search_term)

        results_payload = {
            "user_text_input": user_text_input if user_text_input else "N/A (Checkbox input might have been used)",
            "extracted_symptoms_for_display": processed_symptoms_list,
            "source_of_primary_diagnosis": source_of_primary_diagnosis,
            "orchestrated_results": orchestrated_results, # Vẫn truyền kết quả gốc để xử lý info/error
            "orchestrated_results_with_details": orchestrated_results_with_details, # Truyền list mới cho các card chi tiết
            "guidance_package": guidance_package # Giờ chỉ có details và wikipedia
        }
        
          # --- Lưu vào Lịch sử Session ---
        if 'diagnosis_history' not in session:
            session['diagnosis_history'] = []
        
        # Tạo một bản ghi lịch sử TÓM TẮT trước đó, giờ sẽ lưu ĐẦY ĐỦ hơn
        history_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_input_text": results_payload.get("user_text_input", "N/A"),
            "processed_symptoms": results_payload.get("extracted_symptoms_for_display", []),
            # Lưu kết quả tóm tắt chính (đã có)
            "primary_source": results_payload.get("source_of_primary_diagnosis"),
            "primary_diagnosis": None, # Sẽ được điền bên dưới
            "primary_confidence_or_probability": None, # Sẽ được điền bên dưới

            # >>> THÊM CÁC TRƯỜNG CHI TIẾT KHÁC <<< 
            "orchestrated_results_with_details": results_payload.get("orchestrated_results_with_details", []), # Lưu list chi tiết cho các card gợi ý
            "guidance_package": results_payload.get("guidance_package", {}) # Lưu package guidance và wikipedia
            # >>> KẾT THÚC THÊM <<<
        }

        # Lấy chẩn đoán chính để lưu vào lịch sử (giữ nguyên)
        orchestrated_results = results_payload.get("orchestrated_results", [])
        if orchestrated_results and orchestrated_results[0] and not orchestrated_results[0].get("info") and not orchestrated_results[0].get("error"):
            history_entry["primary_diagnosis"] = orchestrated_results[0].get("disease", "Unknown")
            if orchestrated_results[0].get("type") == "ml":
                 # Lấy giá trị numeric/display tùy cái nào có
                 primary_prob = orchestrated_results[0].get("probability_display") or orchestrated_results[0].get("probability")
                 history_entry["primary_confidence_or_probability"] = primary_prob
            elif orchestrated_results[0].get("type") == "rule":
                 history_entry["primary_confidence_or_probability"] = orchestrated_results[0].get("confidence")


        session['diagnosis_history'].append(history_entry)
        # Giới hạn số lượng mục lịch sử trong session (ví dụ: 10 mục gần nhất)
        if len(session['diagnosis_history']) > 10:
            session['diagnosis_history'] = session['diagnosis_history'][-10:]
        
        session.modified = True # Đảm bảo session được lưu

        return render_template('results.html', title='Diagnosis Results', results_data=results_payload)
    
    return redirect(url_for('index'))
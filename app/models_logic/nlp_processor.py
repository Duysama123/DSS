# health_diagnosis_expert_system/app/models_logic/nlp_processor.py
import re
import os
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer # Import cả hai để dễ chuyển đổi
from fuzzywuzzy import process

# --- Tải tài nguyên NLTK một lần khi module được import ---
# (Trong môi trường sản xuất, việc này nên được xử lý cẩn thận hơn,
# ví dụ như trong một script setup hoặc Dockerfile)
try:
    nltk.data.find('corpora/stopwords')
except LookupError: # Sử dụng LookupError thay vì nltk.downloader.DownloadError trực tiếp
    nltk.download('stopwords', quiet=True)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/wordnet') # Cần cho WordNetLemmatizer
except LookupError:
    nltk.download('wordnet', quiet=True)
try:
    nltk.data.find('corpora/omw-1.4') # Cần cho WordNetLemmatizer trong một số ngôn ngữ
except LookupError:
    nltk.download('omw-1.4', quiet=True)


# --- Biến toàn cục của module ---
SYMPTOM_LEXICON = {}
KNOWN_SYMPTOMS_SET = set()
STEMMER = PorterStemmer()
# # LEMMATIZER = WordNetLemmatizer()
STOP_WORDS = set(stopwords.words('english'))
NLP_PROCESSOR_INITIALIZED = False

# Đường dẫn cơ sở của module này (app/models_logic)
MODULE_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- ĐỊNH NGHĨA CÁC BIẾN ĐỂ TẠO ĐƯỜNG DẪN MẶC ĐỊNH CHO LEXICON ---
# 1. Xác định thư mục gốc của dự án (đi lên 2 cấp từ MODULE_BASE_DIR)
#    app/models_logic/ -> app/ -> health_diagnosis_expert_system/ (thư mục gốc)
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(MODULE_BASE_DIR))

# 2. Tên file lexicon mặc định
DEFAULT_LEXICON_FILE_NAME = "your_english_symptom_lexicon.json" # Đảm bảo tên này đúng

# 3. Tạo đường dẫn đầy đủ đến file lexicon mặc định
DEFAULT_LEXICON_PATH = os.path.join(PROJECT_ROOT_DIR, 'data', 'knowledge_base', DEFAULT_LEXICON_FILE_NAME)
# Đường dẫn này sẽ là ví dụ: D:\health_dss\data\knowledge_base\your_english_symptom_lexicon.json


# SỬA TÊN THAM SỐ Ở ĐÂY
def load_lexicon_and_known_symptoms(feature_columns_from_model, lexicon_file_path=DEFAULT_LEXICON_PATH):
    print(f"DEBUG NLP_PROCESSOR.PY - lexicon_file_path AT FUNCTION START: '{lexicon_file_path}'") # Dòng print này
    print(f"DEBUG NLP_PROCESSOR.PY - DEFAULT_LEXICON_PATH AT FUNCTION START: '{DEFAULT_LEXICON_PATH}'") # Dòng print này
    global SYMPTOM_LEXICON, KNOWN_SYMPTOMS_SET, NLP_PROCESSOR_INITIALIZED # Sửa LEXICON_LOADED thành NLP_PROCESSOR_INITIALIZED

    if NLP_PROCESSOR_INITIALIZED:
        return

    print("NLP: Attempting to load lexicon and known symptoms...")
    print(f"NLP: Using lexicon file path: {lexicon_file_path}") # In ra đường dẫn thực tế đang dùng

    # 1. Khởi tạo KNOWN_SYMPTOMS_SET
    if not feature_columns_from_model:
        print("NLP CRITICAL: feature_columns_from_model is empty or None. Cannot initialize NLP processor effectively.")
        NLP_PROCESSOR_INITIALIZED = False # Đảm bảo cờ này đúng
        return 
    
    KNOWN_SYMPTOMS_SET = set(feature_columns_from_model)
    print(f"NLP: Initialized with {len(KNOWN_SYMPTOMS_SET)} known standard symptoms from model features.")

    # 2. Tải Symptom Lexicon từ file JSON
    # actual_lexicon_path bây giờ chính là lexicon_file_path được truyền vào (hoặc giá trị mặc định của nó)
    actual_lexicon_path = lexicon_file_path 

    temp_lexicon = {}
    try:
        if os.path.exists(actual_lexicon_path):
            with open(actual_lexicon_path, 'r', encoding='utf-8') as f:
                temp_lexicon = json.load(f)
            print(f"NLP: Symptom Lexicon loaded with {len(temp_lexicon)} entries from {actual_lexicon_path}.")
        else:
            print(f"NLP WARNING: Symptom Lexicon file not found at {actual_lexicon_path}. Lexicon will only contain standard symptoms.")
            
    except json.JSONDecodeError:
        print(f"NLP ERROR: Symptom Lexicon file {actual_lexicon_path} is not valid JSON. Lexicon will be minimal.")
    except Exception as e:
        print(f"NLP ERROR: An unexpected error occurred while loading symptom lexicon: {e}. Lexicon will be minimal.")
    
    SYMPTOM_LEXICON = temp_lexicon

    # 3. Bổ sung SYMPTOM_LEXICON
    # ... (phần code bổ sung lexicon giữ nguyên) ...
    for std_symptom in KNOWN_SYMPTOMS_SET:
        if std_symptom not in SYMPTOM_LEXICON:
            SYMPTOM_LEXICON[std_symptom] = std_symptom
        symptom_with_spaces = std_symptom.replace('_', ' ')
        if symptom_with_spaces != std_symptom and symptom_with_spaces not in SYMPTOM_LEXICON:
            SYMPTOM_LEXICON[symptom_with_spaces] = std_symptom
            
    print(f"NLP: Symptom Lexicon final size after processing standard symptoms: {len(SYMPTOM_LEXICON)}")
    
    if KNOWN_SYMPTOMS_SET and SYMPTOM_LEXICON:
        NLP_PROCESSOR_INITIALIZED = True
        print("NLP: Lexicon and known symptoms successfully loaded and processed.")
    else:
        NLP_PROCESSOR_INITIALIZED = False # Đặt lại nếu có vấn đề
        print("NLP CRITICAL: Failed to properly initialize lexicon or known symptoms.")


# --- Hàm tiền xử lý văn bản ---
def preprocess_text_english(text_input):
    text = str(text_input).lower()
    text = re.sub(r'[^\w\s-]', '', text) # Loại bỏ dấu câu, giữ lại gạch nối
    
    tokens = nltk.word_tokenize(text)
    
    # Sử dụng Stemming hoặc Lemmatization
    # processed_tokens = [STEMMER.stem(word) for word in tokens if word not in STOP_WORDS and len(word) > 1]
    # Hoặc:
    lemmatizer = WordNetLemmatizer() # Tạo instance ở đây để không bị lỗi nếu dùng lần đầu
    processed_tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in STOP_WORDS and len(word) > 1]
    
    return processed_tokens, text # Trả về cả text gốc (đã lowercase, bỏ dấu câu) để khớp cụm từ

# --- Hàm trích xuất triệu chứng ---
def extract_symptoms_from_text_english(text_input):
    if not NLP_PROCESSOR_INITIALIZED: # Kiểm tra cờ khởi tạo tổng thể
        print("NLP ERROR: NLP Processor not initialized. Call load_lexicon_and_known_symptoms first with feature_columns.")
        # Cố gắng khởi tạo lại (cần feature_columns, có thể lấy từ ml_model_loader nếu đã tải)
        # from . import ml_model_loader # Tránh import vòng nếu có thể
        # if ml_model_loader.FEATURE_COLUMNS:
        #    load_lexicon_and_known_symptoms(ml_model_loader.FEATURE_COLUMNS)
        # else:
        #    return [] # Không thể làm gì nếu không có feature_columns
        # Cách tốt hơn là đảm bảo initial_setup trong routes.py gọi đúng thứ tự
        return []


    original_text_processed_for_phrases = str(text_input).lower()
    original_text_processed_for_phrases = " " + re.sub(r'[^\w\s-]', '', original_text_processed_for_phrases) + " "

    # Không cần tokens đã stem/lemma nếu chiến lược chính là khớp cụm từ với lexicon gốc
    # processed_tokens, _ = preprocess_text_english(text_input) 

    extracted_symptoms_standardized = set()

    # Sắp xếp các key của lexicon theo độ dài giảm dần để ưu tiên khớp cụm từ dài nhất
    sorted_lexicon_keys = sorted(SYMPTOM_LEXICON.keys(), key=len, reverse=True)

    text_to_search_iteratively = original_text_processed_for_phrases

    for phrase_key in sorted_lexicon_keys:
        # Sử dụng regex để khớp từ/cụm từ hoàn chỉnh, không phân biệt hoa thường (do đã lower case)
        # re.escape để xử lý các ký tự đặc biệt có thể có trong phrase_key
        pattern = r'\b' + re.escape(phrase_key) + r'\b'
        
        # Tìm tất cả các lần xuất hiện không chồng chéo của phrase_key
        # và thay thế chúng để không bị khớp lại bởi các key ngắn hơn là một phần của nó
        
        # Cách tiếp cận đơn giản: tìm và thêm, set() sẽ lo việc trùng lặp
        # Nếu muốn xử lý việc "tiêu thụ" cụm từ đã khớp để tránh khớp lại phần con:
        # Cần một vòng lặp while và thay thế trong text_to_search_iteratively
        
        if re.search(pattern, text_to_search_iteratively):
            standard_symptom = SYMPTOM_LEXICON[phrase_key]
            if standard_symptom in KNOWN_SYMPTOMS_SET:
                extracted_symptoms_standardized.add(standard_symptom)
                # print(f"NLP Phrase Match: '{phrase_key}' -> '{standard_symptom}'")
                # Để tránh khớp lại, bạn có thể thay thế cụm từ đã khớp bằng placeholder
                # text_to_search_iteratively = re.sub(pattern, " [MATCHED] ", text_to_search_iteratively, count=1) # Thay thế 1 lần


    # (Tùy chọn) Bước 2: Fuzzy matching cho các từ/cụm từ ngắn còn lại nếu không có nhiều kết quả
    if not extracted_symptoms_standardized and len(str(text_input).split()) <= 5 : # Chỉ fuzzy nếu ít từ và chưa có gì
        processed_tokens_for_fuzzy, _ = preprocess_text_english(text_input)
        for token in processed_tokens_for_fuzzy:
            if len(token) > 2: # Chỉ fuzzy các token có độ dài nhất định
                # Fuzzy match với các key trong SYMPTOM_LEXICON
                # Giới hạn choices để tăng tốc, ví dụ chỉ các key có độ dài tương tự
                potential_keys = [k for k in SYMPTOM_LEXICON.keys() if abs(len(k) - len(token)) <= 2 or token in k]
                if not potential_keys:
                    potential_keys = SYMPTOM_LEXICON.keys() # Fallback to all keys if no good candidates

                match, score = process.extractOne(token, potential_keys if potential_keys else [""]) # Handle empty potential_keys
                if score >= 88: # Ngưỡng cao cho fuzzy
                    standard_symptom = SYMPTOM_LEXICON[match]
                    if standard_symptom in KNOWN_SYMPTOMS_SET:
                        extracted_symptoms_standardized.add(standard_symptom)
                        # print(f"NLP Fuzzy Match: '{token}' ~ '{match}' -> '{standard_symptom}' (Score: {score})")


    print(f"NLP - Input: \"{text_input}\"")
    final_symptoms = list(extracted_symptoms_standardized)
    print(f"NLP - Extracted standardized symptoms: {final_symptoms}")
    return final_symptoms
import pandas as pd
import os
import json

# --- CẤU HÌNH ĐƯỜNG DẪN ---
# Đường dẫn tương đối từ vị trí của script này (thư mục gốc dự án)
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Thư mục gốc của dự án
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'knowledge_base') # Nơi lưu file output

# Tên file input chứa header cột (X_train đã xử lý)
X_TRAIN_CSV_FILENAME = 'X_train_filtered.csv'

# Tên file output cho danh sách triệu chứng chuẩn
STANDARD_SYMPTOMS_TXT_FILENAME = 'standard_feature_columns.txt'
STANDARD_SYMPTOMS_JSON_FILENAME = 'standard_feature_columns.json'


def extract_and_save_feature_columns():
    """
    Đọc header từ file X_train_filtered.csv để lấy danh sách FEATURE_COLUMNS
    và lưu vào file text và JSON.
    """
    feature_columns = []
    x_train_full_path = os.path.join(PROCESSED_DATA_DIR, X_TRAIN_CSV_FILENAME)

    print(f"Đang cố gắng đọc header từ: {x_train_full_path}")

    try:
        if os.path.exists(x_train_full_path):
            df_train_cols = pd.read_csv(x_train_full_path, nrows=0) # Chỉ đọc header
            feature_columns = sorted(df_train_cols.columns.tolist()) # Sắp xếp để nhất quán
            print(f"Đã trích xuất thành công {len(feature_columns)} tên cột đặc trưng (triệu chứng).")
        else:
            print(f"LỖI: Không tìm thấy file '{X_TRAIN_CSV_FILENAME}' tại '{PROCESSED_DATA_DIR}'.")
            print("Hãy đảm bảo bạn đã chạy notebook tiền xử lý và lưu file này.")
            return
    except Exception as e:
        print(f"Lỗi khi đọc file CSV: {e}")
        return

    if not feature_columns:
        print("Không trích xuất được cột đặc trưng nào.")
        return

    # Tạo thư mục output nếu chưa có
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- Lưu vào file .txt (mỗi triệu chứng một dòng) ---
    output_txt_path = os.path.join(OUTPUT_DIR, STANDARD_SYMPTOMS_TXT_FILENAME)
    try:
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            for symptom in feature_columns:
                f.write(f"{symptom}\n")
        print(f"Đã lưu danh sách triệu chứng chuẩn vào: {output_txt_path}")
    except Exception as e:
        print(f"Lỗi khi lưu file TXT: {e}")

    # --- Lưu vào file .json (danh sách các triệu chứng) ---
    output_json_path = os.path.join(OUTPUT_DIR, STANDARD_SYMPTOMS_JSON_FILENAME)
    try:
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(feature_columns, f, indent=2, ensure_ascii=False)
        print(f"Đã lưu danh sách triệu chứng chuẩn vào: {output_json_path}")
    except Exception as e:
        print(f"Lỗi khi lưu file JSON: {e}")


if __name__ == "__main__":
    extract_and_save_feature_columns()
import joblib
import os

def main():
    # Xác định đường dẫn đến thư mục chứa model và encoder
    # Giả sử script này nằm trong thư mục gốc của dự án HEALTH_DSS
    # Nếu bạn đặt script này ở nơi khác, hãy điều chỉnh đường dẫn tương đối cho phù hợp
    project_root_dir = os.path.dirname(os.path.abspath(__file__)) # Hoặc đặt cố định nếu script ở 1 nơi
    # Nếu script này nằm trong D:\health_dss\scripts\ thì project_root_dir là D:\health_dss\scripts\
    # Nếu script này nằm trong D:\health_dss\ thì project_root_dir là D:\health_dss\
    
    # Điều chỉnh đường dẫn này cho đúng với vị trí file .pkl của bạn so với script
    # Ví dụ, nếu script view_encoder_classes.py nằm trong thư mục gốc HEALTH_DSS:
    models_dir = os.path.join(project_root_dir, 'models') 
    # Nếu script nằm trong thư mục con 'scripts':
    # models_dir = os.path.join(os.path.dirname(project_root_dir), 'models')


    encoder_filename = 'disease_label_encoder_filtered.pkl'
    encoder_path = os.path.join(models_dir, encoder_filename)

    print(f"Attempting to load LabelEncoder from: {encoder_path}")

    if not os.path.exists(encoder_path):
        print(f"ERROR: LabelEncoder file not found at {encoder_path}")
        print("Please ensure the path is correct and the file exists.")
        return

    try:
        disease_label_encoder = joblib.load(encoder_path)
        print("LabelEncoder loaded successfully.")

        if hasattr(disease_label_encoder, 'classes_'):
            disease_classes = list(disease_label_encoder.classes_)
            print("\n--- List of Disease Classes Encoded ---")
            for i, disease_name in enumerate(disease_classes):
                print(f"{i + 1}. {disease_name}")
            
            print(f"\nTotal number of disease classes: {len(disease_classes)}")

            # (Tùy chọn) Lưu danh sách ra file text để dễ xem và sử dụng
            output_file_path = os.path.join(project_root_dir, 'disease_classes_from_encoder.txt')
            with open(output_file_path, 'w', encoding='utf-8') as f:
                for disease_name in disease_classes:
                    f.write(f"{disease_name}\n")
            print(f"\nList of disease classes also saved to: {output_file_path}")

        else:
            print("ERROR: The loaded object does not appear to be a scikit-learn LabelEncoder (missing 'classes_' attribute).")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
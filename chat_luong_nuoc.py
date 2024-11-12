import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from tkinter import *
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

# Đọc dữ liệu và tiền xử lý
def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        global data
        data = pd.read_csv(file_path)
        messagebox.showinfo("File Loaded", "Data loaded successfully!")
    else:
        messagebox.showwarning("No File", "Please select a file.")

def preprocess_data():
    global X, y
    data.dropna(inplace=True)  # Loại bỏ các dòng có giá trị thiếu
    X = data.drop('Potability', axis=1)  # Các cột đặc trưng
    y = data['Potability']  # Cột mục tiêu
    messagebox.showinfo("Preprocessing", "Data preprocessed successfully!")

# Huấn luyện mô hình
def train_model():
    global model, X_train, X_test, y_train, y_test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    messagebox.showinfo("Training", f"Model trained with accuracy: {acc * 100:.2f}%")

# Kiểm tra kết quả huấn luyện
def evaluate_model():
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    plt.matshow(cm, cmap='coolwarm')
    plt.title("Confusion Matrix")
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()
    report = classification_report(y_test, y_pred)
    messagebox.showinfo("Evaluation", report)

# Dự đoán chất lượng nước mới
def predict_quality():
    try:
        input_data = [
            float(entry_pH.get()), float(entry_Hardness.get()), float(entry_Solids.get()),
            float(entry_Chloramines.get()), float(entry_Sulfate.get()), float(entry_Conductivity.get()),
            float(entry_OrganicCarbon.get()), float(entry_Trihalomethanes.get()), float(entry_Turbidity.get())
        ]
        prediction = model.predict([input_data])[0]
        result = "Drinkable" if prediction == 1 else "Not Drinkable"
        messagebox.showinfo("Prediction Result", f"The water is: {result}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Giao diện Tkinter
root = Tk()
root.title("Water Quality Prediction")
root.geometry("500x400")

# Nút chọn file
Button(root, text="Load Data", command=load_data).pack(pady=10)

# Nút tiền xử lý
Button(root, text="Preprocess Data", command=preprocess_data).pack(pady=10)

# Nút huấn luyện mô hình
Button(root, text="Train Model", command=train_model).pack(pady=10)

# Nút kiểm tra mô hình
Button(root, text="Evaluate Model", command=evaluate_model).pack(pady=10)

# Phần nhập dữ liệu
Label(root, text="Enter water parameters:").pack(pady=10)
entry_pH = Entry(root)
entry_Hardness = Entry(root)
entry_Solids = Entry(root)
entry_Chloramines = Entry(root)
entry_Sulfate = Entry(root)
entry_Conductivity = Entry(root)
entry_OrganicCarbon = Entry(root)
entry_Trihalomethanes = Entry(root)
entry_Turbidity = Entry(root)

entries = [
    ("pH", entry_pH), ("Hardness", entry_Hardness), ("Solids", entry_Solids),
    ("Chloramines", entry_Chloramines), ("Sulfate", entry_Sulfate), ("Conductivity", entry_Conductivity),
    ("Organic Carbon", entry_OrganicCarbon), ("Trihalomethanes", entry_Trihalomethanes), ("Turbidity", entry_Turbidity)
]

for label_text, entry in entries:
    Label(root, text=label_text).pack()
    entry.pack()

# Nút dự đoán
Button(root, text="Predict Quality", command=predict_quality).pack(pady=20)

root.mainloop()

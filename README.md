# 🗑️ Garbage Classification Based on Image Data (CNN + Flask)

A deep learning project that uses **Computer Vision** and **Convolutional Neural Networks (CNN)** to classify garbage images into five categories: **glass**, **metal**, **paper**, **plastic**, and **trash**.  
This system is also deployed using a simple and interactive **Flask web application** with a clean UI.

---

## 📸 Demo

<img src="https://user-images.githubusercontent.com/your-image-demo.gif" width="700"/>

> _Upload an image and let the model classify your waste in real-time!_

---

## 📚 Table of Contents

- [📌 About the Project](#-about-the-project)
- [🗃️ Dataset](#️dataset)
- [🛠️ Technologies Used](#️technologies-used)
- [🧠 Model Training](#️model-training)
- [🌐 Flask Web App](#-flask-web-app)
- [⚙️ How to Run Locally](#️how-to-run-locally)
- [📷 Screenshots](#-screenshots)
- [📈 Result & Accuracy](#-result--accuracy)
- [📄 License](#-license)
- [🙋‍♂️ Author](#-author)

---

## 📌 About the Project

In daily life, a large volume of waste is generated from households and industries. Manual sorting is inefficient, error-prone, and hinders recycling.  
This project aims to **automate the waste classification** process using image-based input and a CNN model that recognizes visual patterns (shape, color, texture) in waste images. The result? A system that is **faster, more accurate, and scalable** for real-world applications.

---

## 🗃️ Dataset

We used the publicly available dataset from Kaggle:  
🔗 [Garbage Classification Dataset](https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification/data)

The dataset contains images grouped into the following categories:


📁 glass/
📁 metal/
📁 paper/
📁 plastic/
📁 trash/


---

## 🛠️ Technologies Used

- Python 3.10+
- TensorFlow / Keras
- Flask
- OpenCV
- NumPy & Pandas
- Matplotlib & Seaborn
- Scikit-learn

---

## 🧠 Model Training

The training pipeline consists of:

- ✅ Dataset loading and preprocessing
- ✅ Image resizing and normalization
- ✅ Exploratory Data Analysis (EDA)
- ✅ Data augmentation & oversampling
- ✅ CNN model design and training (3 phases)
- ✅ Evaluation with accuracy, loss curves, and confusion matrix

Example CNN architecture (simplified):


## 🌐 Flask Web App
The trained CNN model (final_model_33.h5) is deployed using a Flask web application with modular HTML templates and Bootstrap styling.

📦 static/uploads/       → Folder for uploaded images
📄 app.py                → Main Flask app script
📄 final_model_33.h5     → Trained CNN model
📄 requirements.txt      → Dependency list
📄 start.sh              → Script to run the app (optional)
📁 templates/
    ├─ index.html        → Homepage (upload form)
    ├─ picture.html      → Result page for image classification
    ├─ live_camera.html  → Live camera prediction page
    ├─ cek.html          → Combined camera + image UI
    └─ header.html       → Common navbar/header


## ▶️ Route Overview (app.py):
/ → Homepage for uploading images

/predict → Handles image classification

/picture → Displays uploaded image & result

/live_camera → Access webcam for live prediction

/cek → Combined interface (image + camera)

The app runs locally on port 5000 and is styled with Bootstrap.


## ⚙️ How to Run Locally
bash
Copy
Edit

# 1. Clone the repository
git clone https://github.com/MuhammadAfdhalF/Garbage-Classification-by-Images-Data-CNN-and-Flask-API-.git
cd Garbage-Classification-by-Images-Data-CNN-and-Flask-API-

# 2. Install required dependencies
pip install -r requirements.txt

# 3. Run the Flask app
python app.py

Then open your browser and go to:
👉 http://127.0.0.1:5000/

## 📷 Screenshots
Add your screenshots by uploading them to GitHub and replacing the links above.

## 📈 Result & Accuracy
✅ Final Accuracy: ~93% on validation data

📉 Training loss and accuracy plots

📊 Confusion matrix for classification analysis

## 🙋‍♂️ Author
Muhammad Afdhal F
👨‍💻 GitHub
📧 Email: your.email@example.com
📷 Instagram (optional) | 🌐 Website (optional

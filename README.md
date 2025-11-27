<img width="1897" height="865" alt="image" src="https://github.com/user-attachments/assets/5005a24d-712f-4f76-92c1-66ee1fcaaf43" />
<img width="1903" height="882" alt="image" src="https://github.com/user-attachments/assets/962ded5a-27f8-4cc3-8aa0-88934443cedc" />

🚀 Intelligent ML Algorithm Recommender (Streamlit App)

A fully automated Machine Learning analysis web application built using Streamlit, capable of:

loading messy CSV/Excel files

repairing broken data

detecting problem type

performing smart preprocessing

training multiple ML models

selecting the best algorithm

generating visualizations

providing detailed logs

optional Auto EDA (ydata-profiling)

This system runs end-to-end ML with one click.

🌟 Features
🔍 1. Super-Robust Dataset Loader

Handles:

Damaged CSV files

Encodings (UTF-8, Latin-1, CP1252, ISO-8859-1)

Unknown delimiters (, ; | \t space)

Binary-file detection

Single-column CSV splitting

Auto-cleaning of index columns

Automatic data repairs

🤖 2. Problem Type Detection

Automatically detects whether your dataset is:

Binary Classification

Multiclass Classification

Regression

🧠 3. Intelligent Preprocessing

Missing value imputation

LabelEncoding / OneHotEncoding

StandardScaler / MinMaxScaler (auto selected)

Variance threshold (drops constant features)

Optional feature selection

Categorical + Numerical pipeline building

⚙️ 4. Multi-Model Training

Trains multiple algorithms depending on problem type:

Classification:

Logistic Regression

Random Forest

Decision Tree

Naive Bayes

SVM

KNN

AdaBoost

Regression:

Linear Regression

Random Forest Regressor

Decision Tree Regressor

Models are auto-selected based on:

dataset size

class balance

feature count

📊 5. Adaptive Metrics

Accuracy, F1, AUC (classification)

R², RMSE, MAE (regression)

📈 6. Visualizations

Performance bar charts

Confusion matrix

ROC curves

Regression error plots

Multi-model comparison

Auto-generated Streamlit Plotly graphs

🧾 7. Optional Auto EDA

Generates full HTML profiling report (if installed):

pip install ydata-profiling

🖥 8. Full Streamlit UI

Upload CSV/Excel

Auto-detect target column

Run entire analysis

Download comparison results

View logs

Beautiful UI with custom CSS

📦 Installation
1. Clone the repository
git clone https://github.com/sengobasar/Algorithm-name-recommender.git
cd Algorithm-name-recommender

2. Create a virtual environment
python -m venv venv
venv\Scripts\activate     # Windows
# or
source venv/bin/activate  # Mac/Linux

3. Install dependencies
pip install -r requirements.txt

▶️ Run the Streamlit App
streamlit run app.py

📁 Project Structure
Algorithm-name-recommender/
│
├── app.py                     # MAIN Streamlit UI Application
├── ml_recommender.py          # Complete ML pipeline engine
├── ui_utils.py                # Console UI utilities
├── requirements.txt           # Dependencies
├── iris_demo.csv              # Example dataset
└── venv/ (optional)           # Local environment

🧠 How It Works
1️⃣ Upload your dataset

CSV or Excel — even corrupted or weird files.

2️⃣ The engine does:

Encoding detection

Delimiter guessing

Cleaning

Splitting single-column CSV

Problem type detection

3️⃣ Builds preprocessing pipeline
4️⃣ Trains multiple ML models
5️⃣ Picks best algorithm
6️⃣ Shows:

Results

Visualizations

Logs

Downloadable CSV

Model scores

🎯 Outputs You Get

Best algorithm

Primary metric (Accuracy / F1 / R²)

Comparison table

Visual analysis charts

Optional HTML EDA report

Clean console logs

Downloadable CSV of results

🔧 Requirements

All dependencies are in requirements.txt.
Install using:

pip install -r requirements.txt


Optional:

pip install ydata-profiling
pip install tpot

🤝 Contributing

Pull requests welcome.

📝 License

MIT License.
If you'd like to improve the model selection, add algorithms, or enhance visualizations — feel free.

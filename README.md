<img width="1897" height="865" alt="image" src="https://github.com/user-attachments/assets/5005a24d-712f-4f76-92c1-66ee1fcaaf43" />
<img width="1903" height="882" alt="image" src="https://github.com/user-attachments/assets/962ded5a-27f8-4cc3-8aa0-88934443cedc" />

🚀 Intelligent ML Algorithm Recommender System

A fully automated Machine Learning pipeline that analyzes any dataset, preprocesses it, tests multiple algorithms, compares performance, and recommends the best ML model — all without manual trial-and-error.

This system is designed to help beginners, students, and professionals quickly determine the most suitable algorithm for classification or regression problems.

🌟 Key Features
✅ Automatic Problem Detection

Identifies whether the dataset is for:

Binary Classification

Multiclass Classification

Regression

✅ Smart Preprocessing

Automatic missing value handling

Categorical encoding (OneHot / Label Encoding)

Feature scaling

Automatic feature selection (for high dimensional data)

✅ Multi-Algorithm Training

Evaluates a curated set of top-performing algorithms:

Logistic Regression

Random Forest

Decision Tree

Naive Bayes

SVM

XGBoost

LightGBM

Linear Regression / Ridge / Lasso (for regression)

✅ Adaptive Metrics

Automatically picks the right evaluation metrics:

Accuracy, Precision, Recall, F1, AUC (Classification)

R², RMSE, MAE (Regression)

✅ Rich Visualizations

Generates:

Performance comparison bar charts

Confusion matrix

ROC curves

Regression scatter & residual plots

✅ Auto EDA (Optional)

Generates a full HTML report using ydata-profiling.

📦 Installation
git clone https://github.com/sengobasar/Algorithm-name-recommender.git
cd Algorithm-name-recommender

Create a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

Install dependencies
pip install -r requirements.txt

🧠 Usage Example
Python Script
from ml_recommender import IntelligentMLRecommendationSystem

recommender = IntelligentMLRecommendationSystem()
best_model, results = recommender.run_automated_ml(
    file_path="your_dataset.csv",
    target_column="target",
    generate_eda=False
)

Command-Line Usage
python ml_recommender.py --file data.csv --target target_column

📊 Example (Iris Dataset)
from sklearn.datasets import load_iris
import pandas as pd

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df["target"] = iris.target
df.to_csv("iris.csv", index=False)

from ml_recommender import IntelligentMLRecommendationSystem
recommender = IntelligentMLRecommendationSystem()
recommender.run_automated_ml("iris.csv", "target", generate_eda=False)

📁 Output Generated

When you run the system, you get:

✔ Best algorithm (e.g., Random Forest)

✔ Performance comparison table

✔ Model evaluation plots

✔ Saved best model (best_model.pkl)

✔ Optional EDA report (eda_report_*.html)

🛠 Customization

You can easily extend the system by editing:

select_algorithms_by_problem_type → add/remove ML models

create_intelligent_preprocessing_pipeline → modify preprocessing

create_*_plots → add new visualizations

🤝 Contributing

Pull requests are welcome!
If you'd like to improve the model selection, add algorithms, or enhance visualizations — feel free.

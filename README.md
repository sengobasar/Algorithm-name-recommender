<div align="center">

# 🤖 AI-Powered ML Algorithm Recommender

### *Smart, Transparent, One-Click Machine Learning Pipeline*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎯 Demo](#-demo) • [📖 Documentation](#-how-it-works)

![Demo](https://img.shields.io/badge/Status-Hackathon_Ready-success?style=for-the-badge)
![AI Powered](https://img.shields.io/badge/AI-Powered-purple?style=for-the-badge)

</div>

---

## 🧠 **What Makes This AI-Powered?**

> **Unlike black-box AutoML tools**, our system uses **intelligent AI agents** that make transparent, adaptive decisions at every step. Perfect for **learning, debugging, and real-world messy data**.

<table>
<tr>
<td width="25%" align="center">
<img src="https://img.icons8.com/fluency/96/artificial-intelligence.png" width="64"/>
<br><b>Smart Detection</b>
<br>AI analyzes target distribution & auto-detects problem type
</td>
<td width="25%" align="center">
<img src="https://img.icons8.com/fluency/96/module.png" width="64"/>
<br><b>Adaptive Pipeline</b>
<br>Preprocessing based on skewness, collinearity, not fixed rules
</td>
<td width="25%" align="center">
<img src="https://img.icons8.com/fluency/96/engineering.png" width="64"/>
<br><b>Dynamic Selection</b>
<br>AI picks 7 best from 21 algorithms based on dataset traits
</td>
<td width="25%" align="center">
<img src="https://img.icons8.com/fluency/96/transparency.png" width="64"/>
<br><b>Full Transparency</b>
<br>See WHY each decision was made—not a black box
</td>
</tr>
</table>

### 🎯 **Key AI Capabilities**

```diff
+ 🧠 Intelligent Problem Detection: Binary/Multiclass/Regression auto-identified
+ 🔧 Adaptive Preprocessing: Type-aware imputation, smart scaling selection
+ ⚙️ Dynamic Algorithm Pool: 21 algorithms, 7 selected based on data characteristics
+ 📊 Empirical Validation: 5-fold cross-validation with transparent metrics
+ 🎓 Educational Value: Shows reasoning—perfect for learning ML workflows
```

---

## 📊 **Stats at a Glance**

<div align="center">

| 🤖 Algorithms | 🔄 Cross-Validation | ⚡ Time to Results | 🎯 Accuracy |
|:---:|:---:|:---:|:---:|
| **21** ML Models | **5-Fold** CV | **< 60 sec** | Ranked & Visualized |

</div>

---

## ⚡ **Quick Start**

```bash
# 1️⃣ Clone the repository
git clone https://github.com/sengobasar/Algorithm-name-recommender.git
cd Algorithm-name-recommender

# 2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate          # Mac/Linux
# venv\Scripts\activate           # Windows

# 3️⃣ Install dependencies & Run
pip install -r requirements.txt
streamlit run app.py
```

**🎉 That's it!** Open browser → Upload CSV → Get AI recommendations

---

## ✨ **Features**

### 🔧 **Robust Data Handling**
- ✅ **Repairs corrupted files** - handles malformed CSV/Excel
- ✅ **Auto-detects encodings** - UTF-8, Latin-1, CP1252, ISO-8859-1
- ✅ **Smart delimiter detection** - comma, semicolon, tab, pipe, space
- ✅ **Cleans noisy data** - handles missing values intelligently

### 🧠 **Intelligent Preprocessing**
- ✅ **Type-aware imputation** - mean/median for numerical, mode for categorical
- ✅ **Adaptive scaling** - StandardScaler/MinMaxScaler auto-selected
- ✅ **Smart encoding** - LabelEncoder for ordinal, OneHot for nominal
- ✅ **Feature selection** - variance threshold, collinearity handling

### 🤖 **Multi-Algorithm Training**
- ✅ **21 algorithms available** - dynamically selects best 7 for your data
- ✅ **5-fold cross-validation** - robust performance estimation
- ✅ **Parallel execution** - fast training on multiple models
- ✅ **Adaptive metrics** - Accuracy/F1/AUC for classification, R²/RMSE/MAE for regression

### 📊 **Rich Visualizations**
- ✅ **Performance comparisons** - interactive bar charts
- ✅ **Confusion matrices** - for classification tasks
- ✅ **ROC curves** - AUC visualization
- ✅ **Error plots** - regression residual analysis
- ✅ **Downloadable results** - CSV export of all metrics

---

## 🎯 **How It Works**

```mermaid
graph LR
    A[📁 Upload Dataset] --> B[🔍 AI Analysis]
    B --> C[🧹 Smart Cleaning]
    C --> D[🧠 Adaptive Preprocessing]
    D --> E[🤖 Train 7 Models]
    E --> F[📊 5-Fold CV]
    F --> G[🏆 Rank & Recommend]
    G --> H[📈 Visualize Results]
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e9
    style G fill:#fce4ec
    style H fill:#fff9c4
```

### 📋 **Step-by-Step Process**

| Step | Process | AI Magic ✨ |
|:---:|---------|-------------|
| **1** | 📁 **Upload** | Handles CSV/Excel with any encoding/delimiter |
| **2** | 🔍 **Analyze** | AI detects types, skewness, collinearity, missing patterns |
| **3** | 🧹 **Clean** | Auto-repairs corrupted data, validates structure |
| **4** | 🧠 **Preprocess** | Adaptive pipeline: imputation → scaling → encoding |
| **5** | 🤖 **Train** | 7 algorithms selected from 21 based on dataset characteristics |
| **6** | 📊 **Validate** | 5-fold cross-validation for robust metrics |
| **7** | 🏆 **Recommend** | Best algorithm ranked with reasoning + visualizations |

---

## 🤖 **Supported Algorithms**

<details open>
<summary><b>📊 Classification Models (7 algorithms)</b></summary>

- 🎯 Logistic Regression
- 🌳 Random Forest Classifier
- 🌲 Decision Tree Classifier
- 📈 Naive Bayes
- 🎨 Support Vector Machine (SVM)
- 📍 K-Nearest Neighbors (KNN)
- 🚀 AdaBoost Classifier

</details>

<details>
<summary><b>📈 Regression Models (3+ algorithms)</b></summary>

- 📉 Linear Regression
- 🌳 Random Forest Regressor
- 🌲 Decision Tree Regressor
- *+ More selected dynamically*

</details>

> 💡 **AI dynamically selects** the best 7 algorithms based on dataset size, class balance, feature count, and problem complexity.

---

## 🌟 **What Makes Us Different**

<table>
<tr>
<td width="50%">

### 🔓 **Not a Black Box**
Unlike AutoML tools, you see:
- ✅ Why each preprocessing step was chosen
- ✅ How algorithms were selected
- ✅ Detailed performance comparisons
- ✅ Step-by-step reasoning logs

**Perfect for:** Education, debugging, understanding ML workflows

</td>
<td width="50%">

### 🧹 **Built for Messy Data**
Real-world datasets are imperfect:
- ✅ Handles corrupted files
- ✅ Mixed encodings & delimiters
- ✅ Missing values & noise
- ✅ Inconsistent formats

**No preprocessing needed** - just upload!

</td>
</tr>
<tr>
<td width="50%">

### ⚡ **Fast & Local**
- ✅ Results in < 60 seconds
- ✅ No cloud dependencies
- ✅ Runs on your machine
- ✅ Privacy-friendly

**Your data never leaves** your computer!

</td>
<td width="50%">

### 📚 **Educational**
Learn while you work:
- ✅ See all metrics & comparisons
- ✅ Understand preprocessing choices
- ✅ Compare algorithm performance
- ✅ Export results for analysis

**Great for students & researchers!**

</td>
</tr>
</table>

---

## 📦 **Installation**

### **Prerequisites**
- Python 3.8 or higher
- pip package manager

### **Dependencies**
All required packages are in `requirements.txt`:
```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
plotly>=5.14.0
openpyxl>=3.1.0
ydata-profiling>=4.5.0  # Optional: for Auto-EDA
```

### **Optional Features**
```bash
# For comprehensive EDA reports
pip install ydata-profiling

# For advanced AutoML (future integration)
pip install tpot
```

---

## 🎬 **Usage Example**

1. **Launch the app:**
   ```bash
   streamlit run app.py
   ```

2. **Upload your dataset** (CSV or Excel)

3. **Select target column** from dropdown

4. **Click "🚀 Run Analysis"**

5. **Get results:**
   - 🏆 Best algorithm recommendation
   - 📊 Performance metrics for all models
   - 📈 Interactive visualizations
   - 💾 Downloadable comparison CSV

---

## 📁 **Project Structure**

```
Algorithm-name-recommender/
│
├── app.py                    # 🎨 Streamlit UI Application
├── ml_recommender.py         # 🧠 Core ML Pipeline Engine
├── ui_utils.py               # 🖥️ Console UI Utilities
├── requirements.txt          # 📦 Dependencies
├── iris_demo.csv             # 📊 Example Dataset
├── README.md                 # 📖 This file
└── venv/                     # 🐍 Virtual Environment (optional)
```

---

## 🔬 **Research Foundation**

This project is based on academic research focusing on:
- **Adaptive preprocessing** based on data characteristics
- **Transparent algorithm selection** vs black-box automation
- **Educational ML workflows** for learning and debugging
- **Robust data handling** for real-world imperfect datasets

> 📄 *Full research paper available in repository*

---

## 🎓 **Use Cases**

| Use Case | Description |
|----------|-------------|
| 🎓 **Education** | Learn ML workflows with transparent reasoning |
| 🔬 **Research** | Quick baseline comparisons for experiments |
| 💼 **Business** | Fast prototyping for data analysis projects |
| 🧪 **Data Science** | Explore algorithm performance on new datasets |
| 🏆 **Hackathons** | Rapid ML pipeline for competitions |

---

## 🚀 **Future Roadmap**

- [ ] 🎛️ Hyperparameter tuning with Optuna
- [ ] 🔍 Model explainability (SHAP, LIME)
- [ ] 📝 Text classification support
- [ ] ⏰ Time series analysis
- [ ] 🏗️ Deep learning integration
- [ ] 🌐 REST API endpoint
- [ ] 📊 Benchmark vs AutoGluon/Auto-sklearn

---

## 🤝 **Contributing**

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 **Author**

**Sengo Basar**
- GitHub: [@sengobasar](https://github.com/sengobasar)
- Project: [Algorithm-name-recommender](https://github.com/sengobasar/Algorithm-name-recommender)

---

## 🙏 **Acknowledgments**

Built with:
- 🐍 Python & Scikit-learn for ML
- 🎨 Streamlit for beautiful UI
- 📊 Plotly for interactive visualizations
- 🧮 Pandas & NumPy for data processing

---

<div align="center">

### ⭐ **If you find this useful, please star the repo!**

[![Star this repo](https://img.shields.io/github/stars/sengobasar/Algorithm-name-recommender?style=social)](https://github.com/sengobasar/Algorithm-name-recommender)

**Made with ❤️ for the ML community**

</div>

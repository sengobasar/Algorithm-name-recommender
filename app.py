# COMPLETE & UNIFIED ML RECOMMENDER - app.py (FINAL ROBUST VERSION)
# Handles single columns, missing features, and all edge cases

import streamlit as st
import pandas as pd
import numpy as np
import warnings
import joblib
from datetime import datetime
import io
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import chardet
import os
import sys
import streamlit.components.v1 as components
import base64

def custom_file_uploader(label, types, help_text):
    """Custom file uploader with animated folder design"""
    component = _custom_file_uploader_component(label, types, help_text)

    if component and component.value:
        component_value = component.value
        # Parse the returned data - try different approaches
        try:
            if isinstance(component_value, dict):
                file_data = component_value['file_data']
                file_name = component_value['file_name']
                file_type = component_value['file_type']
            else:
                # If it's not a dict, try to access as attributes
                file_data = getattr(component_value, 'file_data', None)
                file_name = getattr(component_value, 'file_name', None)
                file_type = getattr(component_value, 'file_type', None)

            if file_data and file_name:
                # Decode base64 data
                file_bytes = base64.b64decode(file_data)

                # Create a file-like object
                file_obj = io.BytesIO(file_bytes)
                file_obj.name = file_name
                file_obj.type = file_type

                return file_obj
            else:
                st.error("Missing file data or filename from upload")
                return None
        except Exception as e:
            st.error(f"Error processing uploaded file: {str(e)}")
            return None

    return None

def _custom_file_uploader_component(label, types, help_text):
    """Streamlit component for custom file uploader"""
    # HTML and CSS for the custom uploader
    html_code = f"""
    <div class="container">
      <div class="folder">
        <div class="front-side">
          <div class="tip"></div>
          <div class="cover"></div>
        </div>
        <div class="back-side cover"></div>
      </div>
      <label class="custom-file-upload">
        <input class="title" type="file" id="file-input" accept="{','.join('.' + t for t in types)}" />
        {label}
      </label>
    </div>

    <style>
    .container {{
      --transition: 350ms;
      --folder-W: 120px;
      --folder-H: 80px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-end;
      padding: 10px;
      background: linear-gradient(135deg, #6dd5ed, #2193b0);
      border-radius: 15px;
      box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
      height: calc(var(--folder-H) * 1.7);
      position: relative;
    }}

    .folder {{
      position: absolute;
      top: -20px;
      left: calc(50% - 60px);
      animation: float 2.5s infinite ease-in-out;
      transition: transform var(--transition) ease;
    }}

    .folder:hover {{
      transform: scale(1.05);
    }}

    .folder .front-side,
    .folder .back-side {{
      position: absolute;
      transition: transform var(--transition);
      transform-origin: bottom center;
    }}

    .folder .back-side::before,
    .folder .back-side::after {{
      content: "";
      display: block;
      background-color: white;
      opacity: 0.5;
      z-index: 0;
      width: var(--folder-W);
      height: var(--folder-H);
      position: absolute;
      transform-origin: bottom center;
      border-radius: 15px;
      transition: transform 350ms;
      z-index: 0;
    }}

    .container:hover .back-side::before {{
      transform: rotateX(-5deg) skewX(5deg);
    }}
    .container:hover .back-side::after {{
      transform: rotateX(-15deg) skewX(12deg);
    }}

    .folder .front-side {{
      z-index: 1;
    }}

    .container:hover .front-side {{
      transform: rotateX(-40deg) skewX(15deg);
    }}

    .folder .tip {{
      background: linear-gradient(135deg, #ff9a56, #ff6f56);
      width: 80px;
      height: 20px;
      border-radius: 12px 12px 0 0;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
      position: absolute;
      top: -10px;
      z-index: 2;
    }}

    .folder .cover {{
      background: linear-gradient(135deg, #ffe563, #ffc663);
      width: var(--folder-W);
      height: var(--folder-H);
      box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
      border-radius: 10px;
    }}

    .custom-file-upload {{
      font-size: 1.1em;
      color: #ffffff;
      text-align: center;
      background: rgba(255, 255, 255, 0.2);
      border: none;
      border-radius: 10px;
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
      cursor: pointer;
      transition: background var(--transition) ease;
      display: inline-block;
      width: 100%;
      padding: 10px 35px;
      position: relative;
    }}

    .custom-file-upload:hover {{
      background: rgba(255, 255, 255, 0.4);
    }}

    .custom-file-upload input[type="file"] {{
      display: none;
    }}

    @keyframes float {{
      0% {{
        transform: translateY(0px);
      }}

      50% {{
        transform: translateY(-20px);
      }}

      100% {{
        transform: translateY(0px);
      }}
    }}
    </style>

    <script>
    const fileInput = document.getElementById('file-input');
    const label = document.querySelector('.custom-file-upload');

    label.addEventListener('click', () => {{
      fileInput.click();
    }});

    fileInput.addEventListener('change', (event) => {{
      const file = event.target.files[0];
      if (file) {{
        const reader = new FileReader();
        reader.onload = function(e) {{
          const fileData = e.target.result.split(',')[1]; // Remove data: prefix
          const fileInfo = {{
            file_data: fileData,
            file_name: file.name,
            file_type: file.type
          }};
          // Send data back to Streamlit
          window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: fileInfo
          }}, '*');
        }};
        reader.readAsDataURL(file);
      }}
    }});
    </script>
    """

    return components.html(html_code, height=200)


# Add the parent directory to path to allow importing ui_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ui_utils import ConsoleUI, MessageType
from llm_explainer import render_ai_explanation_panel

# Core ML libraries
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB
import xgboost as xgb
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, r2_score, mean_squared_error

warnings.filterwarnings('ignore')

class IntelligentMLRecommendationSystem:
    def __init__(self):
        self.log = []
        self.df = None
        self.X = None
        self.y = None
        self.target_column = None
        self.dataset_info = {}
        self.problem_type = None
        self.preprocessing_pipeline = None
        self.trained_models = {}
        self.best_model_name = None
        self.best_model_results = None
        self.evaluation_results = None
        self.test_data = None

    def log_message(self, message, msg_type=MessageType.INFO):
        """Log a message with a specific type"""
        formatted_msg = ConsoleUI.format_message(message, msg_type)
        self.log.append(formatted_msg)
        
        if msg_type in [MessageType.ERROR, MessageType.WARNING]:
            print(formatted_msg)
        print(message)

    def run_complete_analysis(self, data_source, target_column=None):
        """Main orchestrator function"""
        self.log_message("🚀 STARTING AUTOMATED ML PIPELINE")
        
        try:
            # Step 1: Load and Analyze
            self._load_and_analyze(data_source, target_column)
            
            # Step 2: Create Preprocessing Pipeline
            self._create_preprocessing_pipeline()
            # Step 3 & 4: Train and Evaluate Models
            self._train_and_evaluate_models()
            
            # Step 5: Rank and Select Best Model
            self._analyze_and_rank_results()
            
            # Step 6: Create Visualizations
            fig = self._create_visualizations()
            
            self.log_message("🎉 ANALYSIS SUCCESSFULLY COMPLETED!")
            return {
                'best_algorithm': self.best_model_name,
                'best_score': {list(self.best_model_results['metrics'].keys())[0]: 
                              list(self.best_model_results['metrics'].values())[0]},
                'comparison_df': self.evaluation_results,
                'visualization_figure': fig,
                'log': self.log,
                'problem_type': self.problem_type
            }
        except Exception as e:
            self.log_message(f"❌ Error in analysis: {str(e)}")
            raise

    def _detect_file_type(self, data_source):
        """Detect the actual file type and content"""
        data_source.seek(0)
        first_bytes = data_source.read(100)
        data_source.seek(0)
        
        # Check for binary file signatures
        if first_bytes.startswith(b'\x50\x4b'):  # ZIP/Excel signature
            return 'excel'
        elif first_bytes.startswith(b'\xd0\xcf\x11\xe0'):  # Old Excel signature
            return 'excel'
        elif b'\x00' in first_bytes[:50]:  # Contains null bytes = likely binary
            return 'binary'
        elif len([byte for byte in first_bytes if byte > 127]) / len(first_bytes) > 0.3:  # Too many high bytes
            return 'binary'
        else:
            return 'text'

    def _detect_encoding(self, data_source):
        """Detect file encoding using chardet"""
        data_source.seek(0)
        raw_data = data_source.read()
        data_source.seek(0)
        
        try:
            detected = chardet.detect(raw_data)
            encoding = detected['encoding'] if detected['encoding'] else 'utf-8'
            confidence = detected['confidence'] if detected['confidence'] else 0.0
            
            self.log_message(
                f"Detected encoding: {encoding} (confidence: {confidence:.2f})",
                MessageType.INFO
            )
            
            # Fallback to common encodings if confidence is low
            if confidence < 0.7:
                return 'utf-8'
            return encoding
        except:
            return 'utf-8'

    def _super_robust_csv_reader(self, data_source):
        """Ultra-robust CSV reader with comprehensive error handling"""
        # First, detect file type
        file_type = self._detect_file_type(data_source)
        self.log_message(f"Detected file type: {file_type}", MessageType.INFO)
        
        if file_type == 'binary':
            error_msg = (
                "This appears to be a binary file, not a CSV.\n"
                "Please ensure you're uploading a text-based CSV file.\n"
                "If this should be a CSV, the file may be corrupted."
            )
            self.log_message(error_msg, MessageType.ERROR)
            ErrorAlert(error_msg)
            raise ValueError(error_msg)
        
        # Detect encoding
        encoding = self._detect_encoding(data_source)
        
        # Define comprehensive parsing strategies
        parsing_strategies = [
            # Standard approaches
            {'encoding': encoding},
            {'encoding': encoding, 'on_bad_lines': 'skip'},
            {'encoding': encoding, 'engine': 'python'},
            {'encoding': encoding, 'engine': 'python', 'on_bad_lines': 'skip'},
            
            # Try with different separators
            {'encoding': encoding, 'sep': ';', 'on_bad_lines': 'skip'},
            {'encoding': encoding, 'sep': '\t', 'on_bad_lines': 'skip'},
            {'encoding': encoding, 'sep': '|', 'on_bad_lines': 'skip'},
            {'encoding': encoding, 'sep': ' ', 'on_bad_lines': 'skip'},
            
            # Different encodings as fallback
            {'encoding': 'latin-1', 'on_bad_lines': 'skip'},
            {'encoding': 'cp1252', 'on_bad_lines': 'skip'},
            {'encoding': 'iso-8859-1', 'on_bad_lines': 'skip'},
            
            # Last resort - single column with manual parsing
            {'encoding': encoding, 'header': None, 'names': ['raw_data'], 'on_bad_lines': 'skip'},
        ]
        
        last_error = None
        
        for i, strategy in enumerate(parsing_strategies):
            try:
                data_source.seek(0)
                self.log_message(f"🔄 Trying parsing strategy #{i+1}...")
                
                df = pd.read_csv(data_source, **strategy)
                
                # Validate result
                if df.empty:
                    raise ValueError("Empty dataframe")
                
                if df.shape[1] == 0:
                    raise ValueError("No columns found")
                
                # Check if it's just a single column that needs to be split
                if df.shape[1] == 1 and 'raw_data' in df.columns:
                    self.log_message("Single column detected - attempting to split...", MessageType.INFO)
                    df = self._split_single_column(df)
                
                # Final validation
                if df.shape[0] < 5:  # Need at least 5 rows for ML
                    raise ValueError("Too few rows for machine learning")
                
                if df.shape[1] < 2:  # Need at least 2 columns (feature + target)
                    raise ValueError("Need at least 2 columns for ML (features + target)")
                
                self.log_message(f"Success with strategy #{i+1}: {df.shape[0]} rows, {df.shape[1]} columns", MessageType.SUCCESS)
                return df
                
            except Exception as e:
                last_error = e
                self.log_message(f"Strategy #{i+1} failed: {str(e)}", MessageType.WARNING)
                continue
        
        # If all strategies failed, provide helpful error message
        error_msg = (
            "All parsing strategies failed. Please check your file format.\n\n"
            "**Issues detected:**\n"
            "• File might be corrupted or not a proper CSV\n"
            "• Might have only 1 column (need at least 2 for ML)\n"
            "• Insufficient data for machine learning\n\n"
            "**Solutions:**\n"
            "1. Check your file: Open in notepad to verify it's readable text\n"
            "2. Ensure multiple columns: ML needs features + target column\n"
            "3. Add more data: Need at least 10+ rows for analysis\n"
            "4. Try Excel format: Save as .xlsx instead of .csv\n"
            "5. Check delimiters: Ensure data is properly separated\n\n"
            f"Last error: {str(last_error)}"
        )
        raise ValueError(error_msg)

    def _split_single_column(self, df):
        """Attempt to split a single column into multiple columns"""
        
        raw_data = df['raw_data'].dropna().astype(str)
        
        if raw_data.empty:
            raise ValueError("No data to split")
        
        # Try different delimiters
        delimiters = [',', ';', '\t', '|', ' ', ':', '-']
        best_delimiter = None
        max_columns = 1
        
        for delimiter in delimiters:
            # Test on first few rows
            test_splits = [row.split(delimiter) for row in raw_data.head(5)]
            column_counts = [len(split) for split in test_splits]
            
            # Check if this delimiter gives consistent multiple columns
            if len(set(column_counts)) == 1 and column_counts[0] > 1:
                if column_counts[0] > max_columns:
                    max_columns = column_counts[0]
                    best_delimiter = delimiter
        
        if best_delimiter is None:
            # Try to create synthetic features if we have numeric data
            if raw_data.str.match(r'^[\d\.\-\+e]+$').any():
                self.log_message("🔧 Creating synthetic features from single numeric column...")
                numeric_data = pd.to_numeric(raw_data, errors='coerce').dropna()
                
                if len(numeric_data) > 5:
                    # Create basic statistical features
                    df_new = pd.DataFrame({
                        'original_value': numeric_data,
                        'value_squared': numeric_data ** 2,
                        'value_log': np.log(np.abs(numeric_data) + 1),
                        'value_normalized': (numeric_data - numeric_data.mean()) / numeric_data.std(),
                        'target': numeric_data  # Use original as target for now
                    })
                    return df_new
            
            raise ValueError("Could not split single column into multiple features")
        
        # Split using best delimiter
        self.log_message(f"🔧 Splitting using delimiter '{best_delimiter}' into {max_columns} columns")
        
        split_data = []
        for row in raw_data:
            parts = row.split(best_delimiter)
            # Pad or trim to consistent length
            while len(parts) < max_columns:
                parts.append('')
            parts = parts[:max_columns]
            split_data.append(parts)
        
        # Create new dataframe
        columns = [f'feature_{i}' for i in range(max_columns-1)] + ['target']
        df_new = pd.DataFrame(split_data, columns=columns)
        
        # Clean and convert numeric columns
        for col in df_new.columns:
            # Try to convert to numeric
            numeric_series = pd.to_numeric(df_new[col], errors='coerce')
            if not numeric_series.isna().all():
                df_new[col] = numeric_series
        
        # Remove rows with all NaN values
        df_new = df_new.dropna(how='all')
        
        return df_new

    def _load_and_analyze(self, data_source, target_column):
        self.log_message("📁 STEP 1: LOADING & ANALYZING DATASET")
        
        try:
            # Handle Excel files
            if data_source.name.endswith(('.xlsx', '.xls')):
                try:
                    data_source.seek(0)
                    self.df = pd.read_excel(data_source)
                    self.log_message(f"✅ Excel file loaded: {self.df.shape}")
                except Exception as e:
                    raise ValueError(f"❌ Could not read Excel file: {str(e)}")
            
            # Handle CSV files with super robust parsing
            else:
                self.df = self._super_robust_csv_reader(data_source)
        
        except Exception as e:
            raise ValueError(str(e))
        
        # Clean the dataframe
        self.df = self._clean_dataframe(self.df)
        
        # CRITICAL FIX: Ensure we have adequate data for ML
        if self.df.shape[0] < 5:
            raise ValueError(
                f"❌ Insufficient data: Only {self.df.shape[0]} rows found.\n"
                f"Machine learning requires at least 10+ rows for reliable analysis.\n"
                f"Please provide a dataset with more samples."
            )
        
        if self.df.shape[1] < 2:
            raise ValueError(
                f"❌ Insufficient features: Only {self.df.shape[1]} column(s) found.\n"
                f"Machine learning requires at least 2 columns (features + target).\n"
                f"Please ensure your dataset has multiple columns."
            )
        
        # Auto-detect target column if not provided
        if not target_column or target_column not in self.df.columns:
            target_column = self.df.columns[-1]
            self.log_message(f"🎯 Auto-detected target column: '{target_column}'")
        
        # Separate features and target
        self.X = self.df.drop(columns=[target_column])
        self.y = self.df[target_column]
        self.target_column = target_column
        
        # CRITICAL CHECK: Ensure X is not empty
        if self.X.shape[1] == 0:
            raise ValueError(
                f"❌ No features available after removing target column.\n"
                f"The dataset must have multiple columns to separate features from target.\n"
                f"Current columns: {list(self.df.columns)}\n"
                f"Target column: {target_column}\n"
                f"Remaining features: {self.X.shape[1]}"
            )
        
        # Perform internal analysis
        self._analyze_dataset_characteristics()
        self._detect_problem_type()
        
        self.log_message(f"✅ Dataset analysis complete. Problem type: {self.problem_type}")
        self.log_message(f"✅ Features: {self.X.shape[1]} columns, Target: '{self.target_column}'")

    def _clean_dataframe(self, df):
        """Clean the loaded dataframe"""
        original_shape = df.shape
        
        # Remove completely empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Clean column names
        df.columns = [str(col).strip().replace('\n', '').replace('\r', '').replace('\t', '') for col in df.columns]
        
        # Remove duplicate columns
        df = df.loc[:, ~df.columns.duplicated()]
        
        # Remove columns that look like indices
        cols_to_drop = []
        for col in df.columns:
            if ('Unnamed' in str(col) and 
                df[col].astype(str).str.match(r'^\d+$').all() and 
                df[col].nunique() == len(df)):
                cols_to_drop.append(col)
        
        if cols_to_drop:
            df = df.drop(columns=cols_to_drop)
            self.log_message(f"🧹 Removed {len(cols_to_drop)} index columns")
        
        if df.shape != original_shape:
            self.log_message(f"🧹 Cleaned dataframe: {original_shape} → {df.shape}")
        
        return df

    def _analyze_dataset_characteristics(self):
        """Analyze dataset characteristics"""
        self.dataset_info = {
            'n_samples': self.df.shape[0],
            'n_features': self.X.shape[1],
            'columns': list(self.df.columns),
            'missing_values': self.df.isnull().sum().sum(),
            'missing_percentage': (self.df.isnull().sum().sum() / self.df.size) * 100
        }
        
        # Identify feature types
        numerical_features = self.X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = self.X.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        
        self.dataset_info.update({
            'numerical_features': numerical_features,
            'categorical_features': categorical_features,
            'n_numerical': len(numerical_features),
            'n_categorical': len(categorical_features)
        })
        
        # Analyze target variable
        if self.y.dtype in ['object', 'category', 'bool'] or self.y.nunique() < 20:
            self.dataset_info['target_type'] = 'categorical'
            self.dataset_info['n_classes'] = self.y.nunique()
            self.dataset_info['class_distribution'] = self.y.value_counts().to_dict()
        else:
            self.dataset_info['target_type'] = 'numerical'
            self.dataset_info['target_stats'] = {
                'min': float(self.y.min()),
                'max': float(self.y.max()),
                'mean': float(self.y.mean()),
                'median': float(self.y.median())
            }

    def _detect_problem_type(self):
        """Detect ML problem type"""
        if self.dataset_info['target_type'] == 'categorical':
            if self.dataset_info['n_classes'] == 2:
                self.problem_type = 'binary_classification'
            else:
                self.problem_type = 'multiclass_classification'
        else:
            self.problem_type = 'regression'
            
        self.log_message(f"🎯 Problem Type: {self.problem_type.replace('_', ' ').title()}")

    def _create_preprocessing_pipeline(self):
        """Create preprocessing pipeline"""
        self.log_message("🔧 STEP 2: CREATING PREPROCESSING PIPELINE")
        
        num_features = self.dataset_info['numerical_features']
        cat_features = self.dataset_info['categorical_features']
        
        transformers = []
        
        # Numerical preprocessing
        if num_features:
            num_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')), 
                ('scaler', StandardScaler())
            ])
            transformers.append(('num', num_transformer, num_features))
        
        # Categorical preprocessing
        if cat_features:
            cat_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')), 
                ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
            ])
            transformers.append(('cat', cat_transformer, cat_features))
        
        # CRITICAL: Ensure we have at least one transformer
        if not transformers:
            raise ValueError(
                f"❌ No valid features found for preprocessing.\n"
                f"Numerical features: {len(num_features)}\n"
                f"Categorical features: {len(cat_features)}\n"
                f"Please ensure your dataset has valid feature columns."
            )
        
        preprocessor = ColumnTransformer(transformers=transformers, remainder='drop')
        self.preprocessing_pipeline = Pipeline(steps=[('preprocessor', preprocessor)])
        
        self.log_message(f"✅ Preprocessing pipeline created ({len(transformers)} transformers)")

    def _train_and_evaluate_models(self):
        """Train and evaluate models"""
        self.log_message("📊 STEP 3: TRAINING & EVALUATING MODELS")
        
        # Define algorithms
        if 'classification' in self.problem_type:
            algorithms = {
                'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
                'Random Forest': RandomForestClassifier(random_state=42, n_estimators=50),  # Reduced for speed
                'Decision Tree': DecisionTreeClassifier(random_state=42),
                'Naive Bayes': GaussianNB()
            }
        else:
            algorithms = {
                'Linear Regression': LinearRegression(),
                'Random Forest': RandomForestRegressor(random_state=42, n_estimators=50),
                'Decision Tree': DecisionTreeRegressor(random_state=42)
            }
        
        # Train/test split with better error handling
        try:
            if 'classification' in self.problem_type and len(self.y.unique()) > 1:
                X_train, X_test, y_train, y_test = train_test_split(
                    self.X, self.y, test_size=0.3, random_state=42, stratify=self.y
                )
            else:
                X_train, X_test, y_train, y_test = train_test_split(
                    self.X, self.y, test_size=0.3, random_state=42
                )
        except Exception as e:
            # Fallback to simple split
            X_train, X_test, y_train, y_test = train_test_split(
                self.X, self.y, test_size=0.3, random_state=42
            )
            self.log_message("⚠️ Using simple train/test split")
        
        self.test_data = (X_test, y_test)
        self.log_message(f"✅ Data split: {len(X_train)} train, {len(X_test)} test samples")
        
        # Train models
        results = {}
        for name, model in algorithms.items():
            try:
                self.log_message(f"  • Training {name}...")
                
                # Create complete pipeline
                pipeline = Pipeline([
                    ('preprocessor', self.preprocessing_pipeline.steps[0][1]),
                    ('model', model)
                ])
                
                # Train model
                pipeline.fit(X_train, y_train)
                y_pred = pipeline.predict(X_test)
                
                # Calculate metrics
                if 'classification' in self.problem_type:
                    metrics = {
                        'accuracy': accuracy_score(y_test, y_pred),
                        'f1_score': f1_score(y_test, y_pred, average='weighted')
                    }
                else:
                    metrics = {
                        'r2_score': r2_score(y_test, y_pred),
                        'rmse': np.sqrt(mean_squared_error(y_test, y_pred))
                    }
                
                results[name] = {
                    'metrics': metrics,
                    'pipeline': pipeline,
                    'y_pred': y_pred,
                    'y_true': y_test
                }
                
                self.log_message(f"    ✓ {name} completed")
                
            except Exception as e:
                self.log_message(f"    ✗ {name} failed: {str(e)}")
                continue
        
        if not results:
            raise ValueError(
                "❌ No models were successfully trained.\n"
                "This usually happens when:\n"
                "• Dataset is too small\n"
                "• Features are not properly formatted\n"
                "• All feature values are missing or constant\n"
                "Please check your data quality and try again."
            )
        
        self.trained_models = results
        self.log_message(f"✅ Successfully trained {len(results)} models")

    def _analyze_and_rank_results(self):
        """Analyze and rank results"""
        self.log_message("🏆 STEP 4: ANALYZING RESULTS")
        
        # Determine primary metric
        primary_metric = 'accuracy' if 'classification' in self.problem_type else 'r2_score'
        
        # Create comparison dataframe
        comparison_data = []
        for name, result in self.trained_models.items():
            row = {'Algorithm': name}
            row.update(result['metrics'])
            comparison_data.append(row)
        
        self.evaluation_results = pd.DataFrame(comparison_data).sort_values(
            by=primary_metric, ascending=False
        ).reset_index(drop=True)
        
        # Get best model
        self.best_model_name = self.evaluation_results.iloc[0]['Algorithm']
        self.best_model_results = self.trained_models[self.best_model_name]
        
        self.log_message(f"🥇 Best: {self.best_model_name} ({primary_metric}: {self.best_model_results['metrics'][primary_metric]:.4f})")

    def _create_visualizations(self):
        """Create visualizations"""
        self.log_message("📈 STEP 5: CREATING VISUALIZATIONS")
        
        primary_metric = 'accuracy' if 'classification' in self.problem_type else 'r2_score'
        metric_title = 'Accuracy' if primary_metric == 'accuracy' else 'R² Score'
        
        # Create subplots
        fig = make_subplots(
            rows=1, cols=2, 
            subplot_titles=(f"Model Performance ({metric_title})", "Best Model Analysis")
        )
        
        # Performance comparison
        fig.add_trace(
            go.Bar(
                x=self.evaluation_results['Algorithm'],
                y=self.evaluation_results[primary_metric],
                text=[f"{x:.4f}" for x in self.evaluation_results[primary_metric]],
                textposition='auto',
                name=metric_title
            ),
            row=1, col=1
        )
        
        # Second visualization
        if 'classification' in self.problem_type:
            try:
                cm = confusion_matrix(self.best_model_results['y_true'], self.best_model_results['y_pred'])
                fig.add_trace(
                    go.Heatmap(z=cm, colorscale='Blues', showscale=False),
                    row=1, col=2
                )
            except:
                fig.add_trace(
                    go.Scatter(x=[1], y=[1], mode='text', text=['Classification Results'], textposition='middle center'),
                    row=1, col=2
                )
        else:
            fig.add_trace(
                go.Scatter(
                    x=self.best_model_results['y_true'],
                    y=self.best_model_results['y_pred'],
                    mode='markers',
                    name='Predictions'
                ),
                row=1, col=2
            )
        
        fig.update_layout(height=500, title_text="ML Analysis Results")
        return fig


def display_error(message):
    """Display an error message in a styled container"""
    st.markdown(f"""
    <div style='background-color: #ffebee; border-left: 5px solid #f44336; padding: 1rem; margin: 1rem 0; border-radius: 4px;'>
        <div style='display: flex; align-items: center;'>
            <span style='color: #f44336; margin-right: 10px; font-weight: bold;'>ERROR</span>
            <span>{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_success(message):
    """Display a success message in a styled container"""
    st.markdown(f"""
    <div style='background-color: #e8f5e9; border-left: 5px solid #4caf50; padding: 1rem; margin: 1rem 0; border-radius: 4px;'>
        <div style='display: flex; align-items: center;'>
            <span style='color: #4caf50; margin-right: 10px; font-weight: bold;'>SUCCESS</span>
            <span>{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_warning(message):
    """Display a warning message in a styled container"""
    st.markdown(f"""
    <div style='
        background-color: #fff8e1;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    '>
        <div style='display: flex; align-items: center;'>
            <span style='color: #ff9800; margin-right: 10px; font-weight: bold;'>WARNING</span>
            <span>{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="ML Algorithm Recommender",
        page_icon="🤖",  # Using robot emoji instead of rocket
        layout="wide"
    )
    
    # Initialize session state
    if "analysis_done" not in st.session_state:
        st.session_state.analysis_done = False
        st.session_state.ai_active = False
        st.session_state.analysis_results = None
        st.session_state.structured_results = None
    
    # Custom CSS for the application - Professional ML Research Theme
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Ubuntu', sans-serif;
        }

        .main-title {
            font-size: 4rem;
            color: #ffffff;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 700;
            font-family: 'Ubuntu', sans-serif;
            letter-spacing: 0.5px;
            line-height: 1.1;
            text-transform: uppercase;
        }

        .subtitle {
            text-align: center;
            color: #b1b1b1;
            margin-bottom: 3rem;
            font-size: 1.3rem;
            font-family: 'Ubuntu', sans-serif;
            font-weight: 300;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
        }

        .section-header {
            font-size: 2.5rem;
            color: #ffffff;
            margin-bottom: 2rem;
            font-weight: 500;
            font-family: 'Ubuntu', sans-serif;
            text-align: center;
            border-bottom: 2px solid #333333;
            padding-bottom: 1rem;
        }

        .subsection-header {
            font-size: 1.5rem;
            color: #ffffff;
            margin-bottom: 1.5rem;
            font-weight: 400;
            font-family: 'Ubuntu', sans-serif;
        }

        .metric-card {
            background: #1a1a1a;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            margin-bottom: 2rem;
            border: 1px solid #333333;
        }

        .metric-title {
            font-size: 0.9rem;
            color: #888888;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 600;
            color: #ffffff;
            font-family: 'Courier New', monospace;
        }

        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #7e22ce, #3b82f6);
            color: white;
            font-weight: 500;
            border: none;
            padding: 1rem;
            border-radius: 8px;
            transition: all 0.3s ease;
            font-family: 'Ubuntu', sans-serif;
            font-size: 1.1rem;
        }

        .stButton>button:hover {
            background: linear-gradient(135deg, #6b21a8, #2563eb);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(126, 34, 206, 0.4);
        }

        .sidebar .sidebar-content {
            background: #000000;
            padding: 2rem;
            border-radius: 12px;
            font-family: 'Ubuntu', sans-serif;
            color: #ffffff;
        }

        .welcome-text {
            font-size: 1.2rem;
            line-height: 1.7;
            color: #cccccc;
            margin-bottom: 2rem;
        }

        .feature-list {
            background: #1a1a1a;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            border: 1px solid #333333;
        }

        .feature-list ul {
            margin: 0;
            padding-left: 1.5rem;
        }

        .feature-list li {
            margin-bottom: 0.8rem;
            color: #cccccc;
            font-size: 1.1rem;
        }

        .hero-section {
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
            padding: 4rem 2rem;
            border-radius: 15px;
            margin-bottom: 3rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }

        .content-section {
            background: #0a0a0a;
            padding: 3rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            border: 1px solid #222222;
        }

        .gradient-text {
            background: linear-gradient(90deg, #ffffff 0%, #cccccc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stTextInput>div>div>input {
            background-color: #1a1a1a;
            color: #ffffff;
            border: 1px solid #333333;
            border-radius: 6px;
            padding: 0.5rem;
        }

        .stTextInput>div>div>input:focus {
            border-color: #7e22ce;
            box-shadow: 0 0 0 2px rgba(126, 34, 206, 0.2);
        }

        .stFileUploader>div {
            background-color: #1a1a1a;
            border: 2px dashed #333333;
            border-radius: 10px;
        }

        .stFileUploader>div:hover {
            border-color: #7e22ce;
        }

        .stExpander {
            background-color: #1a1a1a;
            border: 1px solid #333333;
            border-radius: 8px;
        }

        .stExpander summary {
            color: #ffffff;
            font-weight: 500;
        }

        .stDataFrame {
            background-color: #1a1a1a;
            border-radius: 8px;
        }

        .stDataFrame table {
            color: #ffffff;
        }

        .stDataFrame thead th {
            background-color: #333333;
            color: #ffffff;
        }

        .stDataFrame tbody tr:nth-child(even) {
            background-color: #0a0a0a;
        }

        .stDataFrame tbody tr:nth-child(odd) {
            background-color: #1a1a1a;
        }
        
        /* Custom Expander Cards */
        div[data-testid="stExpander"] {
            border: none;
            border-radius: 8px;
            background: linear-gradient(145deg, #212121, #000);
            margin-bottom: 10px; /* Add space between cards */
        }
        div[data-testid="stExpander"] summary:hover {
            background: linear-gradient(145deg, #444, #111);
        }
        div[data-testid="stExpander"] summary {
            background: linear-gradient(145deg, #333, #000);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            color: #00ffeb;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-size: 1.1em;
        }
    </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="main-title">ML Algorithm Recommender</h1>
        <div class="subtitle">
            Intelligent machine learning pipeline for automated algorithm selection and preprocessing under imperfect data conditions
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        # Add animated folder decoration
        st.markdown("""
        <div class="container">
          <div class="folder">
            <div class="front-side">
              <div class="tip"></div>
              <div class="cover"></div>
            </div>
            <div class="back-side cover"></div>
          </div>
        </div>

        <style>
        .container {
          --transition: 350ms;
          --folder-W: 120px;
          --folder-H: 80px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: flex-end;
          padding: 10px;
          background: linear-gradient(135deg, #6dd5ed, #2193b0);
          border-radius: 15px;
          box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
          height: calc(var(--folder-H) * 1.7);
          position: relative;
          margin-bottom: 20px;
        }

        .folder {
          position: absolute;
          top: -20px;
          left: calc(50% - 60px);
          animation: float 2.5s infinite ease-in-out;
          transition: transform var(--transition) ease;
        }

        .folder:hover {
          transform: scale(1.05);
        }

        .folder .front-side,
        .folder .back-side {
          position: absolute;
          transition: transform var(--transition);
          transform-origin: bottom center;
        }

        .folder .back-side::before,
        .folder .back-side::after {
          content: "";
          display: block;
          background-color: white;
          opacity: 0.5;
          z-index: 0;
          width: var(--folder-W);
          height: var(--folder-H);
          position: absolute;
          transform-origin: bottom center;
          border-radius: 15px;
          transition: transform 350ms;
          z-index: 0;
        }

        .container:hover .back-side::before {
          transform: rotateX(-5deg) skewX(5deg);
        }
        .container:hover .back-side::after {
          transform: rotateX(-15deg) skewX(12deg);
        }

        .folder .front-side {
          z-index: 1;
        }

        .container:hover .front-side {
          transform: rotateX(-40deg) skewX(15deg);
        }

        .folder .tip {
          background: linear-gradient(135deg, #ff9a56, #ff6f56);
          width: 80px;
          height: 20px;
          border-radius: 12px 12px 0 0;
          box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
          position: absolute;
          top: -10px;
          z-index: 2;
        }

        .folder .cover {
          background: linear-gradient(135deg, #ffe563, #ffc663);
          width: var(--folder-W);
          height: var(--folder-H);
          box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
          border-radius: 10px;
        }

        @keyframes float {
          0% {
            transform: translateY(0px);
          }

          50% {
            transform: translateY(-20px);
          }

          100% {
            transform: translateY(0px);
          }
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div style="margin-top: -130px;"></div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx', 'xls'],
            help="Need at least 2 columns and 10+ rows for ML"
        )
        
        if uploaded_file:
            display_success(f"File loaded: {uploaded_file.name}")
            
            target_column = st.text_input(
                "Target column (optional)", 
                help="Leave blank to auto-detect (uses last column)"
            )
            
            css = """
<style>
@keyframes button-shimmer-rotate {
    0% {
        transform: translate(-50%, -50%) rotate(0deg);
    }
    100% {
        transform: translate(-50%, -50%) rotate(360deg);
    }
}

/* Target the specific Streamlit button element */
div.stButton > button {
    /* SaaS Black Pill Button Style */
    background-color: #000000;
    color: #FFFFFF;
    border: 1px solid #FFFFFF;
    border-radius: 9999px; /* Pill shape */
    
    /* Positioning for pseudo-elements and layout */
    position: relative;
    overflow: hidden;
    z-index: 1;
    transition: box-shadow 0.3s ease;

    /* Override any conflicting styles from the app's main CSS */
    background-image: none;
    transform: none;
}

/* Rotating shimmer pseudo-element */
div.stButton > button::before {
    content: "";
    position: absolute;
    z-index: -1;
    top: 50%;
    left: 50%;
    width: 200%;
    height: 200%;
    background: conic-gradient(
        transparent 0deg,
        transparent 270deg,
        rgba(255, 255, 255, 0.5) 295deg,
        rgba(255, 255, 255, 0) 320deg,
        transparent 360deg
    );
    animation: button-shimmer-rotate 4s linear infinite;
}

/* Hover glow effect */
div.stButton > button:hover {
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
    /* Reset other hover effects */
    transform: none; 
    background-color: #111111;
}

/* Ensure button text is above the shimmer */
div.stButton > button span {
    position: relative;
    z-index: 2;
}
</style>
"""
            st.markdown(css, unsafe_allow_html=True)
            run_analysis = st.button("Run Analysis", type="primary", key="run_analysis")
        
        st.markdown("---")
        st.markdown("### Dataset Requirements")
        with st.expander("View requirements"):
            st.markdown("""
            - **Minimum Requirements:**
                - 2+ columns (features + target)
                - 10+ rows of data
                - Text or numeric data format
                - Consistent data structure
            - **Recommended:**
                - 100+ rows for better model performance
                - Clean, labeled data
                - Balanced classes (for classification)
            """)
        
        st.markdown("### Supported Features")
        with st.expander("View features"):
            st.markdown("""
            - **Data Handling:**
                - Automatic type detection
                - Missing value imputation
                - Outlier handling
                - Categorical encoding
            - **Advanced Features:**
                - Smart feature selection
                - Cross-validation
                - Hyperparameter tuning
                - Performance metrics
            """)
    
    # Main content
    if uploaded_file:
        # Show analysis results if available
        if st.session_state.get("analysis_done") and st.session_state.analysis_results:
            # Display results
            display_results(st.session_state.analysis_results)
            
            # Add AI explanation button if not already active
            if not st.session_state.get("ai_active", False):
                if st.sidebar.button("🤖 Explain with AI", key="activate_ai_sidebar"):
                    st.session_state.ai_active = True
                    st.rerun()
            
            # Download results
            st.markdown("---")
            st.subheader("📁 Export Results")
            csv_data = st.session_state.analysis_results['comparison_df'].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv_data,
                file_name=f"ml_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime='text/csv',
                help="Download the model comparison results as a CSV file"
            )
            
            # Processing log
            with st.expander("🔍 View Processing Log"):
                for log_entry in st.session_state.analysis_results['log']:
                    if '\u274c' in log_entry:
                        st.error(log_entry)
                    elif '\u26a0\ufe0f' in log_entry:
                        st.warning(log_entry)
                    elif '\u2705' in log_entry:
                        st.success(log_entry)
                    else:
                        st.info(log_entry)
        # Show file analysis
        with st.expander("File Analysis", expanded=True):
            st.markdown("### Dataset Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown('<div class="metric-title">File Name</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{uploaded_file.name}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown('<div class="metric-title">File Size</div>', unsafe_allow_html=True)
                size_mb = uploaded_file.size / (1024 * 1024)
                if size_mb < 1:
                    size_str = f"{uploaded_file.size / 1024:.1f} KB"
                else:
                    size_str = f"{size_mb:.2f} MB"
                st.markdown(f'<div class="metric-value">{size_str}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown('<div class="metric-title">File Type</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{uploaded_file.type.split("/")[-1].upper()}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        if run_analysis:
            with st.spinner("Analyzing dataset and selecting best algorithms..."):
                try:
                    uploaded_file.seek(0)
                    
                    recommender = IntelligentMLRecommendationSystem()
                    results = recommender.run_complete_analysis(
                        data_source=uploaded_file,
                        target_column=target_column if target_column else None
                    )
                    
                    # Store results in session state
                    st.session_state.analysis_results = results
                    st.session_state.analysis_done = True
                    st.session_state.structured_results = {
                        'best_algorithm': results['best_algorithm'],
                        'metrics': results['best_score'],
                        'model_comparison': results['comparison_df'].to_dict(),
                        'problem_type': results.get('problem_type', 'unknown')
                    }
                    
                    st.balloons()
                    st.rerun()  # Rerun to update the UI with the new state
                    
                except Exception as e:
                    st.markdown(f"""
                    <div class='error-box'>
                        <h3>❌ File Processing Error</h3>
                        <p>{str(e)}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show processing log if available
                    if 'recommender' in locals() and recommender.log:
                        with st.expander("🔍 Detailed Processing Log"):
                            for log_entry in recommender.log:
                                st.text(log_entry)
    else:
        # Welcome message
        st.info("👈 Upload a dataset to get started!")

        with st.expander("👋 Welcome & Overview", expanded=True):
            st.markdown("""
            This system addresses the challenge of selecting appropriate machine learning algorithms when working with real-world datasets that may contain missing values, mixed data types, or inconsistent formatting. Traditional approaches often fail under these conditions, requiring extensive manual preprocessing.
            """)

        with st.expander("⚙️ How It Works", expanded=True):
            st.markdown("""
            The system employs an intelligent preprocessing strategy that adapts to dataset characteristics:

            - **Type-aware feature processing**: Automatically detects numerical and categorical features
            - **Robust imputation**: Handles missing values using appropriate strategies for each data type
            - **Flexible encoding**: Transforms categorical variables while preserving information
            - **Standardization**: Normalizes numerical features for algorithm compatibility

            Once a dataset is provided, the system follows a systematic evaluation process:

            1.  **Dataset Inspection**: Analyzes data structure, identifies feature types, and detects problem type (classification vs regression).
            2.  **Type-Aware Preprocessing**: Applies transformations, handles missing values, and prepares data.
            3.  **Multi-Algorithm Evaluation**: Trains and evaluates multiple suitable algorithms on the prepared data.
            4.  **Transparent Recommendation**: Ranks algorithms by performance and recommends the best one.
            """)
        
        with st.expander("⁉️ Help & Troubleshooting"):
            st.markdown("""
            **❌ "No models were successfully trained"**
            - Dataset may have insufficient columns or rows
            - Ensure at least 2 columns (features + target) and 10+ rows
            - Check for corrupted or non-standard data formats

            **❌ "at least one array or dtype is required"**
            - Usually indicates no valid features were found
            - Verify data contains multiple columns with meaningful content
            - Ensure target column is properly identified

            **❌ "binary file" error**
            - File may be corrupted or not in expected format
            - Try saving as Excel (.xlsx) or ensure CSV is properly formatted
            - Open file in a text editor to verify readable content
            """)

def display_results(analysis_results):
    """Display the analysis results in a user-friendly format"""
    # Create two columns: main content (2/3) and right column (1/3)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Inject custom CSS for the expander cards
        st.markdown("""
        <style>
        div[data-testid="stExpander"] {
            border: none;
            border-radius: 8px;
            background: linear-gradient(145deg, #212121, #000);
            margin-bottom: 10px; /* Add space between cards */
        }
        div[data-testid="stExpander"] summary:hover {
            background: linear-gradient(145deg, #444, #111);
        }
        div[data-testid="stExpander"] summary {
            background: linear-gradient(145deg, #333, #000);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            color: #00ffeb;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-size: 1.1em;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Card 1: Analysis Complete
        with st.expander("🎉 Analysis Complete!", expanded=True):
            st.success("Successfully processed and analyzed your dataset!")

        # Card 2: Best Algorithm & Metrics
        with st.expander("🎯 Best Algorithm & Metrics", expanded=True):
            metric_name, metric_value = list(analysis_results['best_score'].items())[0]
            st.subheader("Best Algorithm: " + analysis_results['best_algorithm'])
            st.metric(f"Best {metric_name}", f"{metric_value:.4f}")
        
        # Card 3: Detailed Comparison
        with st.expander("📈 Model Comparison & Visualization", expanded=True):
            st.subheader("Model Leaderboard")
            st.dataframe(analysis_results['comparison_df'].style.highlight_max(axis=0))
            
            # Display visualization if available
            if 'visualization_figure' in analysis_results and analysis_results['visualization_figure'] is not None:
                st.subheader("Performance Visualization")
                st.plotly_chart(analysis_results['visualization_figure'], use_container_width=True)

    # Add AI explanation panel to the right column if active
    # This is the ONLY place where the AI panel is rendered
    if st.session_state.get("ai_active", False):
        with col2:
            render_ai_explanation_panel(st.session_state.structured_results)

if __name__ == "__main__":
    main()

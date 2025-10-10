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

    def log_message(self, message):
        self.log.append(message)
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
            
            self.log_message(f"🔍 Detected encoding: {encoding} (confidence: {confidence:.2f})")
            
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
        self.log_message(f"🔍 Detected file type: {file_type}")
        
        if file_type == 'binary':
            raise ValueError(
                "❌ This appears to be a binary file, not a CSV. \n"
                "Please ensure you're uploading a text-based CSV file. \n"
                "If this should be a CSV, the file may be corrupted."
            )
        
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
                    self.log_message("🔧 Single column detected - attempting to split...")
                    df = self._split_single_column(df)
                
                # Final validation
                if df.shape[0] < 5:  # Need at least 5 rows for ML
                    raise ValueError("Too few rows for machine learning")
                
                if df.shape[1] < 2:  # Need at least 2 columns (feature + target)
                    raise ValueError("Need at least 2 columns for ML (features + target)")
                
                self.log_message(f"✅ Success with strategy #{i+1}: {df.shape[0]} rows, {df.shape[1]} columns")
                return df
                
            except Exception as e:
                last_error = e
                self.log_message(f"⚠️ Strategy #{i+1} failed: {str(e)}")
                continue
        
        # If all strategies failed, provide helpful error message
        raise ValueError(
            f"❌ Could not parse the file successfully.\n\n"
            f"**Issues detected:**\n"
            f"• File might be corrupted or not a proper CSV\n"
            f"• Might have only 1 column (need at least 2 for ML)\n"
            f"• Insufficient data for machine learning\n\n"
            f"**Solutions:**\n"
            f"1. **Check your file**: Open in notepad to verify it's readable text\n"
            f"2. **Ensure multiple columns**: ML needs features + target column\n"
            f"3. **Add more data**: Need at least 10+ rows for analysis\n"
            f"4. **Try Excel format**: Save as .xlsx instead of .csv\n"
            f"5. **Check delimiters**: Ensure data is properly separated\n\n"
            f"Last error: {str(last_error)}"
        )

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


def main():
    st.set_page_config(
        page_title="ML Algorithm Recommender",
        page_icon="🚀",
        layout="wide"
    )
    
    st.markdown("""
    <style>
        .main-title {
            font-size: 3rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: bold;
        }
        .error-box {
            background-color: #ffe6e6;
            border: 2px solid #ff4444;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        .success-box {
            background: linear-gradient(90deg, #4CAF50, #45a049);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-title">🚀 ML Algorithm Recommender</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <strong>Ultra-Robust File Parser</strong> - Handles single columns, missing features, and corrupted files!
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📁 Upload Dataset")
        uploaded_file = st.file_uploader(
            "Choose CSV or Excel file", 
            type=['csv', 'xlsx', 'xls'],
            help="Need at least 2 columns and 10+ rows for ML"
        )
        
        if uploaded_file:
            st.success(f"✅ File loaded: {uploaded_file.name}")
            
            target_column = st.text_input(
                "Target column (optional)", 
                help="Leave blank to auto-detect (uses last column)"
            )
            
            run_analysis = st.button("🚀 Run Analysis", type="primary")
        
        st.markdown("---")
        st.markdown("### 📋 Requirements")
        st.info("""
        **Your dataset needs:**
        - At least 2 columns (features + target)
        - At least 10+ rows
        - Readable text format
        - Consistent structure
        """)
        
        st.markdown("### 🛠️ Auto-Fixes")
        st.markdown("""
        - Single column splitting
        - Feature generation
        - Encoding detection
        - Delimiter auto-detection
        - Error recovery
        """)
    
    # Main content
    if uploaded_file:
        # Show file analysis
        with st.expander("🔍 File Analysis", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📄 Name", uploaded_file.name)
            with col2:
                st.metric("📊 Size", f"{uploaded_file.size / 1024:.1f} KB")
            with col3:
                st.metric("🔧 Type", uploaded_file.type.split('/')[-1].upper())
        
        if run_analysis:
            with st.spinner("🔄 Processing with ultra-robust parser..."):
                try:
                    uploaded_file.seek(0)
                    
                    recommender = IntelligentMLRecommendationSystem()
                    results = recommender.run_complete_analysis(
                        data_source=uploaded_file,
                        target_column=target_column if target_column else None
                    )
                    
                    # Success message
                    st.markdown("""
                    <div class='success-box'>
                        <h2>🎉 Analysis Complete!</h2>
                        <p>Successfully processed and analyzed your dataset!</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.balloons()
                    
                    # Results
                    st.markdown("## 🏆 Results")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🥇 Best Algorithm", results['best_algorithm'])
                    with col2:
                        metric_name = list(results['best_score'].keys())[0]
                        metric_value = list(results['best_score'].values())[0]
                        st.metric(f"📊 {metric_name.title()}", f"{metric_value:.4f}")
                    with col3:
                        st.metric("🎯 Problem", results['problem_type'].replace('_', ' ').title())
                    
                    # Comparison table
                    st.markdown("## 📊 Algorithm Comparison")
                    st.dataframe(results['comparison_df'], use_container_width=True)
                    
                    # Visualizations
                    if results['visualization_figure']:
                        st.markdown("## 📈 Visualizations")
                        st.plotly_chart(results['visualization_figure'], use_container_width=True)
                    
                    # Download results
                    csv_data = results['comparison_df'].to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Results",
                        data=csv_data,
                        file_name=f"ml_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime='text/csv'
                    )
                    
                    # Processing log
                    with st.expander("🔍 Processing Log"):
                        for log_entry in results['log']:
                            if '❌' in log_entry:
                                st.error(log_entry)
                            elif '⚠️' in log_entry:
                                st.warning(log_entry)
                            elif '✅' in log_entry:
                                st.success(log_entry)
                            else:
                                st.info(log_entry)
                    
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
        
        # Help section
        st.markdown("""
        ## 🆘 Common Issues & Solutions
        
        **❌ "No models were successfully trained"**
        - Your dataset likely has only 1 column
        - ML needs multiple columns (features + target)
        - Try adding more columns or use Excel format
        
        **❌ "at least one array or dtype is required"**
        - Usually means no valid features found
        - Check if your data has proper columns
        - Ensure data is not corrupted
        
        **❌ "binary file" error**
        - File is corrupted or not CSV format
        - Try saving as Excel (.xlsx)
        - Open file in notepad to check if readable
        """)

if __name__ == "__main__":
    main()

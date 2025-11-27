# COMPLETE INTELLIGENT ML ALGORITHM RECOMMENDER SYSTEM
# Implements: Auto EDA → Smart Preprocessing → Multi-Algorithm Training → Adaptive Metrics → Visualization

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
import sys

# Add the parent directory to path to allow importing ui_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ui_utils import ConsoleUI, MessageType

warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, KFold
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import (
    RandomForestClassifier, RandomForestRegressor,
    GradientBoostingClassifier, GradientBoostingRegressor,
    AdaBoostClassifier, AdaBoostRegressor
)
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import SVC, SVR
from sklearn.naive_bayes import GaussianNB
import xgboost as xgb
from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.metrics import (
    # Classification metrics
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, confusion_matrix, classification_report, roc_curve,
    # Regression metrics  
    r2_score, mean_squared_error, mean_absolute_error,
    # Clustering metrics
    silhouette_score, calinski_harabasz_score, davies_bouldin_score
)

# AutoEDA libraries
try:
    from ydata_profiling import ProfileReport
    HAS_PROFILING = True
except ImportError:
    HAS_PROFILING = False
    print("⚠️ ydata-profiling not installed. Install with: pip install ydata-profiling")

# AutoML
try:
    from tpot import TPOTClassifier, TPOTRegressor
    HAS_TPOT = True
except ImportError:
    HAS_TPOT = False
    print("⚠️ TPOT not installed. Install with: pip install tpot")

import joblib
import io
from datetime import datetime

class IntelligentMLRecommendationSystem:
    """
    Complete ML Algorithm Recommender with:
    - Auto EDA
    - Smart preprocessing  
    - Problem type detection
    - Adaptive metrics
    - Professional visualization
    """
    
    def __init__(self):
        self.dataset_info = {}
        self.problem_type = None
        self.preprocessing_pipeline = None
        self.trained_models = {}
        self.best_model = None
        self.evaluation_results = {}
        self.profile_report = None
        
        ConsoleUI.print_message("INTELLIGENT ML RECOMMENDATION SYSTEM", MessageType.HEADER)
        ConsoleUI.print_message("Auto EDA • Smart Preprocessing • Adaptive Metrics", MessageType.INFO)
        ConsoleUI.print_message("Multi-Algorithm Training • Professional Visualization", MessageType.INFO)
    
    def load_and_analyze_dataset(self, file_path, target_column=None):
        """
        STEP 1: Load dataset and perform comprehensive auto EDA
        """
        ConsoleUI.print_message("STEP 1: LOADING & ANALYZING DATASET", MessageType.STEP)
        
        # Load dataset
        try:
            if file_path.endswith('.csv'):
                self.df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                self.df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format. Use CSV or Excel.")
            
            ConsoleUI.print_message(
                f"Dataset loaded: {self.df.shape[0]:,} samples, {self.df.shape[1]} features", 
                MessageType.SUCCESS
            )
            
        except Exception as e:
            error_msg = f"Failed to load dataset: {str(e)}"
            ConsoleUI.print_message(error_msg, MessageType.ERROR)
            raise
        
        # Auto-detect target column if not specified
        if target_column is None:
            target_column = self.df.columns[-1]  # Assume last column is target
            ConsoleUI.print_message(
                f"Auto-detected target column: '{target_column}'", 
                MessageType.INFO
            )
        
        # Separate features and target
        self.X = self.df.drop(columns=[target_column])
        self.y = self.df[target_column]
        self.target_column = target_column
        
        # Comprehensive dataset analysis
        self._analyze_dataset_characteristics()
        self._detect_problem_type()
        self._analyze_data_quality()
        
        return self.X, self.y
    
    def _analyze_dataset_characteristics(self):
        """Comprehensive dataset characteristic analysis"""
        
        # Basic information
        self.dataset_info = {
            'n_samples': self.df.shape[0],
            'n_features': self.X.shape[1],
            'target_column': self.target_column,
            'dataset_size_mb': self.df.memory_usage(deep=True).sum() / 1024**2,
        }
        
        # Feature type analysis
        numerical_features = self.X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = self.X.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_features = self.X.select_dtypes(include=['datetime64']).columns.tolist()
        
        self.dataset_info.update({
            'numerical_features': numerical_features,
            'categorical_features': categorical_features,
            'datetime_features': datetime_features,
            'n_numerical': len(numerical_features),
            'n_categorical': len(categorical_features),
            'n_datetime': len(datetime_features),
        })
        
        # Data quality metrics
        missing_info = self.df.isnull().sum()
        self.dataset_info.update({
            'total_missing': missing_info.sum(),
            'missing_percentage': (missing_info.sum() / self.df.size) * 100,
            'features_with_missing': missing_info[missing_info > 0].index.tolist(),
            'constant_features': [col for col in self.X.columns if self.X[col].nunique() <= 1],
        })
        
        # Target analysis
        if self.y.dtype in ['object', 'category']:
            unique_targets = self.y.nunique()
            target_distribution = self.y.value_counts()
            
            self.dataset_info.update({
                'target_type': 'categorical',
                'n_classes': unique_targets,
                'class_distribution': target_distribution.to_dict(),
                'is_balanced': target_distribution.min() / target_distribution.max() > 0.3,
                'target_names': target_distribution.index.tolist()
            })
        else:
            self.dataset_info.update({
                'target_type': 'numerical',
                'target_mean': self.y.mean(),
                'target_std': self.y.std(),
                'target_min': self.y.min(),
                'target_max': self.y.max(),
            })
        
        # Feature correlations (for numerical features only)
        if len(numerical_features) > 1:
            corr_matrix = self.X[numerical_features].corr()
            high_corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > 0.8:
                        high_corr_pairs.append((
                            corr_matrix.columns[i], 
                            corr_matrix.columns[j], 
                            corr_matrix.iloc[i, j]
                        ))
            
            self.dataset_info['high_correlation_pairs'] = high_corr_pairs
            self.dataset_info['avg_feature_correlation'] = np.mean(np.abs(corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)]))
        
        # Print analysis summary
        print(f"📊 Dataset Analysis Summary:")
        print(f"   • Size: {self.dataset_info['n_samples']:,} samples × {self.dataset_info['n_features']} features")
        print(f"   • Memory: {self.dataset_info['dataset_size_mb']:.1f} MB")
        print(f"   • Numerical features: {self.dataset_info['n_numerical']}")
        print(f"   • Categorical features: {self.dataset_info['n_categorical']}")
        print(f"   • Missing values: {self.dataset_info['total_missing']} ({self.dataset_info['missing_percentage']:.1f}%)")
        if self.dataset_info.get('high_correlation_pairs'):
            print(f"   • High correlations: {len(self.dataset_info['high_correlation_pairs'])} pairs")
    
    def _detect_problem_type(self):
        """Intelligent problem type detection"""
        
        if self.dataset_info['target_type'] == 'categorical':
            if self.dataset_info['n_classes'] == 2:
                self.problem_type = 'binary_classification'
                ConsoleUI.print_message(
                    f"Problem Type: BINARY CLASSIFICATION ({self.dataset_info['n_classes']} classes)",
                    MessageType.INFO
                )
            else:
                self.problem_type = 'multiclass_classification'
                ConsoleUI.print_message(
                    f"Problem Type: MULTICLASS CLASSIFICATION ({self.dataset_info['n_classes']} classes)",
                    MessageType.INFO
                )
        else:
            self.problem_type = 'regression'
            ConsoleUI.print_message("Problem Type: REGRESSION (continuous target)", MessageType.INFO)
        
        self.dataset_info['problem_type'] = self.problem_type
    
    def _analyze_data_quality(self):
        """Data quality assessment and recommendations"""
        
        quality_issues = []
        recommendations = []
        
        # Missing values
        if self.dataset_info['missing_percentage'] > 20:
            quality_issues.append("High missing values (>20%)")
            recommendations.append("Consider advanced imputation or feature engineering")
        elif self.dataset_info['missing_percentage'] > 5:
            quality_issues.append("Moderate missing values (5-20%)")
            recommendations.append("Apply appropriate imputation strategies")
        
        # Class imbalance (for classification)
        if self.problem_type in ['binary_classification', 'multiclass_classification']:
            if not self.dataset_info['is_balanced']:
                quality_issues.append("Class imbalance detected")
                recommendations.append("Consider class weighting or resampling techniques")
        
        # High dimensionality
        feature_to_sample_ratio = self.dataset_info['n_features'] / self.dataset_info['n_samples']
        if feature_to_sample_ratio > 0.1:
            quality_issues.append("High dimensionality (many features vs samples)")
            recommendations.append("Feature selection recommended")
        
        # Constant features
        if self.dataset_info['constant_features']:
            quality_issues.append(f"Constant features detected: {len(self.dataset_info['constant_features'])}")
            recommendations.append("Remove constant features")
        
        # High correlations
        if self.dataset_info.get('high_correlation_pairs'):
            quality_issues.append(f"High feature correlations: {len(self.dataset_info['high_correlation_pairs'])} pairs")
            recommendations.append("Consider feature selection or PCA")
        
        self.dataset_info['quality_issues'] = quality_issues
        self.dataset_info['recommendations'] = recommendations
        
        if quality_issues:
            ConsoleUI.print_message("Data Quality Issues:", MessageType.WARNING)
            for issue in quality_issues:
                ConsoleUI.print_message(issue, MessageType.RESULT)
            
            ConsoleUI.print_message("Recommendations:", MessageType.INFO)
            for rec in recommendations:
                ConsoleUI.print_message(rec, MessageType.RESULT)
    
    def generate_auto_eda_report(self):
        """Generate comprehensive EDA report (optional)"""
        
        if not HAS_PROFILING:
            ConsoleUI.print_message(
                "ydata-profiling not available. Install with: pip install ydata-profiling",
                MessageType.WARNING
            )
            return
        
        ConsoleUI.print_message("GENERATING AUTO EDA REPORT...", MessageType.INFO)
        
        try:
            # Generate profile report
            self.profile_report = ProfileReport(
                self.df,
                title="Automated Dataset Analysis Report",
                explorative=True,
                minimal=False,
                samples={"head": 5, "tail": 5}
            )
            
            # Save report
            report_filename = f"eda_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            self.profile_report.to_file(report_filename)
            ConsoleUI.print_message(
                f"Detailed EDA report saved: {report_filename}",
                MessageType.SUCCESS
            )
            return report_filename
            
        except Exception as e:
            error_msg = f"Failed to generate EDA report: {str(e)}"
            ConsoleUI.print_message(error_msg, MessageType.ERROR)
            return None
    
    def create_intelligent_preprocessing_pipeline(self):
        """
        STEP 2: Create smart preprocessing pipeline based on data characteristics
        """
        print("\n🔧 STEP 2: CREATING INTELLIGENT PREPROCESSING PIPELINE")
        print("=" * 50)
        
        numerical_features = self.dataset_info['numerical_features']
        categorical_features = self.dataset_info['categorical_features']
        
        # Numerical preprocessing pipeline
        numerical_steps = [('imputer', SimpleImputer(strategy='median'))]
        
        # Choose scaler based on data characteristics
        if self.dataset_info.get('avg_feature_correlation', 0) > 0.5:
            numerical_steps.append(('scaler', StandardScaler()))
            print("   ✅ Using StandardScaler (high correlation detected)")
        else:
            numerical_steps.append(('scaler', MinMaxScaler()))
            print("   ✅ Using MinMaxScaler (low correlation)")
        
        numerical_transformer = Pipeline(steps=numerical_steps)
        
        # Categorical preprocessing pipeline
        categorical_steps = [('imputer', SimpleImputer(strategy='most_frequent'))]
        
        # Choose encoding based on cardinality
        max_cardinality = max([self.X[col].nunique() for col in categorical_features]) if categorical_features else 0
        
        if max_cardinality > 10:
            # High cardinality - use label encoding
            categorical_steps.append(('encoder', LabelEncoder()))
            print(f"   ✅ Using LabelEncoder (high cardinality: {max_cardinality})")
        else:
            # Low cardinality - use one-hot encoding
            categorical_steps.append(('encoder', OneHotEncoder(drop='first', sparse=False)))
            print(f"   ✅ Using OneHotEncoder (low cardinality: {max_cardinality})")
        
        categorical_transformer = Pipeline(steps=categorical_steps)
        
        # Combine preprocessing
        preprocessing_steps = []
        
        if numerical_features:
            preprocessing_steps.append(('num', numerical_transformer, numerical_features))
        if categorical_features:
            preprocessing_steps.append(('cat', categorical_transformer, categorical_features))
        
        preprocessor = ColumnTransformer(transformers=preprocessing_steps)
        
        # Add feature selection if high dimensionality
        pipeline_steps = [('preprocessor', preprocessor)]
        
        if self.dataset_info['n_features'] / self.dataset_info['n_samples'] > 0.1:
            n_features_to_select = min(50, int(self.dataset_info['n_samples'] * 0.1))
            
            if self.problem_type == 'regression':
                feature_selector = SelectKBest(f_regression, k=n_features_to_select)
            else:
                feature_selector = SelectKBest(f_classif, k=n_features_to_select)
            
            pipeline_steps.append(('feature_selection', feature_selector))
            print(f"   ✅ Added feature selection (selecting top {n_features_to_select} features)")
        
        # Remove constant features
        if self.dataset_info['constant_features']:
            pipeline_steps.insert(-1 if len(pipeline_steps) > 1 else 0, 
                                 ('variance_filter', VarianceThreshold()))
            print("   ✅ Added variance threshold (removing constant features)")
        
        self.preprocessing_pipeline = Pipeline(steps=pipeline_steps)
        
        print(f"   ✅ Preprocessing pipeline created with {len(pipeline_steps)} steps")
        return self.preprocessing_pipeline
    
    def select_algorithms_by_problem_type(self):
        """
        STEP 3: Select appropriate algorithms based on problem type and dataset characteristics
        """
        ConsoleUI.print_message(
            f"STEP 3: SELECTING ALGORITHMS FOR {self.problem_type.upper()}", 
            MessageType.STEP
        )
        
        algorithms = {}
        
        # Common parameters
        class_weight = 'balanced' if not self.dataset_info.get('is_balanced', True) else None
        
        if self.problem_type in ['binary_classification', 'multiclass_classification']:
            # Enhanced classification algorithms
            multi_class = 'ovr' if self.problem_type == 'binary_classification' else 'multinomial'
            eval_metric = 'logloss' if self.problem_type == 'binary_classification' else 'mlogloss'
            
            algorithms = {
                # Linear models
                'Logistic Regression': LogisticRegression(
                    random_state=42, max_iter=1000, multi_class=multi_class,
                    class_weight=class_weight, solver='lbfgs'
                ),
                'Ridge Classifier': RidgeClassifier(
                    random_state=42, class_weight=class_weight
                ),
                
                # Tree-based models
                'Random Forest': RandomForestClassifier(
                    random_state=42, n_estimators=100, class_weight=class_weight
                ),
                'Gradient Boosting': GradientBoostingClassifier(
                    random_state=42, n_estimators=100, learning_rate=0.1
                ),
                'XGBoost': xgb.XGBClassifier(
                    random_state=42, eval_metric=eval_metric, verbosity=0,
                    use_label_encoder=False, scale_pos_weight=1 if class_weight is None else (sum(self.y == 0) / sum(self.y == 1) if class_weight == 'balanced' else 1)
                ),
                'LightGBM': LGBMClassifier(
                    random_state=42, n_estimators=100, class_weight=class_weight
                ),
                
                # Other models
                'SVM': SVC(
                    random_state=42, probability=True, class_weight=class_weight
                ),
                'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
                'Naive Bayes': GaussianNB(),
                'AdaBoost': AdaBoostClassifier(
                    random_state=42, n_estimators=50
                )
            }
            
        else:  # Regression
            algorithms = {
                # Linear models
                'Linear Regression': LinearRegression(),
                'Ridge': Ridge(random_state=42),
                'Lasso': Lasso(random_state=42, max_iter=5000),
                'ElasticNet': ElasticNet(random_state=42, max_iter=5000),
                
                # Tree-based models
                'Random Forest': RandomForestRegressor(random_state=42, n_estimators=100),
                'Gradient Boosting': GradientBoostingRegressor(
                    random_state=42, n_estimators=100, learning_rate=0.1
                ),
                'XGBoost': xgb.XGBRegressor(random_state=42, verbosity=0),
                'LightGBM': LGBMRegressor(random_state=42, n_estimators=100),
                
                # Other models
                'SVR': SVR(),
                'K-Neighbors': KNeighborsRegressor(n_neighbors=5),
                'AdaBoost': AdaBoostRegressor(random_state=42, n_estimators=50)
            }
        
        # Filter algorithms based on dataset size
        is_small_dataset = self.dataset_info['n_samples'] < 1000
        
        if is_small_dataset:
            ConsoleUI.print_message(
                "Small dataset detected - using simplified models", 
                MessageType.WARNING
            )
            # For small datasets, prefer simpler models
            complex_models = ['XGBoost', 'LightGBM', 'Gradient Boosting']
            for model in complex_models:
                if model in algorithms:
                    del algorithms[model]
        
        # Ensure we have exactly 7 algorithms
        if len(algorithms) > 7:
            # If we have too many, prioritize based on problem type
            priority_order = {
                'binary_classification': [
                    'Logistic Regression', 'Random Forest', 'SVM',
                    'Decision Tree', 'K-Nearest Neighbors', 'Naive Bayes', 'AdaBoost'
                ],
                'multiclass_classification': [
                    'Logistic Regression', 'Random Forest', 'SVM',
                    'Decision Tree', 'K-Nearest Neighbors', 'Naive Bayes', 'AdaBoost'
                ],
                'regression': [
                    'Linear Regression', 'Random Forest', 'SVR',
                    'Decision Tree', 'K-Neighbors', 'Ridge', 'Lasso'
                ]
            }
            
            # Get the top 7 algorithms for the current problem type
            priority_list = priority_order.get(self.problem_type, list(algorithms.keys()))
            selected_keys = [algo for algo in priority_list if algo in algorithms][:7]
            algorithms = {k: algorithms[k] for k in selected_keys}
        
        # Log selected algorithms
        ConsoleUI.print_message(f"Selected {len(algorithms)} algorithms:", MessageType.INFO)
        for i, name in enumerate(algorithms.keys(), 1):
            ConsoleUI.print_message(f"{i}. {name}", MessageType.RESULT)
        
        return algorithms
    
    def train_and_evaluate_models(self):
        """
        STEP 4: Train multiple algorithms with cross-validation and appropriate metrics
        """
        print(f"\n📊 STEP 4: TRAINING & EVALUATING MODELS")
        print("=" * 50)
        
        # Get algorithms
        algorithms = self.select_algorithms_by_problem_type()
        
        # Train/test split with stratification for classification
        if self.problem_type in ['binary_classification', 'multiclass_classification']:
            X_train, X_test, y_train, y_test = train_test_split(
                self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
            )
            cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                self.X, self.y, test_size=0.2, random_state=42
            )
            cv = KFold(n_splits=5, shuffle=True, random_state=42)
        
        print(f"   📈 Training set: {len(X_train)} samples")
        print(f"   📈 Test set: {len(X_test)} samples")
        print(f"   🔄 Cross-validation: {cv.n_splits}-fold")
        
        results = {}
        
        # Train each algorithm
        for name, algorithm in algorithms.items():
            print(f"\n   🤖 Training {name}...")
            
            # Create complete pipeline
            complete_pipeline = Pipeline([
                ('preprocessing', self.preprocessing_pipeline),
                ('algorithm', algorithm)
            ])
            
            try:
                # Cross-validation with appropriate scoring
                if self.problem_type == 'binary_classification':
                    cv_scores_acc = cross_val_score(complete_pipeline, X_train, y_train, cv=cv, scoring='accuracy', n_jobs=-1)
                    cv_scores_auc = cross_val_score(complete_pipeline, X_train, y_train, cv=cv, scoring='roc_auc', n_jobs=-1)
                    cv_scores_f1 = cross_val_score(complete_pipeline, X_train, y_train, cv=cv, scoring='f1', n_jobs=-1)
                    
                elif self.problem_type == 'multiclass_classification':
                    cv_scores_acc = cross_val_score(complete_pipeline, X_train, y_train, cv=cv, scoring='accuracy', n_jobs=-1)
                    cv_scores_f1 = cross_val_score(complete_pipeline, X_train, y_train, cv=cv, scoring='f1_macro', n_jobs=-1)
                    cv_scores_auc = None  # Not directly applicable to multiclass
                    
                elif self.problem_type == 'regression':
                    cv_scores_r2 = cross_val_score(complete_pipeline, X_train, y_train, cv=cv, scoring='r2', n_jobs=-1)
                    cv_scores_mae = cross_val_score(complete_pipeline, X_train, y_train, cv=cv, scoring='neg_mean_absolute_error', n_jobs=-1)
                    cv_scores_rmse = cross_val_score(complete_pipeline, X_train, y_train, cv=cv, scoring='neg_mean_squared_error', n_jobs=-1)
                    cv_scores_rmse = np.sqrt(-cv_scores_rmse)  # Convert to positive RMSE
                
                # Train on full training set
                complete_pipeline.fit(X_train, y_train)
                
                # Test predictions
                y_pred = complete_pipeline.predict(X_test)
                
                # Calculate test metrics based on problem type
                if self.problem_type == 'binary_classification':
                    test_accuracy = accuracy_score(y_test, y_pred)
                    test_precision = precision_score(y_test, y_pred, average='binary')
                    test_recall = recall_score(y_test, y_pred, average='binary')
                    test_f1 = f1_score(y_test, y_pred, average='binary')
                    
                    # Get probabilities for AUC
                    try:
                        y_pred_proba = complete_pipeline.predict_proba(X_test)[:, 1]
                        test_auc = roc_auc_score(y_test, y_pred_proba)
                    except:
                        y_pred_proba = None
                        test_auc = None
                    
                    results[name] = {
                        'pipeline': complete_pipeline,
                        'cv_accuracy': cv_scores_acc,
                        'cv_f1': cv_scores_f1,
                        'cv_auc': cv_scores_auc,
                        'test_accuracy': test_accuracy,
                        'test_precision': test_precision,
                        'test_recall': test_recall,
                        'test_f1': test_f1,
                        'test_auc': test_auc,
                        'y_pred': y_pred,
                        'y_pred_proba': y_pred_proba,
                        'primary_metric': test_accuracy,
                        'primary_metric_name': 'Accuracy'
                    }
                    
                elif self.problem_type == 'multiclass_classification':
                    test_accuracy = accuracy_score(y_test, y_pred)
                    test_precision = precision_score(y_test, y_pred, average='macro')
                    test_recall = recall_score(y_test, y_pred, average='macro')
                    test_f1 = f1_score(y_test, y_pred, average='macro')
                    
                    # Multiclass AUC (one-vs-rest)
                    try:
                        y_pred_proba = complete_pipeline.predict_proba(X_test)
                        test_auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr')
                    except:
                        y_pred_proba = None
                        test_auc = None
                    
                    results[name] = {
                        'pipeline': complete_pipeline,
                        'cv_accuracy': cv_scores_acc,
                        'cv_f1': cv_scores_f1,
                        'test_accuracy': test_accuracy,
                        'test_precision': test_precision,
                        'test_recall': test_recall,
                        'test_f1': test_f1,
                        'test_auc': test_auc,
                        'y_pred': y_pred,
                        'y_pred_proba': y_pred_proba,
                        'primary_metric': test_f1,  # Use F1 as primary for multiclass
                        'primary_metric_name': 'F1-Score (Macro)'
                    }
                    
                elif self.problem_type == 'regression':
                    test_r2 = r2_score(y_test, y_pred)
                    test_mse = mean_squared_error(y_test, y_pred)
                    test_rmse = np.sqrt(test_mse)
                    test_mae = mean_absolute_error(y_test, y_pred)
                    
                    results[name] = {
                        'pipeline': complete_pipeline,
                        'cv_r2': cv_scores_r2,
                        'cv_mae': -cv_scores_mae,  # Convert back to positive
                        'cv_rmse': cv_scores_rmse,
                        'test_r2': test_r2,
                        'test_mse': test_mse,
                        'test_rmse': test_rmse,
                        'test_mae': test_mae,
                        'y_pred': y_pred,
                        'primary_metric': test_r2,
                        'primary_metric_name': 'R² Score'
                    }
                
                # Print results
                if self.problem_type in ['binary_classification', 'multiclass_classification']:
                    print(f"      ✅ CV Accuracy: {cv_scores_acc.mean():.4f} ± {cv_scores_acc.std():.4f}")
                    print(f"      ✅ Test Accuracy: {results[name]['test_accuracy']:.4f}")
                    print(f"      ✅ Test F1: {results[name]['test_f1']:.4f}")
                    if results[name].get('test_auc'):
                        print(f"      ✅ Test AUC: {results[name]['test_auc']:.4f}")
                else:
                    print(f"      ✅ CV R²: {cv_scores_r2.mean():.4f} ± {cv_scores_r2.std():.4f}")
                    print(f"      ✅ Test R²: {results[name]['test_r2']:.4f}")
                    print(f"      ✅ Test RMSE: {results[name]['test_rmse']:.4f}")
                
            except Exception as e:
                print(f"      ❌ Training failed: {str(e)}")
                continue
        
        # Store results and test data
        self.trained_models = results
        self.test_data = (X_test, y_test)
        
        print(f"\n✅ Successfully trained {len(results)} algorithms")
        return results
    
    def analyze_and_rank_results(self):
        """
        STEP 5: Analyze results and select best model
        """
        print(f"\n🏆 STEP 5: ANALYZING RESULTS & RANKING MODELS")
        print("=" * 50)
        
        if not self.trained_models:
            print("❌ No trained models to analyze")
            return None, None
        
        # Create comparison dataframe
        comparison_data = []
        
        for name, result in self.trained_models.items():
            if self.problem_type in ['binary_classification', 'multiclass_classification']:
                row = {
                    'Algorithm': name,
                    'Primary_Metric': result['primary_metric'],
                    'Primary_Metric_Name': result['primary_metric_name'],
                    'Test_Accuracy': result['test_accuracy'],
                    'Test_Precision': result['test_precision'],
                    'Test_Recall': result['test_recall'],
                    'Test_F1': result['test_f1'],
                    'CV_Accuracy_Mean': result['cv_accuracy'].mean(),
                    'CV_Accuracy_Std': result['cv_accuracy'].std(),
                }
                if 'test_auc' in result and result['test_auc'] is not None:
                    row['Test_AUC'] = result['test_auc']
                    
            else:  # regression
                row = {
                    'Algorithm': name,
                    'Primary_Metric': result['primary_metric'],
                    'Primary_Metric_Name': result['primary_metric_name'],
                    'Test_R2': result['test_r2'],
                    'Test_RMSE': result['test_rmse'],
                    'Test_MAE': result['test_mae'],
                    'CV_R2_Mean': result['cv_r2'].mean(),
                    'CV_R2_Std': result['cv_r2'].std(),
                }
            
            comparison_data.append(row)
        
        # Create comparison dataframe and sort by primary metric
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df = comparison_df.sort_values('Primary_Metric', ascending=False)
        
        # Display results table
        print("📊 Algorithm Performance Ranking:")
        print("=" * 70)
        
        if self.problem_type in ['binary_classification', 'multiclass_classification']:
            display_cols = ['Algorithm', 'Test_Accuracy', 'Test_F1', 'CV_Accuracy_Mean', 'CV_Accuracy_Std']
            if 'Test_AUC' in comparison_df.columns:
                display_cols.insert(-2, 'Test_AUC')
        else:
            display_cols = ['Algorithm', 'Test_R2', 'Test_RMSE', 'Test_MAE', 'CV_R2_Mean', 'CV_R2_Std']
        
        print(comparison_df[display_cols].round(4).to_string(index=False))
        
        # Select best model
        best_algorithm_name = comparison_df.iloc[0]['Algorithm']
        self.best_model = self.trained_models[best_algorithm_name]
        self.best_algorithm_name = best_algorithm_name
        
        print(f"\n🥇 BEST ALGORITHM: {best_algorithm_name}")
        print(f"   📊 {self.best_model['primary_metric_name']}: {self.best_model['primary_metric']:.4f}")
        
        # Calculate performance insights
        self._generate_performance_insights(comparison_df)
        
        return best_algorithm_name, comparison_df
    
    def _generate_performance_insights(self, comparison_df):
        """Generate intelligent performance insights"""
        
        print(f"\n💡 PERFORMANCE INSIGHTS:")
        
        # Top performers
        top_3 = comparison_df.head(3)['Algorithm'].tolist()
        print(f"   🏆 Top 3 performers: {', '.join(top_3)}")
        
        # Performance spread
        primary_scores = comparison_df['Primary_Metric'].values
        performance_spread = primary_scores.max() - primary_scores.min()
        
        if performance_spread < 0.05:
            print(f"   📊 Close competition: All algorithms within {performance_spread:.3f} performance")
        else:
            print(f"   📊 Clear winner: {performance_spread:.3f} performance gap")
        
        # Stability analysis
        if self.problem_type in ['binary_classification', 'multiclass_classification']:
            cv_stds = comparison_df['CV_Accuracy_Std'].values
        else:
            cv_stds = comparison_df['CV_R2_Std'].values
        
        most_stable = comparison_df.iloc[cv_stds.argmin()]['Algorithm']
        print(f"   🎯 Most stable: {most_stable} (lowest CV std)")
        
        # Algorithm-specific insights
        if 'Random Forest' in comparison_df['Algorithm'].values:
            rf_rank = comparison_df[comparison_df['Algorithm'] == 'Random Forest'].index[0] + 1
            if rf_rank <= 3:
                print(f"   🌲 Random Forest (#{rf_rank}): Good for interpretability + performance balance")
        
        if 'Logistic Regression' in comparison_df['Algorithm'].values:
            lr_rank = comparison_df[comparison_df['Algorithm'] == 'Logistic Regression'].index[0] + 1
            if lr_rank <= 3:
                print(f"   📈 Logistic Regression (#{lr_rank}): Excellent interpretability for medical use")
    
    def create_comprehensive_visualizations(self):
        """
        STEP 6: Create problem-type specific visualizations
        """
        print(f"\n📈 STEP 6: GENERATING COMPREHENSIVE VISUALIZATIONS")
        print("=" * 50)
        
        if not self.trained_models:
            print("❌ No trained models to visualize")
            return
        
        # Determine figure layout based on problem type
        if self.problem_type in ['binary_classification', 'multiclass_classification']:
            fig, axes = plt.subplots(3, 2, figsize=(20, 15))
            self._create_classification_plots(axes)
        else:
            fig, axes = plt.subplots(2, 2, figsize=(18, 12))
            self._create_regression_plots(axes)
        
        plt.tight_layout()
        
        # Save visualization
        viz_filename = f"ml_analysis_{self.problem_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(viz_filename, dpi=300, bbox_inches='tight')
        print(f"✅ Visualizations saved: {viz_filename}")
        plt.show()
    
    def _create_classification_plots(self, axes):
        """Create classification-specific plots"""
        
        X_test, y_test = self.test_data
        algorithm_names = list(self.trained_models.keys())
        
        # 1. Algorithm Performance Comparison
        ax1 = axes[0, 0]
        primary_metrics = [self.trained_models[name]['primary_metric'] for name in algorithm_names]
        colors = ['gold' if name == self.best_algorithm_name else 'lightblue' for name in algorithm_names]
        
        bars = ax1.bar(algorithm_names, primary_metrics, color=colors)
        ax1.set_title('Algorithm Performance Comparison', fontsize=14, fontweight='bold')
        ax1.set_ylabel(self.best_model['primary_metric_name'])
        ax1.tick_params(axis='x', rotation=45)
        
        for bar, score in zip(bars, primary_metrics):
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01,
                     f'{score:.3f}', ha='center', va='bottom')
        
        # 2. Confusion Matrix for Best Model
        ax2 = axes[0, 1]
        y_pred_best = self.best_model['y_pred']
        cm = confusion_matrix(y_test, y_pred_best)
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax2)
        ax2.set_title(f'Confusion Matrix - {self.best_algorithm_name}', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Predicted')
        ax2.set_ylabel('Actual')
        
        # 3. ROC Curves (for binary classification)
        ax3 = axes[1, 0]
        if self.problem_type == 'binary_classification':
            for name in algorithm_names:
                result = self.trained_models[name]
                if result.get('y_pred_proba') is not None:
                    fpr, tpr, _ = roc_curve(y_test, result['y_pred_proba'])
                    auc_score = result['test_auc']
                    line_width = 3 if name == self.best_algorithm_name else 1
                    ax3.plot(fpr, tpr, label=f'{name} (AUC = {auc_score:.3f})', linewidth=line_width)
            
            ax3.plot([0, 1], [0, 1], 'k--', label='Random')
            ax3.set_xlabel('False Positive Rate')
            ax3.set_ylabel('True Positive Rate')
            ax3.set_title('ROC Curves Comparison', fontsize=14, fontweight='bold')
            ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax3.grid(True, alpha=0.3)
        else:
            # Multiclass - show precision-recall per class
            ax3.text(0.5, 0.5, 'Multiclass Classification\nROC curves less informative', 
                    ha='center', va='center', transform=ax3.transAxes, fontsize=12)
            ax3.set_title('ROC Analysis (Multiclass)', fontsize=14, fontweight='bold')
        
        # 4. Cross-Validation Stability
        ax4 = axes[1, 1]
        cv_means = [self.trained_models[name]['cv_accuracy'].mean() for name in algorithm_names]
        cv_stds = [self.trained_models[name]['cv_accuracy'].std() for name in algorithm_names]
        
        ax4.bar(algorithm_names, cv_means, yerr=cv_stds, capsize=5, color='lightgreen', alpha=0.7)
        ax4.set_title('Cross-Validation Accuracy (5-Fold)', fontsize=14, fontweight='bold')
        ax4.set_ylabel('CV Accuracy')
        ax4.tick_params(axis='x', rotation=45)
        
        # 5. Precision vs Recall
        ax5 = axes[2, 0]
        precisions = [self.trained_models[name]['test_precision'] for name in algorithm_names]
        recalls = [self.trained_models[name]['test_recall'] for name in algorithm_names]
        
        scatter = ax5.scatter(precisions, recalls, s=100, alpha=0.7, c=primary_metrics, cmap='viridis')
        for i, name in enumerate(algorithm_names):
            ax5.annotate(name, (precisions[i], recalls[i]), xytext=(5, 5), 
                        textcoords='offset points', fontsize=9)
        
        ax5.set_xlabel('Precision')
        ax5.set_ylabel('Recall')
        ax5.set_title('Precision vs Recall Trade-off', fontsize=14, fontweight='bold')
        ax5.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax5, label=self.best_model['primary_metric_name'])
        
        # 6. F1-Score Comparison
        ax6 = axes[2, 1]
        f1_scores = [self.trained_models[name]['test_f1'] for name in algorithm_names]
        colors_f1 = plt.cm.viridis(np.linspace(0, 1, len(algorithm_names)))
        
        bars = ax6.barh(algorithm_names, f1_scores, color=colors_f1)
        ax6.set_title('F1-Score Comparison', fontsize=14, fontweight='bold')
        ax6.set_xlabel('F1-Score')
        
        for bar, score in zip(bars, f1_scores):
            ax6.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2.,
                     f'{score:.3f}', ha='left', va='center')
    
    def _create_regression_plots(self, axes):
        """Create regression-specific plots"""
        
        X_test, y_test = self.test_data
        algorithm_names = list(self.trained_models.keys())
        
        # 1. Algorithm Performance Comparison (R²)
        ax1 = axes[0, 0]
        r2_scores = [self.trained_models[name]['test_r2'] for name in algorithm_names]
        colors = ['gold' if name == self.best_algorithm_name else 'lightblue' for name in algorithm_names]
        
        bars = ax1.bar(algorithm_names, r2_scores, color=colors)
        ax1.set_title('Algorithm Performance (R² Score)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('R² Score')
        ax1.tick_params(axis='x', rotation=45)
        
        for bar, score in zip(bars, r2_scores):
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01,
                     f'{score:.3f}', ha='center', va='bottom')
        
        # 2. Actual vs Predicted for Best Model
        ax2 = axes[0, 1]
        y_pred_best = self.best_model['y_pred']
        
        # Plot the perfect prediction line
        min_val = min(min(y_test), min(y_pred_best))
        max_val = max(max(y_test), max(y_pred_best))
        ax2.plot([min_val, max_val], [min_val, max_val], 'r--', alpha=0.5)
        
        # Plot the actual vs predicted points
        ax2.scatter(y_test, y_pred_best, alpha=0.5)
        ax2.set_xlabel('Actual Values')
        ax2.set_ylabel('Predicted Values')
        ax2.set_title(f'Actual vs Predicted - {self.best_algorithm_name}', fontsize=14, fontweight='bold')
        
        # 3. Residual Plot for Best Model
        ax3 = axes[1, 0]
        residuals = y_test - y_pred_best
        ax3.scatter(y_pred_best, residuals, alpha=0.5)
        ax3.axhline(y=0, color='r', linestyle='--', alpha=0.5)
        ax3.set_xlabel('Predicted Values')
        ax3.set_ylabel('Residuals')
        ax3.set_title('Residual Plot', fontsize=14, fontweight='bold')
        
        # 4. Error Comparison
        ax4 = axes[1, 1]
        rmse_scores = [self.trained_models[name]['test_rmse'] for name in algorithm_names]
        mae_scores = [self.trained_models[name]['test_mae'] for name in algorithm_names]
        
        x = np.arange(len(algorithm_names))
        width = 0.35
        
        bars1 = ax4.bar(x - width/2, rmse_scores, width, label='RMSE', color='lightcoral')
        bars2 = ax4.bar(x + width/2, mae_scores, width, label='MAE', color='lightseagreen')
        
        ax4.set_xticks(x)
        ax4.set_xticklabels(algorithm_names, rotation=45, ha='right')
        ax4.set_ylabel('Error')
        ax4.set_title('Error Metrics Comparison', fontsize=14, fontweight='bold')
        ax4.legend()
        
        # Add value labels on top of bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                         f'{height:.3f}', ha='center', va='bottom')
    
    def save_best_model(self, filename='best_model.pkl'):
        """Save the best performing model to disk"""
        if not hasattr(self, 'best_model'):
            print("❌ No best model available. Train models first.")
            return
        
        joblib.dump(self.best_model['pipeline'], filename)
        print(f"✅ Best model saved as {filename}")
    
    def run_automated_ml(self, file_path, target_column=None, generate_eda=True):
        """
        Complete end-to-end ML pipeline execution
        """
        print("\n🚀 STARTING AUTOMATED ML PIPELINE")
        print("=" * 50)
        
        # Step 1: Load and analyze dataset
        self.load_and_analyze_dataset(file_path, target_column)
        
        # Optional: Generate EDA report
        if generate_eda and HAS_PROFILING:
            self.generate_auto_eda_report()
        
        # Step 2: Create preprocessing pipeline
        self.create_intelligent_preprocessing_pipeline()
        
        # Step 3-4: Train and evaluate models
        self.train_and_evaluate_models()
        
        # Step 5: Analyze and rank results
        best_model, comparison_df = self.analyze_and_rank_results()
        
        # Step 6: Create visualizations
        self.create_comprehensive_visualizations()
        
        # Save the best model
        self.save_best_model()
        
        print("\n✨ AUTOMATED ML PIPELINE COMPLETED SUCCESSFULLY!")
        return best_model, comparison_df

# Example usage
if __name__ == "__main__":
    # Example for classification
    print("🔍 EXAMPLE: CLASSIFICATION WITH IRIS DATASET")
    from sklearn.datasets import load_iris
    import pandas as pd
    
    # Load sample dataset
    data = load_iris()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target
    
    # Save to CSV for demonstration
    df.to_csv('iris_demo.csv', index=False)
    
    # Initialize and run the recommender
    recommender = IntelligentMLRecommendationSystem()
    best_model, results = recommender.run_automated_ml(
        file_path='iris_demo.csv',
        target_column='target',
        generate_eda=False  # Set to True if ydata-profiling is installed
    )

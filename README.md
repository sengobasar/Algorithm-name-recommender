<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Powered ML Algorithm Recommender</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
            overflow-x: hidden;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Hero Section */
        .hero {
            text-align: center;
            padding: 60px 20px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            margin: 40px 0;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: fadeInUp 1s ease-out;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .hero h1 {
            font-size: 3em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        .hero .tagline {
            font-size: 1.3em;
            color: #555;
            margin: 20px 0;
        }

        .badges {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin: 30px 0;
        }

        .badge {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            animation: float 3s ease-in-out infinite;
        }

        .badge:nth-child(2) { animation-delay: 0.5s; }
        .badge:nth-child(3) { animation-delay: 1s; }
        .badge:nth-child(4) { animation-delay: 1.5s; }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        /* AI Highlight Section */
        .ai-section {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 40px;
            border-radius: 20px;
            margin: 40px 0;
            color: white;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
            animation: slideInLeft 1s ease-out;
        }

        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .ai-section h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }

        .ai-features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .ai-card {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            padding: 25px;
            border-radius: 15px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .ai-card:hover {
            transform: translateY(-10px) scale(1.05);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }

        .ai-card h3 {
            font-size: 1.5em;
            margin-bottom: 10px;
        }

        /* Features Grid */
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }

        .feature-card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            animation: fadeIn 1s ease-out;
        }

        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .feature-card h3 {
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 15px;
        }

        /* Process Flow */
        .process-flow {
            background: white;
            padding: 40px;
            border-radius: 20px;
            margin: 40px 0;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
        }

        .process-flow h2 {
            text-align: center;
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 40px;
        }

        .steps {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            position: relative;
        }

        .step {
            flex: 1;
            min-width: 150px;
            text-align: center;
            padding: 20px;
            position: relative;
        }

        .step-number {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            font-weight: bold;
            margin: 0 auto 15px;
            animation: bounce 2s ease-in-out infinite;
        }

        .step:nth-child(2) .step-number { animation-delay: 0.3s; }
        .step:nth-child(3) .step-number { animation-delay: 0.6s; }
        .step:nth-child(4) .step-number { animation-delay: 0.9s; }
        .step:nth-child(5) .step-number { animation-delay: 1.2s; }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }

        /* Code Block */
        .code-block {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 30px;
            border-radius: 15px;
            margin: 40px 0;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
            animation: slideInRight 1s ease-out;
        }

        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .code-block pre {
            margin: 0;
            line-height: 1.8;
        }

        .code-comment {
            color: #6272a4;
        }

        .code-command {
            color: #50fa7b;
        }

        /* CTA Button */
        .cta-button {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border-radius: 50px;
            text-decoration: none;
            font-size: 1.2em;
            font-weight: bold;
            margin: 20px 10px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }

        .cta-button:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 50px rgba(102, 126, 234, 0.6);
        }

        /* Stats Section */
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }

        .stat-card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            animation: scaleIn 0.8s ease-out;
        }

        @keyframes scaleIn {
            from {
                transform: scale(0.8);
                opacity: 0;
            }
            to {
                transform: scale(1);
                opacity: 1;
            }
        }

        .stat-number {
            font-size: 3em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .stat-label {
            font-size: 1.1em;
            color: #666;
            margin-top: 10px;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2em;
            }
            
            .steps {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Hero Section -->
        <div class="hero">
            <h1>🤖 AI-Powered ML Algorithm Recommender</h1>
            <p class="tagline">Smart, Transparent, One-Click Machine Learning Pipeline</p>
            <div class="badges">
                <span class="badge">🧠 AI-Driven</span>
                <span class="badge">⚡ Instant Analysis</span>
                <span class="badge">📊 21 Algorithms</span>
                <span class="badge">🎯 Zero Config</span>
            </div>
            <div>
                <a href="#quick-start" class="cta-button">🚀 Get Started</a>
                <a href="https://github.com/sengobasar/Algorithm-name-recommender" class="cta-button">📦 GitHub</a>
            </div>
        </div>

        <!-- AI Highlight Section -->
        <div class="ai-section">
            <h2>🧠 Why AI-Powered?</h2>
            <p style="font-size: 1.2em; margin-bottom: 20px;">
                Unlike traditional AutoML tools that work as black boxes, our system uses <strong>intelligent AI agents</strong> 
                to make transparent, adaptive decisions at every step. Here's the AI magic:
            </p>
            
            <div class="ai-features">
                <div class="ai-card">
                    <h3>🎯 Smart Detection</h3>
                    <p>AI analyzes target distribution, detects problem type (binary/multiclass/regression) and adapts the entire pipeline automatically</p>
                </div>
                <div class="ai-card">
                    <h3>🔧 Adaptive Pipeline</h3>
                    <p>Intelligent preprocessing based on skewness, collinearity, feature types—not generic fixed pipelines</p>
                </div>
                <div class="ai-card">
                    <h3>⚙️ Dynamic Selection</h3>
                    <p>AI picks 7 best algorithms from 21 candidates based on dataset size, balance, and characteristics</p>
                </div>
                <div class="ai-card">
                    <h3>📈 Transparent Reasoning</h3>
                    <p>Unlike black-box AutoML, see <strong>why</strong> each decision was made—perfect for learning and trust</p>
                </div>
            </div>
        </div>

        <!-- Stats -->
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">21</div>
                <div class="stat-label">ML Algorithms</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">5</div>
                <div class="stat-label">Cross-Validation Folds</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">1</div>
                <div class="stat-label">Click to Results</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">100%</div>
                <div class="stat-label">Transparent</div>
            </div>
        </div>

        <!-- Process Flow -->
        <div class="process-flow">
            <h2>⚡ How It Works in 5 Steps</h2>
            <div class="steps">
                <div class="step">
                    <div class="step-number">1</div>
                    <h3>📁 Upload</h3>
                    <p>Drop messy CSV/Excel—AI handles broken formats, encodings</p>
                </div>
                <div class="step">
                    <div class="step-number">2</div>
                    <h3>🔍 Analyze</h3>
                    <p>AI detects types, skewness, collinearity, missing patterns</p>
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    <h3>🧠 Preprocess</h3>
                    <p>Adaptive pipeline: imputation, scaling, encoding—auto-tuned</p>
                </div>
                <div class="step">
                    <div class="step-number">4</div>
                    <h3>🤖 Train</h3>
                    <p>7 algorithms trained with 5-fold CV—parallel execution</p>
                </div>
                <div class="step">
                    <div class="step-number">5</div>
                    <h3>🏆 Recommend</h3>
                    <p>Best algorithm ranked—visualizations + reasoning included</p>
                </div>
            </div>
        </div>

        <!-- Features -->
        <div class="features">
            <div class="feature-card">
                <h3>🔧 Robust Data Handling</h3>
                <ul>
                    <li>✅ Repairs corrupted files</li>
                    <li>✅ Auto-detects delimiters</li>
                    <li>✅ Handles 4+ encodings</li>
                    <li>✅ Cleans noisy data</li>
                </ul>
            </div>
            
            <div class="feature-card">
                <h3>🎯 Smart Preprocessing</h3>
                <ul>
                    <li>✅ Type-aware imputation</li>
                    <li>✅ Adaptive scaling selection</li>
                    <li>✅ Intelligent encoding</li>
                    <li>✅ Feature selection</li>
                </ul>
            </div>
            
            <div class="feature-card">
                <h3>📊 Rich Visualizations</h3>
                <ul>
                    <li>✅ Performance bar charts</li>
                    <li>✅ Confusion matrices</li>
                    <li>✅ ROC curves</li>
                    <li>✅ Error distribution plots</li>
                </ul>
            </div>
            
            <div class="feature-card">
                <h3>🚀 Zero Configuration</h3>
                <ul>
                    <li>✅ No manual tuning needed</li>
                    <li>✅ Auto problem detection</li>
                    <li>✅ One-click execution</li>
                    <li>✅ Downloadable results</li>
                </ul>
            </div>
        </div>

        <!-- Quick Start -->
        <div id="quick-start" class="code-block">
            <pre><span class="code-comment"># 🚀 Quick Start (3 Commands)</span>

<span class="code-command">git clone</span> https://github.com/sengobasar/Algorithm-name-recommender.git
<span class="code-command">cd</span> Algorithm-name-recommender

<span class="code-comment"># Create virtual environment</span>
<span class="code-command">python -m venv venv</span>
<span class="code-command">source venv/bin/activate</span>  <span class="code-comment"># Windows: venv\Scripts\activate</span>

<span class="code-comment"># Install & Run</span>
<span class="code-command">pip install -r requirements.txt</span>
<span class="code-command">streamlit run app.py</span>

<span class="code-comment"># 🎉 Open browser → Upload dataset → Get AI recommendations!</span></pre>
        </div>

        <!-- Algorithms -->
        <div class="process-flow">
            <h2>🤖 Supported Algorithms</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 30px;">
                <div>
                    <h3 style="color: #667eea; margin-bottom: 15px;">📊 Classification (7 Models)</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li>✅ Logistic Regression</li>
                        <li>✅ Random Forest</li>
                        <li>✅ Decision Tree</li>
                        <li>✅ Naive Bayes</li>
                        <li>✅ SVM</li>
                        <li>✅ KNN</li>
                        <li>✅ AdaBoost</li>
                    </ul>
                </div>
                <div>
                    <h3 style="color: #764ba2; margin-bottom: 15px;">📈 Regression (3+ Models)</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li>✅ Linear Regression</li>
                        <li>✅ Random Forest Regressor</li>
                        <li>✅ Decision Tree Regressor</li>
                        <li>✅ + More based on data</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Key Differentiators -->
        <div class="ai-section" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <h2>🌟 What Makes Us Different</h2>
            <div class="ai-features">
                <div class="ai-card">
                    <h3>🔓 Not a Black Box</h3>
                    <p>See reasoning for every decision—perfect for education and debugging</p>
                </div>
                <div class="ai-card">
                    <h3>🧹 Handles Messy Data</h3>
                    <p>Built for real-world datasets with noise, missing values, inconsistencies</p>
                </div>
                <div class="ai-card">
                    <h3>⚡ Fast & Practical</h3>
                    <p>Results in seconds—no cloud dependencies, runs locally</p>
                </div>
                <div class="ai-card">
                    <h3>📚 Educational</h3>
                    <p>Learn ML workflows—shows metrics, comparisons, and preprocessing steps</p>
                </div>
            </div>
        </div>

        <!-- Footer CTA -->
        <div class="hero" style="margin-top: 60px;">
            <h2 style="color: #667eea; margin-bottom: 20px;">Ready to Try?</h2>
            <p style="font-size: 1.2em; color: #666; margin-bottom: 30px;">
                Transform your messy datasets into ML insights in under 60 seconds
            </p>
            <a href="https://github.com/sengobasar/Algorithm-name-recommender" class="cta-button">⭐ Star on GitHub</a>
            <a href="#quick-start" class="cta-button">🚀 Get Started Now</a>
            
            <div style="margin-top: 40px; padding-top: 30px; border-top: 2px solid #eee;">
                <p style="color: #999;">Built with ❤️ using Python • Streamlit • Scikit-learn</p>
                <p style="color: #999; margin-top: 10px;">MIT License • Contributions Welcome</p>
            </div>
        </div>
    </div>
</body>
</html>

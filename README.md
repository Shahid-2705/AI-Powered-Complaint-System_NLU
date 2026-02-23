# Smart Incident / Complaint Understanding System

An AI-powered system designed to automatically analyze, classify, and route customer complaints. Built with Python, Flask, Streamlit, and Hugging Face Transformers.

## Features

1. **AI NLU Engine**:
   - **Intent Classification**: Uses zero-shot classification (`typeform/distilbert-base-uncased-mnli`) to categorize complaints (e.g., Delivery Delay, Payment Issue, Technical Problem).
   - **Sentiment Analysis**: Analyzes text sentiment (`cardiffnlp/twitter-roberta-base-sentiment`).
   - **Priority Prediction**: Automatically predicts if the issue is Low, Medium, or High priority.
   - **Auto-Reply Generation**: Generates a professional contextual reply to the customer using `google/flan-t5-small`.

2. **Smart Routing & Escalation**:
   - Routes tickets to specific departments (Logistics, Finance, IT Support, etc.) based on category.
   - Escalates tickets automatically if sentiment is Negative AND priority is High, or if specific keywords (legal, court, police, fraud) are detected.

3. **Web Application (Flask)**:
   - A modern user-friendly web interface for customers to submit their complaints.
   - Shows real-time analysis results and the auto-generated response.
   - Saves structured data into a local SQLite database.

4. **Analytics Dashboard (Streamlit)**:
   - A real-time data visualization dashboard pointing to the SQLite database.
   - Displays complaint category distributions (Bar Chart), priority distributions (Pie Chart), and daily trends (Line Chart).

## Project Structure

```text
smart_incident_system/
│
├── app.py                # Main Flask web application (User UI)
├── nlu_engine.py         # Hugging Face Transformers logic and AI Pipeline
├── db_config.py          # SQLite DB setup and query wrappers
├── dashboard.py          # Streamlit Analytics Dashboard
│
├── requirements.txt      # Project dependencies
├── README.md             # This file
│
├── templates/            # HTML templates for Flask
│   ├── index.html        # Complaint submission form
│   └── result.html       # Analysis and generated reply view
│
└── static/               # Static assets
    └── style.css         # CSS for the Flask web application
```

## Setup Instructions

1. **Install Prerequisites**:
   Ensure you have Python 3.8+ installed.

2. **Install Dependencies**:
   Navigate to the `smart_incident_system` directory in your terminal and run:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Downloading the Hugging Face transformer models for the first time will take some time depending on your internet connection.* 
   *Note: PyTorch will install the CPU version by default from PyPI if not configured otherwise. For GPU usage, ensure you have the correct CUDA PyTorch version installed from https://pytorch.org/.*

3. **Initialize Database and Start the Web App**:
   The web application allows users to submit complaints. Start it by running:
   ```bash
   python app.py
   ```
   The Flask application will start on `http://127.0.0.1:5000/` or `http://localhost:5000/`.

4. **Start the Analytics Dashboard**:
   The Streamlit dashboard allows administrators to visualize the aggregated complaints data. Open a new terminal instance, navigate to the `smart_incident_system` directory, and run:
   ```bash
   streamlit run dashboard.py
   ```
   The dashboard will open automatically in your browser at `http://localhost:8501/`.

## Usage
1. Go to the web app (`localhost:5000`) and submit a few dummy complaints.
   - *Example 1:* "I ordered a laptop a week ago and it's still not here. This is unacceptable, I am going to report this as fraud!"
   - *Example 2:* "I was double charged on my last invoice. Please fix this."
2. The AI will analyze the text, provide a response, and store the result.
3. Check the Streamlit dashboard (`localhost:8501`) to view the metrics populate in real-time.
"# AI-Powered-Complaint-System_NLU" 

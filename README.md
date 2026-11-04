# Netflix Customer Intelligence: Churn Prediction & AI Analytics Copilot

An end-to-end data analytics, machine learning, and interactive web application built to analyze Netflix customer behavior, predict churn risks, and provide automated business intelligence insights.

---

## 🚀 Project Overview & Development Journey
This project was engineered from scratch, taking raw data through a rigorous end-to-end data science and software deployment pipeline. Here are the core stages and milestones accomplished during its development:

1. **Data Collection & Aggregation:** Gathered and consolidated comprehensive customer usage metrics, subscription histories, watch patterns, and feedback logs.

2. **Data Cleaning & Preprocessing:** Handled missing values, treated outliers, standardized formats, and built robust automated cleaning scripts (`data_cleaning.py`, `handle_missing.py`).

3. **Exploratory Data Analysis (EDA):** Performed deep exploratory data analysis via Jupyter/Python notebooks (`netflix_eda_notebook.ipynb`, `eda_analysis.py`) to uncover key customer behavioral trends and churn drivers.

4. **Feature Engineering:** Extracted and engineered predictive features (`feature_engineering.py`) to enhance machine learning model performance.

5. **Database Population & Management:** Structured and loaded processed datasets into a high-performance relational database (`load_to_sql.py`, `netflix_customer_intelligence.db`).

6. **Machine Learning & Predictive Modeling:** Developed robust churn prediction algorithms and customer segmentation models to calculate risk scores and lifetime value (CLV).

7. **Interactive Streamlit Copilot App (`app.py`):** Built a feature-rich, interactive web application incorporating business intelligence queries, real-time analytics dashboards, automated recommendation engines, and dynamic user interfaces.

---

## 📁 Project Structure
- `app.py`: Main Streamlit application script powering the user interface and copilot features.
- `data_cleaning.py` & `handle_missing.py`: Automated scripts for data preprocessing and hygiene.
- `eda_analysis.py` & `feature_engineering.py`: Core logic for exploratory analysis and feature generation.
- `load_to_sql.py`: Database integration and loading utilities.
- `netflix_eda_notebook.ipynb`: Detailed Jupyter notebook containing visual exploratory analysis.
- `requirements.txt`: List of required Python libraries and dependencies.

---

## 📊 Dataset & Large Files Notice
Due to GitHub's file size restriction (100 MB limit), the large raw dataset files, processed features, and database backups are hosted externally. 

You can download the complete dataset and database files from the link below:
👉 **[Click here to download Netflix Dataset & Database files via Google Drive]
(https://drive.google.com/file/d/1oT7Tauf0gY1gNb3a3QbD35pSOeGJV_2q/view?usp=sharing)** 
(https://drive.google.com/file/d/1ARljMDmg6QssAk5TkEaLcj1okO-MVEMv/view?usp=sharing)
 (https://drive.google.com/file/d/1t0EobO28DrnH49jBRaihnXLGtTtxUfMT/view?usp=sharing)
  (https://drive.google.com/file/d/1NLpImMfLYoI0hmkptwm84uHW51Uorwiw/view?usp=sharing)
   (https://drive.google.com/file/d/1sQq8i6Zu1L5aGpr4bDHV_vW7VE3iESd6/view?usp=sharing)
    (https://drive.google.com/file/d/1jq9ZluCZDcex2XGsb8soG5YnQhn60beW/view?usp=sharing)
     (https://drive.google.com/file/d/1e4SfP_V941x9ubY4lOz8WfCAr1Zc459U/view?usp=sharing)
      (https://drive.google.com/file/d/1TUJaSMyqxnwwWaNa7SufSC5TGsVdx4lU/view?usp=sharing)

---

## 🛠️ How to Run Locally
1. Clone this repository:
   ```bash
   git clone [https://github.com/ayushkumar11092005/Netflix_customer_intelligence.git](https://github.com/ayushkumar11092005/Netflix_customer_intelligence.git)
    2:-  Navigate to the project directory:  cd Netflix_customer_intelligence
    3:-  Install the required dependencies:  pip install -r requirements.txt
    4:-  Run the Streamlit application:  streamlit run app.py
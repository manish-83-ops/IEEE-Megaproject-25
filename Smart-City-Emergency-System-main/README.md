# Smart-City-Emergency-System

Smart Emergency Resource Deployment System
Overview

Urban emergency response systems often rely on static rules or delayed human decisions, which can lead to inefficient allocation of ambulances, police units, and fire services.
This project presents a data-driven decision support system that predicts the expected number of emergency incidents in different city zones and recommends optimal deployment of emergency resources in advance.

The system is designed for smart cities, disaster preparedness, and municipal emergency planning, and was developed as part of the IEEE Mega Project Hackathon.

Problem Statement

Emergency incidents vary significantly by zone, time of day, and day of week

Manual planning leads to delayed or over/under-deployment of resources

Authorities lack predictive tools to proactively prepare for high-risk periods

Proposed Solution

We built a machine learning powered dashboard that:

Predicts incident load for a given zone and time

Converts predictions into actionable deployment plans

Helps authorities plan resources proactively instead of reactively

Provides a centralized interface for monitoring zone-wise risk

System Architecture

Data Layer

Historical emergency incident dataset

Zone, time, and calendar-based features

ML Model

Random Forest Regressor trained on historical patterns

Predicts expected incident count

Decision Engine

Maps predictions to deployment strategies

Determines priority level and required resources

Web Interface

Built using Streamlit

Interactive dashboard for planners and authorities

Features

Zone-wise incident prediction

Time-based risk analysis (hour, weekday/weekend)

Automatic priority classification (Low / Medium / High)

Resource recommendation (ambulance, police, fire)

Interactive dashboard with real-time inputs

Model transparency via feature importance

Scalable design suitable for smart city integration

Technology Stack

Python

Pandas, NumPy

Scikit-learn

Streamlit

Matplotlib

Joblib

Machine Learning Details

Model Used: Random Forest Regressor

Reason for Choice:

Handles non-linear relationships well

Robust to noise and outliers

Performs well on tabular data

Input Features:

zone_id

hour_of_day

day_of_week

is_weekend

Target Variable:

incident_count

Evaluation Metric:

Mean Absolute Error (MAE)

How It Works

User selects:

Zone

Day of week

Hour of day

Model predicts expected incident count

System assigns:

Priority level

Required emergency resources

Dashboard displays results clearly for decision-making

Project Structure
smart-city-emergency-system/
│
├── app.py                  # Streamlit dashboard
├── project.py              # Model training and saving
├── rf_model.pkl            # Trained ML model
├── feature_columns.pkl     # Feature order metadata
├── dataset.csv             # Training dataset
├── requirements.txt        # Dependencies
├── assets/                 # Images used in UI
└── README.md               # Project documentation

How to Run Locally

Clone the repository

git clone https://github.com/<your-username>/smart-city-emergency-system.git
cd smart-city-emergency-system


Install dependencies

pip install -r requirements.txt


Run the application

streamlit run app.py

Deployment

The application is deployed using Streamlit Cloud and can be accessed via the live demo link provided in the submission.

Use Cases

Municipal emergency planning

Smart city command centers

Disaster preparedness and response

Urban safety analytics

Academic and research demonstrations

Future Enhancements

Integration with real-time IoT and emergency call data

City map visualization with zone heatmaps

Automated alert triggers for authorities

Advanced forecasting models (XGBoost, LSTM)

Multi-city scalability

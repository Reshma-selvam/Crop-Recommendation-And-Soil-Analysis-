# Crop Recommendation and Soil Analysis using Deep Learning

## Project Overview
A web-based application that recommends suitable crops based on soil parameters using Deep Learning algorithms — **CNN (Convolutional Neural Network)** and **MLP (Multi-Layer Perceptron)**.

## Features
- User Registration & Login
- Admin Dashboard
- Soil parameter input (Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall)
- Crop Prediction using trained ML model
- Fertilizer Recommendation for each predicted crop
- Dataset upload and model training via web interface

## Tech Stack
- **Backend:** Python, Flask
- **Database:** MySQL (`1croprecomdb`)
- **ML/DL:** Scikit-learn (MLPClassifier), CNN, NumPy, Pandas
- **Visualization:** Matplotlib, Seaborn
- **Frontend:** HTML, CSS (Flask Templates)

## Crops Supported
Rice, Maize, Chickpea, Kidney Beans, Pigeon Peas, Moth Beans, Mung Bean, Black Gram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, Coffee

## Installation

### Requirements
```
pip install flask mysql-connector-python numpy pandas matplotlib seaborn scikit-learn openpyxl pickle5
```

### Database Setup
Create MySQL database named `1croprecomdb` with tables:
- `regtb` — User registration table
- `Querytb` — Query/prediction table

### Run the Application
```
python app.py
```
Open browser: `http://localhost:5000`

## Project Structure
```
crop_project/
├── app.py              # Main Flask application
├── README.md           # Project documentation
├── templates/          # HTML templates
│   ├── index.html
│   ├── AdminLogin.html
│   ├── UserLogin.html
│   ├── UserHome.html
│   ├── AdminHome.html
│   └── ...
└── static/
    └── images/         # Generated charts
```

## Academic Info
- **Degree:** M.Sc. Computer Science
- **College:** Arignar Anna Arts College, Villupuram
- **Year:** 2025–2026
- **Author:** S. Reshma

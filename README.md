# 🛡️ ScamShield AI

### AI-Powered Scam and Fraud Detection Platform

ScamShield AI is a web-based application that uses Machine Learning to analyze text messages and identify potential scam or genuine messages. It aims to improve digital awareness and help users stay alert against online fraud.

## 🚀 Key Features

- **AI-Based Detection:** Analyzes messages and predicts potential scams.
- **User Authentication:** Individual registration and login.
- **Personal Dashboard:** View personal scam detection statistics.
- **Detection History:** View and manage previous scan records.
- **Cybersecurity Guides:** Learn about phishing, fraud alerts, password safety, UPI safety and scam response.
- **Responsive Interface:** Simple and user-friendly design.

## 🛠️ Technologies Used

- Python
- Flask
- Machine Learning
- Scikit-learn
- MySQL
- HTML
- CSS
- JavaScript

## ⚙️ Installation & Setup

1. Clone the repository:

   `git clone https://github.com/ishagadhave128/ScamShield-AI.git`

2. Open the project folder:

   `cd ScamShield-AI`

3. Create and activate a virtual environment:

   `python -m venv venv`

   `venv\Scripts\activate`

4. Install dependencies:

   `pip install -r requirements.txt`

5. Create a `.env` file in the project root and configure:

   - DB_HOST
   - DB_USER
   - DB_PASSWORD
   - DB_NAME
   - SECRET_KEY

6. Create the MySQL database and required tables (`users` and `detection_history`) using the schema expected by the application.

7. Start the application:

   `python app.py`

8. Open `http://127.0.0.1:5000` in your browser.

## 📌 Project Purpose

The goal of ScamShield AI is to promote digital safety by making people more aware of suspicious messages and possible online scams.

## ⚠️ Disclaimer

The detection result is a machine-learning prediction and should not be treated as a guaranteed verification. Always verify suspicious messages through official sources.

## 👩‍💻 Developed By

**Isha Gadhave**

GitHub: https://github.com/ishagadhave128

## 📸 Project Screenshots

### 1. Home Page
![Home Page](Screenshot%202026-11-22%20145758.png)

### 2. Message Detection
![Message Detection](Screenshot%202026-11-22%20145816.png)

### 3. Detection Result
![Detection Result](Screenshot%202026-11-22%20150108.png)

### 4. Login Page
![Login Page](Screenshot%202026-11-22%20180931.png)

### 5. Register Page
![Register Page](Screenshot%202026-11-22%20181113.png)

### 6. Dashboard
![Dashboard](Screenshot%202026-11-22%20181241.png)

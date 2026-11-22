
import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

data = {
    "message": [
        "Your bank account is blocked verify now",
        "Congratulations you won a lottery claim prize",
        "Click this link to get free money",
        "Urgent update your KYC immediately",
        "Send your OTP to receive reward",
        "You won a free iPhone click here",
        "Your account will be suspended call this number",
        "Claim your cash prize now",
        "Pay processing fee to receive your reward",
        "Verify your password using this link",
        "You have won 50000 rupees",
        "Limited offer send bank details now",
        "Your parcel is held pay delivery fee",
        "Download this app to get instant loan",
        "Share OTP to confirm your identity",
        "Your electricity connection will be disconnected pay now",
        "We detected suspicious activity login here",
        "Get guaranteed returns invest today",
        "Your credit card is blocked update details",
        "Click now to claim your gift voucher",

        "Your meeting is scheduled for tomorrow",
        "Please send me the project report",
        "Your order has been delivered",
        "Happy birthday have a wonderful day",
        "The class will start at ten am",
        "Please call me when you are free",
        "Your appointment is confirmed",
        "Thank you for your application",
        "The office will remain closed tomorrow",
        "I have shared the assignment with you",
        "Your payment was successful",
        "Please check your email for the document",
        "We will meet at the college tomorrow",
        "Your interview is scheduled for Monday",
        "The train will arrive at six pm",
        "Please complete the homework today",
        "Your registration is successful",
        "The report is ready for review",
        "See you at the office tomorrow",
        "Thank you for your feedback"
    ],
    "label": [
        "scam", "scam", "scam", "scam", "scam",
        "scam", "scam", "scam", "scam", "scam",
        "scam", "scam", "scam", "scam", "scam",
        "scam", "scam", "scam", "scam", "scam",
        "genuine", "genuine", "genuine", "genuine",
        "genuine", "genuine", "genuine", "genuine",
        "genuine", "genuine", "genuine", "genuine",
        "genuine", "genuine", "genuine", "genuine",
        "genuine", "genuine", "genuine", "genuine"
    ]
}

df = pd.DataFrame(data)

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000))
])

model.fit(df["message"], df["label"])

joblib.dump(model, "scam_model.pkl")

print("ScamShield AI Model trained successfully!")

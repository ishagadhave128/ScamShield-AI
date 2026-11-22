
from flask import Flask, render_template, request, redirect, url_for, session, flash
import csv
from io import StringIO
from flask import make_response
import os
import joblib
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_connection

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

model = joblib.load("scam_model.pkl")


# HOME PAGE - SCAM DETECTION
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    confidence = None
    message = ""

    if request.method == "POST":
        message = request.form.get("message", "").strip()

        if message:
            prediction = model.predict([message])[0]
            probabilities = model.predict_proba([message])[0]
            confidence = round(max(probabilities) * 100, 2)

            result = (
                "SCAM DETECTED"
                if prediction == "scam"
                else "GENUINE MESSAGE"
            )

            # SAVE DETECTION IN DATABASE
            if session.get("user_id"):
                db = get_connection()

                if db:
                    cursor = db.cursor()
                    try:
                        cursor.execute(
                            """
                            INSERT INTO detection_history
                            (user_id, message, prediction, confidence)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (
                                session["user_id"],
                                message,
                                prediction,
                                confidence
                            )
                        )
                        db.commit()

                    except Exception as error:
                        db.rollback()
                        print("Detection Save Error:", error)

                    finally:
                        cursor.close()
                        db.close()

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        message=message
    )


# REGISTER PAGE
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill all fields.")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.")
            return redirect(url_for("register"))

        db = get_connection()

        if not db:
            flash("Database connection failed.")
            return redirect(url_for("register"))

        cursor = db.cursor()

        try:
            hashed_password = generate_password_hash(password)

            cursor.execute(
                """
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
                """,
                (name, email, hashed_password)
            )

            db.commit()
            flash("Registration successful! Please login.")
            return redirect(url_for("login"))

        except Exception as error:
            db.rollback()
            print("Registration Error:", error)
            flash("This email may already be registered.")

        finally:
            cursor.close()
            db.close()

    return render_template("register.html")


# LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        db = get_connection()

        if not db:
            flash("Database connection failed.")
            return redirect(url_for("login"))

        cursor = db.cursor()

        try:
            cursor.execute(
                "SELECT id, name, password FROM users WHERE email = %s",
                (email,)
            )

            user = cursor.fetchone()

        finally:
            cursor.close()
            db.close()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            return redirect(url_for("home"))

        flash("Invalid email or password.")

    return render_template("login.html")


# FEATURES PAGE
@app.route("/features")
def features():
    return render_template("features.html")


# ABOUT PAGE
@app.route("/about")
def about():
    return render_template("about.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# USER DASHBOARD
@app.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    db = get_connection()

    if not db:
        flash("Database connection failed.")
        return redirect(url_for("home"))

    cursor = db.cursor()

    try:
        # TOTAL SCANS
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM detection_history
            WHERE user_id = %s
            """,
            (session["user_id"],)
        )
        total_scans = cursor.fetchone()[0]

        # TOTAL SCAMS
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM detection_history
            WHERE user_id = %s AND prediction = 'scam'
            """,
            (session["user_id"],)
        )
        scams = cursor.fetchone()[0]

        # TOTAL GENUINE MESSAGES
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM detection_history
            WHERE user_id = %s AND prediction = 'genuine'
            """,
            (session["user_id"],)
        )
        genuine = cursor.fetchone()[0]

        # RECENT DETECTION HISTORY
        cursor.execute(
            """
            SELECT id, message, prediction, confidence, created_at
            FROM detection_history
            WHERE user_id = %s
            ORDER BY id DESC
            LIMIT 10
            """,
            (session["user_id"],)
        )

        history = cursor.fetchall()

    finally:
        cursor.close()
        db.close()

    return render_template(
        "dashboard.html",
        total_scans=total_scans,
        scams=scams,
        genuine=genuine,
        history=history
    )


# DELETE SINGLE DETECTION
@app.route("/delete-history/<int:history_id>", methods=["POST"])
def delete_history(history_id):
    if not session.get("user_id"):
        return redirect(url_for("login"))

    db = get_connection()

    if not db:
        flash("Database connection failed.")
        return redirect(url_for("dashboard"))

    cursor = db.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM detection_history
            WHERE id = %s AND user_id = %s
            """,
            (history_id, session["user_id"])
        )

        db.commit()
        flash("Detection record deleted successfully!")

    except Exception as error:
        db.rollback()
        print("Delete Error:", error)
        flash("Unable to delete detection record.")

    finally:
        cursor.close()
        db.close()

    return redirect(url_for("dashboard"))


# DELETE ALL DETECTION HISTORY
@app.route("/delete-all-history", methods=["POST"])
def delete_all_history():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    db = get_connection()

    if not db:
        flash("Database connection failed.")
        return redirect(url_for("dashboard"))

    cursor = db.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM detection_history
            WHERE user_id = %s
            """,
            (session["user_id"],)
        )

        db.commit()
        flash("All detection history deleted successfully!")

    except Exception as error:
        db.rollback()
        print("Delete All Error:", error)
        flash("Unable to delete detection history.")

    finally:
        cursor.close()
        db.close()

    return redirect(url_for("dashboard"))

# EXPORT DETECTION HISTORY AS CSV
@app.route("/export-history")
def export_history():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    db = get_connection()

    if not db:
        flash("Database connection failed.")
        return redirect(url_for("dashboard"))

    cursor = db.cursor()

    try:
        cursor.execute(
            """
            SELECT message, prediction, confidence, created_at
            FROM detection_history
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (session["user_id"],)
        )

        history = cursor.fetchall()

    except Exception as error:
        print("Export Error:", error)
        flash("Unable to export detection history.")
        return redirect(url_for("dashboard"))

    finally:
        cursor.close()
        db.close()

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Message",
        "Prediction",
        "Confidence (%)",
        "Date & Time"
    ])

    for item in history:
        writer.writerow([
            item[0],
            item[1],
            item[2],
            item[3]
        ])

    response = make_response("\ufeff" + output.getvalue())
    response.headers["Content-Disposition"] = (
        "attachment; filename=scamshield_detection_history.csv"
    )
    response.headers["Content-Type"] = "text/csv; charset=utf-8"

    return response



if __name__ == "__main__":
    app.run(debug=True)

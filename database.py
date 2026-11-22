import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME")
        }

        if config["host"] not in ("localhost", "127.0.0.1"):
            config["ssl_verify_cert"] = True
            config["ssl_verify_identity"] = True
            ca_path = os.getenv("DB_SSL_CA")
            if ca_path:
                config["ssl_ca"] = ca_path

        return mysql.connector.connect(**config)

    except mysql.connector.Error as error:
        print("Database Connection Error:", error)
        return None


if __name__ == "__main__":
    db = get_connection()

    if db:
        print("ScamShield AI Database Connected Successfully!")
        db.close()
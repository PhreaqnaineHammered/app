from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def check_license(user_id):
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT expiration FROM orders WHERE user_id = ? AND status = 'completed'", (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        expiration_date = datetime.strptime(result[0], "%Y-%m-%d").date()
        if datetime.now().date() <= expiration_date:
            return {"status": "valid"}
    return {"status": "expired"}

@app.route('/check_license', methods=['POST'])
def check_license_endpoint():
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID required"}), 400

    return jsonify(check_license(user_id))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

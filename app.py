from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace this with your NowPayments API Key
API_KEY = "your_nowpayments_api_key"

@app.route('/callback', methods=['POST'])
def nowpayments_callback():
    data = request.json  # Get the JSON data sent by NowPayments

    # Verify if the request contains required fields
    if "payment_status" in data and "payment_id" in data:
        payment_status = data["payment_status"]
        payment_id = data["payment_id"]
        amount_received = data.get("pay_amount", 0)
        currency = data.get("pay_currency", "Unknown")

        # Log the received data
        print(f"Received payment update: ID {payment_id}, Status {payment_status}, Amount {amount_received} {currency}")

        # Check if payment is confirmed
        if payment_status == "finished":
            # Process successful payment (e.g., mark order as paid)
            print("Payment confirmed!")

        return jsonify({"status": "success"}), 200

    return jsonify({"error": "Invalid request"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

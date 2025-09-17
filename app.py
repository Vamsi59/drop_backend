from flask import Flask, request, jsonify
from flask_cors import CORS
import os  # for Railway PORT

app = Flask(__name__)
CORS(app)  # allow frontend to access API

def predict_dropout(attendance, grades, participation, financial_issue, family_support, health_issue):
    score = 0
    if attendance < 75:
        score += 1
    if grades < 50:
        score += 1
    if participation < 5:
        score += 1
    if financial_issue == "Yes":
        score += 1
    if family_support == "Poor":
        score += 1
    if health_issue == "Yes":
        score += 1

    if score >= 4:
        return "High Risk", ["Immediate counseling required", "Check financial aid", "Provide health support"]
    elif score >= 2:
        return "Moderate Risk", ["Monitor closely", "Offer academic help"]
    else:
        return "Low Risk", ["Encourage continued performance"]

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        attendance = float(data["attendance"])
        grades = float(data["grades"])
        participation = int(data["participation"])
        financial_issue = data["financial_issue"]
        family_support = data["family_support"]
        health_issue = data["health_issue"]

        risk, suggestions = predict_dropout(attendance, grades, participation, financial_issue, family_support, health_issue)

        return jsonify({"risk": risk, "suggestions": suggestions})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Dropout Prediction API is running!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway sets the port
    app.run(host="0.0.0.0", port=port)

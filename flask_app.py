from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "fintech.joblib")
model = joblib.load(MODEL_PATH)


def make_prediction(link_risk_score, sender_trust_score, requests_sensitive_info):
    values = np.array([[link_risk_score, sender_trust_score, requests_sensitive_info]])
    prediction = int(model.predict(values)[0])
    probability = float(model.predict_proba(values)[0][1])
    return prediction, probability


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict_form():
    try:
        link_risk_score = float(request.form["link_risk_score"])
        sender_trust_score = float(request.form["sender_trust_score"])
        requests_sensitive_info = int(request.form["requests_sensitive_info"])

        if not 0 <= link_risk_score <= 100:
            raise ValueError("Link risk score must be between 0 and 100.")
        if not 0 <= sender_trust_score <= 100:
            raise ValueError("Sender trust score must be between 0 and 100.")
        if requests_sensitive_info not in (0, 1):
            raise ValueError("Sensitive information field must be 0 or 1.")

        prediction, probability = make_prediction(
            link_risk_score,
            sender_trust_score,
            requests_sensitive_info,
        )

        label = "Likely scam" if prediction == 1 else "Likely legitimate"
        return render_template(
            "index.html",
            prediction=label,
            probability=round(probability * 100, 1),
            link_risk_score=link_risk_score,
            sender_trust_score=sender_trust_score,
            requests_sensitive_info=requests_sensitive_info,
        )
    except (ValueError, KeyError) as exc:
        return render_template("index.html", error=str(exc)), 400


@app.route("/api/predict", methods=["GET", "POST"])
def predict_api():
    try:
        if request.method == "POST":
            data = request.get_json(silent=True) or {}
        else:
            data = request.args

        link_risk_score = float(data["link_risk_score"])
        sender_trust_score = float(data["sender_trust_score"])
        requests_sensitive_info = int(data["requests_sensitive_info"])

        if not 0 <= link_risk_score <= 100:
            raise ValueError("link_risk_score must be between 0 and 100")
        if not 0 <= sender_trust_score <= 100:
            raise ValueError("sender_trust_score must be between 0 and 100")
        if requests_sensitive_info not in (0, 1):
            raise ValueError("requests_sensitive_info must be 0 or 1")

        prediction, probability = make_prediction(
            link_risk_score,
            sender_trust_score,
            requests_sensitive_info,
        )

        return jsonify({
            "prediction": prediction,
            "label": "likely_scam" if prediction == 1 else "likely_legitimate",
            "scam_probability": round(probability, 4),
            "inputs": {
                "link_risk_score": link_risk_score,
                "sender_trust_score": sender_trust_score,
                "requests_sensitive_info": requests_sensitive_info,
            },
        })
    except (ValueError, KeyError, TypeError) as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    app.run(debug=True)

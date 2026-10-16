# MoneyShield AI Scam Detector

MoneyShield is a Fintech concept designed to help young users identify suspicious financial messages and links before they interact with them. This project uses a logistic-regression machine-learning model to classify a message or link as **likely legitimate (0)** or **likely scam (1)**.

## Live application

https://lillypasternack.pythonanywhere.com

## Machine-learning problem

- **Population:** Young digital-banking and online-payment users who receive financial messages, links, emails or texts.
- **Task:** Binary classification.
- **Model:** Logistic Regression.
- **Target:** `is_scam`
  - `0` = likely legitimate
  - `1` = likely scam

### Input variables

1. `link_risk_score` – 0 to 100. Higher values represent more suspicious URL or message indicators.
2. `sender_trust_score` – 0 to 100. Higher values represent a more trustworthy sender.
3. `requests_sensitive_info` – 0 or 1. Whether the message asks for passwords, banking details, card data or verification codes.

The synthetic dataset is generated with a fixed NumPy seed so the results are reproducible.

## Files

- `fintech.py` – generates synthetic data, trains and validates the model, and saves the dataset and model.
- `fintech.joblib` – trained logistic-regression model.
- `flask_app.py` – Flask web application and API.
- `templates/index.html` – HTML user interface.
- `requirements.txt` – Python dependencies.
- `ADAPTED_PROMPT.txt` – adapted LLM prompt used for the assignment.

Running `fintech.py` also generates `fintech.xlsx`.

## Run the training code

```bash
python3 fintech.py
```

This creates `fintech.xlsx` and `fintech.joblib`.

## Run locally

```bash
pip install -r requirements.txt
python3 flask_app.py
```

Then open `http://127.0.0.1:5000/`.

## API endpoint

### POST `/api/predict`

Example request:

```bash
curl -X POST https://lillypasternack.pythonanywhere.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{"link_risk_score":90,"sender_trust_score":10,"requests_sensitive_info":1}'
```

Example JSON response from the deployed model:

```json
{
  "prediction": 1,
  "label": "likely_scam",
  "scam_probability": 0.9481,
  "inputs": {
    "link_risk_score": 90.0,
    "sender_trust_score": 10.0,
    "requests_sensitive_info": 1
  }
}
```

The endpoint also accepts GET parameters, for example:

```text
https://lillypasternack.pythonanywhere.com/api/predict?link_risk_score=90&sender_trust_score=10&requests_sensitive_info=1
```

## PythonAnywhere deployment

The application is deployed at:

https://lillypasternack.pythonanywhere.com

The WSGI configuration imports the Flask app from `flask_app.py`.

## Course submission

- PythonAnywhere teacher username: `mfalonso`
- Submit this GitHub repository link.
- Submit the public PythonAnywhere URL.
- No passwords, API tokens or credentials are included in this repository.

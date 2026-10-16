# MoneyShield – Scam Risk Classification

MoneyShield is a Fintech concept designed to help young users identify suspicious financial messages and links before they interact with them. This project uses a logistic-regression model to classify a message/link as **likely legitimate (0)** or **likely scam (1)**.

## Machine-learning problem

- **Population:** Young digital-banking and online-payment users who receive financial messages, links, emails or texts.
- **Task:** Binary classification.
- **Target:** `is_scam`
  - `0` = likely legitimate
  - `1` = likely scam

### Input variables

1. `link_risk_score` – 0 to 100. Higher values represent more suspicious URL/message indicators.
2. `sender_trust_score` – 0 to 100. Higher values represent a more trustworthy sender.
3. `requests_sensitive_info` – 0 or 1. Whether the message asks for passwords, banking details, card data or verification codes.

The dataset is synthetic and generated with a fixed NumPy seed so the results are reproducible.

## Files

- `fintech.py` – generates synthetic data, trains and validates the model, saves the dataset and model.
- `fintech.xlsx` – synthetic dataset.
- `fintech.joblib` – trained logistic-regression model.
- `flask_app.py` – Flask web application and API.
- `templates/index.html` – HTML user interface.
- `requirements.txt` – Python dependencies.

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

Open `http://127.0.0.1:5000/`.

## API endpoint

### POST `/api/predict`

Example request:

```bash
curl -X POST https://lillypasternack.pythonanywhere.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "link_risk_score": 85,
    "sender_trust_score": 20,
    "requests_sensitive_info": 1
  }'
```

Example JSON response:

```json
{
  "prediction": 1,
  "label": "likely_scam",
  "scam_probability": 0.97,
  "inputs": {
    "link_risk_score": 85,
    "sender_trust_score": 20,
    "requests_sensitive_info": 1
  }
}
```

The endpoint also accepts GET parameters, for example:

```text
https://lillypasternack.pythonanywhere.com/api/predict?link_risk_score=85&sender_trust_score=20&requests_sensitive_info=1
```

## PythonAnywhere deployment

1. Upload this project to PythonAnywhere.
2. Open a Bash console and install requirements if needed.
3. Run `python3 fintech.py` if you want to regenerate the model on PythonAnywhere.
4. Go to **Web → Add a new web app → Manual configuration → Python 3.x**.
5. Edit the WSGI file so it imports the Flask app from `flask_app.py`.
6. Reload the web app.
7. Test the public root URL and `/api/predict` endpoint.

A typical WSGI import is:

```python
import sys
path = '/home/lillypasternack/mysite'
if path not in sys.path:
    sys.path.append(path)

from flask_app import app as application
```

## Course submission reminder

- Invite Professor Manoel Gadi as teacher on PythonAnywhere using username `mfalonso`.
- Submit the GitHub repository link.
- Submit the public PythonAnywhere URL.
- Do not upload passwords, tokens or credentials.

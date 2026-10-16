import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Reproducible synthetic data
np.random.seed(42)
n = 1000

# MoneyShield input variables
link_risk_score = np.random.randint(0, 101, n)
sender_trust_score = np.random.randint(0, 101, n)
requests_sensitive_info = np.random.binomial(1, 0.35, n)

# Create a realistic scam probability.
# Higher link risk and requests for sensitive info increase scam risk.
# Higher sender trust decreases scam risk.
logit = (
    -2.8
    + 0.055 * link_risk_score
    - 0.045 * sender_trust_score
    + 2.0 * requests_sensitive_info
)
scam_probability = 1 / (1 + np.exp(-logit))
is_scam = np.random.binomial(1, scam_probability)

# Build and save dataset
df = pd.DataFrame({
    "link_risk_score": link_risk_score,
    "sender_trust_score": sender_trust_score,
    "requests_sensitive_info": requests_sensitive_info,
    "is_scam": is_scam,
})
df.to_excel("fintech.xlsx", index=False)

# Train/test split
X = df[["link_risk_score", "sender_trust_score", "requests_sensitive_info"]]
y = df["is_scam"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y,
)

# Logistic regression classification model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Validation reports
print("TRAIN CLASSIFICATION REPORT")
print(classification_report(y_train, model.predict(X_train)))
print("TEST CLASSIFICATION REPORT")
print(classification_report(y_test, model.predict(X_test)))

# Save trained model
joblib.dump(model, "fintech.joblib")
print("Created fintech.xlsx and fintech.joblib")

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load Blue Jays data
df1 = pd.read_csv('blue_jays_games_data.csv')
df1 = df1.dropna(subset=["OPS", "WHIP", "Result"])

# Encode result to numeric
df1['Result'] = df1['Result'].map({'W': 1, 'L': 0})

# Define features and target
X = df1[["OPS", "WHIP"]]
y = df1["Result"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


lrm = LogisticRegression()

# Fit the model using Grid Search
lrm.fit(X_train, y_train)

# Predict on test set
y_pred = lrm.predict(X_test)

# Output results
print("✅ Accuracy on Test Set:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred))

# Load Phillies data
# phillies_data = pd.read_csv('phi_games_data.csv')
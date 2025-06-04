import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# Load Blue Jays data
df1 = pd.read_csv('blue_jays_games_data.csv')
df1 = df1.dropna(subset=["OPS", "WHIP","opp_OPS", "opp_WHIP", "Result"])

# Encode result to numeric
df1['Result'] = df1['Result'].map({'W': 1, 'L': 0})

# Define features and target
X = df1[["OPS", "WHIP", "opp_OPS", "opp_WHIP"]]
y = df1["Result"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled  = scaler.transform(X_test)  # Use same scaler!

lrm = LogisticRegression(class_weight='balanced', C=10)

# Fit the model 
lrm.fit(X_train, y_train)

# Predict on test set
y_pred = lrm.predict(X_test)
y_pred_reset = pd.Series(y_pred, name="Predicted_Result").reset_index(drop=True)


# Predict win probabilities
y_proba = lrm.predict_proba(X_test)[:, 1]

# Reset indices to align properly
X_test_reset = X_test.reset_index(drop=True)
y_test_reset = y_test.reset_index(drop=True)
y_proba_series = pd.Series(y_proba * 100, name="Win_Probability")

# Combine all into one DataFrame
results_df = pd.concat([X_test_reset, y_test_reset, y_pred_reset, y_proba_series], axis=1)
results_df.columns = list(X_test.columns) + ["Actual_Result", "Predicted_Result", "Win_Probability"]
results_df = results_df.round(3)

# Print the table
print(results_df)

# Output results
print("✅ Accuracy on Test Set:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred))


# Load Phillies data
# phillies_data = pd.read_csv('phi_games_data.csv')
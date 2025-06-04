import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load Blue Jays data
df1 = pd.read_csv('blue_jays_games_data.csv')

# Encode result to numeric
df1['Result'] = df1['Result'].map({'W': 1, 'L': 0})

# Define features and target
X = df1[["OPS", "WHIP"]]
y = df1["Result"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define hyperparameter grid
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [3, 5, 7],
    'min_samples_split': [2, 4],
    'min_samples_leaf': [1, 2],
    'max_features': ['sqrt', 'log2'],
    'class_weight': [None, 'balanced']
}

# Initialize Grid Search
grid_search = GridSearchCV(
    estimator=RandomForestClassifier(random_state=42),
    param_grid=param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)

# Fit the model using Grid Search
grid_search.fit(X_train, y_train)

# Best model from Grid Search
best_model = grid_search.best_estimator_

# Predict on test set
y_pred = best_model.predict(X_test)

# Output results
print("✅ Best Parameters:", grid_search.best_params_)
print("✅ Accuracy on Test Set:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred))

# Load Phillies data
# phillies_data = pd.read_csv('phi_games_data.csv')
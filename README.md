# Baseball Game Predictor

This project uses machine learning to predict MLB game outcomes based on team performance metrics. It is an early-stage implementation using logistic regression, feature scaling, and regularization, with plans to evolve into a more complex ensemble-based model as the dataset grows.

## Prediction Strategy

- **Team-Specific Models**: A separate logistic regression model is trained for each team using only that team’s historical games.
- **Opponent-Agnostic**: Each model is independent of the specific opponent; it focuses solely on how a team historically performs based on its own stats.
- **Rolling Average Input**: For game-day predictions, a rolling average of the past two weeks of team stats is used to represent expected performance.
- **Outcome Estimation**: Each model outputs a win probability based on the rolling stats.
- **Final Prediction**: The predicted winner is the team with the higher win probability in that matchup.

## Technical Overview

- **Model**: Logistic Regression
- **Scaling Features**: Features are scaled to manage different stat magnitudes and outliers.
- **Regularization (L2)**: Prevents data overfitting 
- **Dataset**:
  - ~60 data points per team (currently limited to a few teams).
  - 4 features total:
    - `OPS` and `WHIP` for both teams in a game.

## Roadmap

As more teams and features are added, the model will transition to a **Random Forest Classifier** to handle feature interactions and non-linearity more effectively.

## Tech Stack

- Python
- Scikit-learn
- Pandas
- Selenium (for data scraping and schedule updates)

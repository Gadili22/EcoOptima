import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, KFold
from sklearn.ensemble import RandomForestClassifier

class CostPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def generate_dummy_data(self):
        # Simuliamo un dataset per rispettare le linee guida
        np.random.seed(42)
        data = {
            'temperature': np.random.uniform(0, 35, 1000),
            'hour': np.random.randint(0, 24, 1000),
            'day_of_week': np.random.randint(0, 7, 1000),
            'solar_production': np.random.uniform(0, 5, 1000)
        }
        df = pd.DataFrame(data)
        # Target: 1 se costo alto, 0 se basso
        df['high_cost'] = np.where((df['hour'] > 17) & (df['hour'] < 22), 1, 0)
        return df

    def train_and_evaluate(self):
        df = self.generate_dummy_data()
        X = df[['temperature', 'hour', 'day_of_week', 'solar_production']]
        y = df['high_cost']

        # 10-Fold Cross Validation (NO single run)
        kf = KFold(n_splits=10, shuffle=True, random_state=42)
        scores = cross_val_score(self.model, X, y, cv=kf, scoring='accuracy')

        print(f"=== ML Validation Results ===")
        print(f"Mean Accuracy: {scores.mean():.4f}")
        print(f"Std Deviation: {scores.std():.4f}")
        
        # Addestramento finale
        self.model.fit(X, y)
        return scores.mean()

    def predict_tomorrow(self, features):
        return self.model.predict([features])[0]
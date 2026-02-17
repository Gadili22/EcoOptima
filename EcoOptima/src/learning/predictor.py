import pandas as pd
import numpy as np
import os
from sklearn.model_selection import cross_val_score, KFold
from sklearn.ensemble import RandomForestClassifier

class CostPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # Calcola il percorso esatto verso la cartella dataset
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.dataset_path = os.path.join(base_path, "..", "..", "dataset", "energy_data.csv")
    
    def load_or_create_dataset(self):
        """Legge il dataset da CSV. Se non esiste, lo genera e lo salva."""
        
        # 1. TENTATIVO DI LETTURA DAL DISCO (Ora legge con il punto e virgola)
        if os.path.exists(self.dataset_path):
            print("[ML] Lettura dati storici dal file CSV locale...")
            return pd.read_csv(self.dataset_path, sep=';')
        
        # 2. SE IL FILE NON ESISTE, LO GENERA E LO SALVA
        print("[ML] File CSV non trovato. Generazione dataset storico in corso...")
        np.random.seed(42)
        data = {
            'temperature': np.random.uniform(0, 35, 1000),
            'hour': np.random.randint(0, 24, 1000),
            'day_of_week': np.random.randint(0, 7, 1000),
            'solar_production': np.random.uniform(0, 5, 1000)
        }
        df = pd.DataFrame(data)
        
        # Arrotondiamo a 2 cifre decimali per renderlo leggibile
        df['temperature'] = df['temperature'].round(2)
        df['solar_production'] = df['solar_production'].round(2)
        
        # Regola base: Costo alto tra le 17 e le 22
        df['high_cost'] = np.where((df['hour'] > 17) & (df['hour'] < 22), 1, 0)
        
        # Aggiungiamo del "rumore" (5%) per renderlo un dataset realistico
        mask = np.random.rand(len(df)) < 0.05 
        df.loc[mask, 'high_cost'] = 1 - df.loc[mask, 'high_cost']
        
        # Salva il dataframe fisicamente usando il PUNTO E VIRGOLA (sep=';') per Excel Italiano!
        df.to_csv(self.dataset_path, index=False, sep=';')
        print(f"[ML] Dataset salvato con successo in: {self.dataset_path}")
        
        return df

    def train_and_evaluate(self):
        # Chiama la nuova funzione che gestisce il file CSV
        df = self.load_or_create_dataset()
        
        X = df[['temperature', 'hour', 'day_of_week', 'solar_production']]
        y = df['high_cost']

        # 10-Fold Cross Validation
        kf = KFold(n_splits=10, shuffle=True, random_state=42)
        scores = cross_val_score(self.model, X, y, cv=kf, scoring='accuracy')

        print(f"=== ML Validation Results ===")
        print(f"Righe dataset analizzate: {len(df)}")
        print(f"Mean Accuracy: {scores.mean():.4f}")
        print(f"Std Deviation: {scores.std():.4f}")
        
        # Addestramento finale
        self.model.fit(X, y)
        return scores.mean()

    def predict_tomorrow(self, features):
        return self.model.predict([features])[0]
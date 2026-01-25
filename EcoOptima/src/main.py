import os
import sys

# Aggiunge la cartella corrente al path per permettere gli import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic.constraint_scheduler import EnergyScheduler
from learning.predictor import CostPredictor
from uncertainty.risk_model import RiskAnalyzer

def main():
    print("=== EcoOptima: Intelligent HEMS ===")
    
    # 1. Machine Learning: Previsione Costi
    print("\n[ML] Addestramento Modello Previsione Costi...")
    predictor = CostPredictor()
    acc = predictor.train_and_evaluate()
    print(f"Modello pronto con accuratezza media: {acc*100:.2f}%")

    # 2. Risk Analysis (Bayes)
    print("\n[Bayes] Calcolo Rischio Blackout odierno...")
    risk_engine = RiskAnalyzer()
    # Simuliamo uno scenario: Nuvoloso (1) e Alto Carico Utente (1)
    prob_blackout = risk_engine.get_blackout_probability(meteo_val=1, carico_val=1) 
    print(f"Probabilità di Blackout calcolata: {prob_blackout:.2f}")

    if prob_blackout > 0.5:
        print(">>> ATTENZIONE: Rischio elevato rilevato. Attivazione Scheduler Ottimizzato.")
        
        # 3. Scheduling (CSP + Prolog)
        print("\n[CSP] Avvio pianificazione dispositivi con Knowledge Base...")
        
        # Costruisce il percorso assoluto per il file Prolog
        base_path = os.path.dirname(os.path.abspath(__file__))
        kb_path = os.path.join(base_path, "..", "dataset", "devices_rules.pl")
        
        try:
            scheduler = EnergyScheduler(kb_path)
            
            to_schedule = ["lavatrice", "forno", "auto_elettrica"]
            print(f"Dispositivi richiesti: {to_schedule}")
            
            solutions = scheduler.schedule_devices(to_schedule)
            
            if solutions:
                print(f"Trovate {len(solutions)} pianificazioni valide. Ecco la migliore:")
                best_sol = solutions[0] # Semplificazione: prendiamo la prima
                
                # Ordina per orario
                sorted_sol = sorted(best_sol.items(), key=lambda item: item[1])
                
                for dev, time in sorted_sol:
                    print(f" - {dev.ljust(15)}: Accendere alle ore {time}:00")
            else:
                print("Nessuna soluzione trovata! Riduci i carichi o cambia orari.")
                
        except Exception as e:
            print(f"Errore nel caricamento della KB Prolog: {e}")
            print("Assicurati che SWI-Prolog sia installato e nel PATH.")
    else:
        print("Rischio basso. Puoi usare i dispositivi liberamente.")

if __name__ == "__main__":
    main()
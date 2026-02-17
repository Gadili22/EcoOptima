import os
import sys
import matplotlib.pyplot as plt

# Aggiunge la cartella corrente al path per permettere gli import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic.constraint_scheduler import EnergyScheduler
from learning.predictor import CostPredictor
from uncertainty.risk_model import RiskAnalyzer

def main():
    print("=== EcoOptima: Intelligent HEMS (Simulatore di Scenari) ===")
    
    # ---------------------------------------------------------
    # 1. MACHINE LEARNING (Viene addestrato una sola volta)
    # ---------------------------------------------------------
    print("\n[ML] Addestramento Modello Previsione Costi (K-Fold CV)...")
    predictor = CostPredictor()
    acc = predictor.train_and_evaluate()
    print(f"Modello pronto con accuratezza media: {acc*100:.2f}%\n")

    # Inizializza il motore della Rete Bayesiana
    risk_engine = RiskAnalyzer()

    # ---------------------------------------------------------
    # DEFINIZIONE DEI DUE CASI DI STUDIO
    # ---------------------------------------------------------
    scenarios = [
        {
            "nome": "SCENARIO A (Emergenza)", 
            "meteo": 1, "carico": 1, 
            "desc_meteo": "Nuvoloso", "desc_carico": "Alto"
        },
        {
            "nome": "SCENARIO B (Tranquillo)", 
            "meteo": 0, "carico": 0, 
            "desc_meteo": "Sole", "desc_carico": "Basso"
        }
    ]

    # Eseguiamo il programma per entrambi gli scenari
    for scenario in scenarios:
        print(f"==================================================")
        print(f" ESECUZIONE {scenario['nome']}")
        print(f"==================================================")
        
        # 2. Rete Bayesiana
        print(f"[Bayes] Lettura sensori: Meteo={scenario['desc_meteo']}, Carico={scenario['desc_carico']}")
        prob_blackout = risk_engine.get_blackout_probability(meteo_val=scenario['meteo'], carico_val=scenario['carico']) 
        print(f"Probabilità di Blackout calcolata: {prob_blackout:.2f}")

        # Se c'è rischio, interviene lo Scheduler
        if prob_blackout > 0.5:
            print(">>> ATTENZIONE: Rischio elevato rilevato. L'Agente attiva lo Scheduler Ottimizzato.")
            
            # 3. Scheduling (CSP + Prolog)
            print("\n[CSP] Avvio pianificazione dispositivi consultando la KB Prolog...")
            
            base_path = os.path.dirname(os.path.abspath(__file__))
            kb_path = os.path.join(base_path, "..", "dataset", "devices_rules.pl")
            
            try:
                scheduler = EnergyScheduler(kb_path)
                to_schedule = ["lavatrice", "forno", "auto_elettrica"]
                print(f"Dispositivi richiesti dall'utente: {to_schedule}")
                
                solutions = scheduler.schedule_devices(to_schedule)
                
                if solutions:
                    print(f"Trovate {len(solutions)} pianificazioni valide. Ecco la migliore (ottimale):")
                    # Prendiamo sempre la prima soluzione per rendere la demo riproducibile
                    best_sol = solutions[0] 
                    
                    sorted_sol = sorted(best_sol.items(), key=lambda item: item[1])
                    
                    for dev, time in sorted_sol:
                        # Chiediamo a Prolog quanti kW consuma questo specifico dispositivo
                        power = scheduler.kb.get_device_power(dev)
                        print(f" - {dev.ljust(15)} ({power} kW) : Accendere alle ore {time}:00")
                    
                    # --- Generazione Grafico ---
                    print("\n[Grafico] Generazione in corso...")
                    ore = list(range(8, 24))
                    consumi = [0.0] * len(ore)
                    
                    for dev, time in best_sol.items():
                        power = scheduler.kb.get_device_power(dev)
                        indice_ora = time - 8
                        consumi[indice_ora] += power
                    
                    plt.figure(figsize=(10, 6))
                    plt.bar(ore, consumi, color='#ff9800', edgecolor='black', width=0.6)
                    plt.axhline(y=3.5, color='red', linestyle='--', linewidth=2, label='Limite Contatore (3.5 kW)')
                    
                    plt.xlabel('Ora del Giorno', fontsize=12)
                    plt.ylabel('Potenza Stimata (kW)', fontsize=12)
                    plt.title(f'EcoOptima - Profilo Consumi ({scenario["nome"]})', fontsize=14, fontweight='bold')
                    plt.xticks(ore)
                    plt.yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
                    plt.legend()
                    plt.grid(axis='y', linestyle=':', alpha=0.7)
                    plt.tight_layout()
                    
                    print(">>> NOTA: Chiudi la finestra del grafico per far proseguire il programma.\n")
                    plt.show()
                    
                else:
                    print("Nessuna soluzione trovata! Impossibile rispettare i vincoli.\n")
                    
            except Exception as e:
                print(f"Errore nel caricamento della KB Prolog o nel CSP: {e}\n")
        
        # Se il rischio è basso, l'intelligenza artificiale non blocca l'utente
        else:
            print(">>> STATO SICURO: Nessun rischio imminente.")
            print(">>> L'Agente lascia all'utente libertà d'uso totale sui dispositivi.")
            print(">>> (Il modulo Prolog/CSP rimane in standby).\n")

if __name__ == "__main__":
    main()
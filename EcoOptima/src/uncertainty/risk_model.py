# --- FILE AGGIORNATO: src/uncertainty/risk_model.py ---
from pgmpy.models import DiscreteBayesianNetwork  # <--- CAMBIATO QUI
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class RiskAnalyzer:
    def __init__(self):
        # Struttura: Meteo -> Solare -> Rischio <- Carico Rete
        # Abbiamo sostituito BayesianNetwork con DiscreteBayesianNetwork
        self.model = DiscreteBayesianNetwork([
            ('Meteo', 'Solare'),
            ('Solare', 'Rischio'),
            ('Carico', 'Rischio')
        ])
        
        # Definizioni Probabilità (CPD)
        # Meteo: 0=Sole, 1=Nuvoloso
        cpd_meteo = TabularCPD(variable='Meteo', variable_card=2, values=[[0.7], [0.3]]) 
        # Carico: 0=Basso, 1=Alto
        cpd_carico = TabularCPD(variable='Carico', variable_card=2, values=[[0.6], [0.4]]) 

        # Se Sole(0), Solare è Alto(1) con prob 0.9.
        cpd_solare = TabularCPD(variable='Solare', variable_card=2, 
                                values=[[0.1, 0.8], [0.9, 0.2]],
                                evidence=['Meteo'], evidence_card=[2])

        # Rischio dipende da Solare e Carico
        cpd_rischio = TabularCPD(variable='Rischio', variable_card=2,
                                 values=[[0.9, 0.6, 0.7, 0.1],  # No Rischio
                                         [0.1, 0.4, 0.3, 0.9]], # Si Rischio (High)
                                 evidence=['Solare', 'Carico'], evidence_card=[2, 2])

        self.model.add_cpds(cpd_meteo, cpd_carico, cpd_solare, cpd_rischio)
        
        # Verifica che il modello sia valido
        assert self.model.check_model()
        self.infer = VariableElimination(self.model)

    def get_blackout_probability(self, meteo_val, carico_val):
        # meteo_val: 0 (Sole), 1 (Nuvoloso)
        result = self.infer.query(variables=['Rischio'], evidence={'Meteo': meteo_val, 'Carico': carico_val})
        return result.values[1] # Restituisce la probabilità dell'evento 1 (Rischio Alto)
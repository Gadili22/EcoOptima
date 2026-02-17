from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class RiskAnalyzer:
    def __init__(self):
        # Struttura: Meteo -> Solare -> Rischio <- Carico Rete
        self.model = DiscreteBayesianNetwork([
            ('Meteo', 'Solare'),
            ('Solare', 'Rischio'),
            ('Carico', 'Rischio')
        ])
        
        # Meteo: 0=Sole, 1=Nuvoloso
        cpd_meteo = TabularCPD(variable='Meteo', variable_card=2, values=[[0.7], [0.3]]) 
        # Carico: 0=Basso, 1=Alto
        cpd_carico = TabularCPD(variable='Carico', variable_card=2, values=[[0.6], [0.4]]) 

        # Se Sole(0), Solare è Alto(1) con prob 0.9. Se Nuvoloso(1) Solare è Basso(0) con prob 0.8.
        cpd_solare = TabularCPD(variable='Solare', variable_card=2, 
                                values=[[0.1, 0.8], 
                                        [0.9, 0.2]],
                                evidence=['Meteo'], evidence_card=[2])

        # --- TABELLA CORRETTA ---
        # Colonne: [Solare=0,Carico=0], [Solare=0,Carico=1], [Solare=1,Carico=0], [Solare=1,Carico=1]
        # Solare 0 = Basso, Solare 1 = Alto
        cpd_rischio = TabularCPD(variable='Rischio', variable_card=2,
                                 values=[
                                     # Probabilità Rischio Basso (0)
                                     [0.90, 0.10, 0.95, 0.70],  
                                     # Probabilità Rischio Alto (1) -> Blackout
                                     [0.10, 0.90, 0.05, 0.30]   
                                 ],
                                 evidence=['Solare', 'Carico'], evidence_card=[2, 2])

        self.model.add_cpds(cpd_meteo, cpd_carico, cpd_solare, cpd_rischio)
        assert self.model.check_model()
        self.infer = VariableElimination(self.model)

    def get_blackout_probability(self, meteo_val, carico_val):
        result = self.infer.query(variables=['Rischio'], evidence={'Meteo': meteo_val, 'Carico': carico_val})
        return result.values[1]
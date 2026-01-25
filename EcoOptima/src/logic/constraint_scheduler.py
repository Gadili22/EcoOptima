from constraint import *
from .prolog_interface import DeviceKB

class EnergyScheduler:
    def __init__(self, kb_path):
        self.kb = DeviceKB(kb_path)
        self.problem = Problem()
        self.max_power = 3.5  # kW massimi del contatore

    def schedule_devices(self, devices_to_schedule):
        # Variabili: I dispositivi. Dominio: Ore del giorno (0-23)
        # Supponiamo attività dalle 8 alle 24
        for dev in devices_to_schedule:
            self.problem.addVariable(dev, range(8, 24)) 

        # VINCOLO 1: Incompatibilità logica (dalla KB Prolog)
        incompatible_pairs = self.kb.get_incompatible_pairs()
        for dev1, dev2 in incompatible_pairs:
            if dev1 in devices_to_schedule and dev2 in devices_to_schedule:
                # Non possono essere accesi alla stessa ora
                self.problem.addConstraint(lambda a, b: a != b, (dev1, dev2))

        # VINCOLO 2: Potenza massima (Somma carichi < Max Power)
        all_vars = devices_to_schedule
        
        def max_power_constraint(*times):
            # Raggruppa device per orario scelto
            usage_at_time = {}
            for i, time in enumerate(times):
                dev = all_vars[i]
                power = self.kb.get_device_power(dev)
                usage_at_time[time] = usage_at_time.get(time, 0) + power
            
            # Controlla se qualche ora supera il limite
            for t in usage_at_time:
                if usage_at_time[t] > self.max_power:
                    return False
            return True

        self.problem.addConstraint(max_power_constraint, all_vars)

        return self.problem.getSolutions()
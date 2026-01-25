from pyswip import Prolog

class DeviceKB:
    def __init__(self, pl_file_path):
        self.prolog = Prolog()
        # Converte il path di Windows per renderlo compatibile con Prolog
        path_str = pl_file_path.replace("\\", "/")
        self.prolog.consult(path_str)

    def get_incompatible_pairs(self):
        """Recupera coppie di device incompatibili dalla KB."""
        query = "incompatible(X, Y)"
        pairs = set()
        for soln in self.prolog.query(query):
            # Ordina per evitare duplicati (es. A-B e B-A)
            pair = tuple(sorted((soln["X"], soln["Y"])))
            pairs.add(pair)
        return list(pairs)

    def get_device_power(self, device_name):
        """Recupera la potenza di un device."""
        query = f"device({device_name}, P, _)"
        for soln in self.prolog.query(query):
            return float(soln["P"])
        return 0.0
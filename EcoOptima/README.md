# EcoOptima: Sistema intelligente di gestione dell'energia domestica 🏠⚡

**EcoOptima** è un simulatore di Agente Intelligente per la domotica. Ottimizza i consumi elettrici domestici, prevede i costi dell'energia e previene i blackout pianificando l'accensione degli elettrodomestici nel rispetto del limite fisico del contatore (es. 3.5 kW).

## 🚀 Quick Start (Installazione e Avvio)

### 1. Prerequisiti
* **Python 3.1x**
* **SWI-Prolog:** È strettamente necessario averlo installato sul proprio sistema operativo affinché la libreria *pyswip* possa comunicare con la Knowledge Base logica ([Download ufficiale qui](https://www.swi-prolog.org/Download.html)).

### 2. Installazione delle dipendenze
Per evitare ridondanze e mantenere il progetto pulito, tutte le librerie esterne necessarie sono gestite automaticamente. Apri il terminale nella cartella del progetto e lancia:

    pip install -r requirements.txt

### 3. Esecuzione
Avvia l'Agente Intelligente con il comando:

    python src/main.py
> **Nota:** Su Windows potrebbe essere necessario usare il comando `py src/main.py`, mentre su Mac/Linux `python3 src/main.py`.

Al suo avvio, l'Agente eseguirà automaticamente due scenari di test:

* **Scenario A (Emergenza):** Rischio di blackout alto. L'Agente interviene e genera un Grafico a Barre con la ripianificazione sicura degli elettrodomestici per non superare i 3.5 kW. *(Chiudere la finestra del grafico per far proseguire il programma).*
* **Scenario B (Standby):** Rischio basso. L'Agente lascia libertà d'azione all'utente per risparmiare risorse di calcolo.

## 📊 Nota sul Dataset (Auto-Generazione)

Il file storico dei consumi (`dataset/energy_data.csv`) è già incluso nel repository per comodità di valutazione. Tuttavia, il sistema è dotato di un modulo di persistenza intelligente: se il file viene rimosso dalla cartella, al successivo avvio l'Agente genererà automaticamente un nuovo storico realistico di 1000 ore, iniettando del rumore statistico per prevenire l'overfitting del modello predittivo.

---
**Sviluppato da:** Gabriele Di Liso - *Progetto Ingegneria della Conoscenza A.A 2025-2026*
# Fantapalla_Forever_database

## A fun, leisure project of Fantasy Football


La repo e' suddivisa nelle seguenti cartelle:

- Prototyping: contiene notebook temporanei utilizzati per la fase di costruzione degli algoritmi
- Logos: contiene il logo di ciascuna squadra del torneo
- Algoritmo_rose: contiene algoritmi e dati usati per generare le rose all'inizio della competizione
- IGNOBEL: contiene tutti i notebook e gli script usati per i premi speciali e per le statistiche


## Algoritmo Rose

Il programma compie le seguenti operazioni 

  - genera una rosa sulla base del numero di squadre prendendo gli N giocatori con quotazione piu' alta, dove N = numero_squdre * giocatori_rosa
  - simula un campionato di 38 giornate creando accoppiamenti random ad ogni giornata (se numero_squadre << numero_girnate non ci sono problemi di fluttuazioni statistiche)
  - per ogni giornata recupera i voti della corrispettiva giornata nel campionato 2019/20
  - calcola il voto squadra per ogni rosa, schierando automaticamente la formazione migliore sulla base degli schemi disponibili e tenendo conto del modificatore difesa
  - calcola i punti di giornata secondo gli accoppiamenti
  - calcola la classifica finale e salva la rosa solo se il range di punti in classifica (+ tolleranza) e il range di quotazioni rosa sono piu' bassi di quelli della rosa simulata precedentemente
  - repeat
  
Cosi' dopo N_campionati simulati si trova la rosa che minimizza le differenze di prestazioni e di valore

La versione aggiornata assegna le rose parziali solo sulla base delle quotazioni. Si trova nel notebook 

Rose_quotazioni.ipynb

che sfrutta lo stesso python script.

## IGNOBEL 

Sono presenti 2 notebook principali:

- IGNOBEL, che sfrutta il relativo script di utilities per fare webparsing sul sito fantacalcio.it ed estrarre tutti i risultati di giornata necessari per calcolare premi e statistiche, e salva tutti nelle cartelle Dati

- FantapallaStats, che prende i dati dalle cartelle e permette il calcolo di statistiche e premi IGNOBEL

- FantapallaStats_2.0, nuova versione piu' modulare del precedente notebook, che riversa sullo script relativo la definizione delle varie funzioni

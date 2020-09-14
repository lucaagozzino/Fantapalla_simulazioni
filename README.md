# Fantapalla_simulazioni

Il programma compie le seguenti operazioni 

  - genera una rosa sulla base del numero di squadre prendendo gli N giocatori con quotazione piu' alta, dove N = numero_squdre * giocatori_rosa
  - simula un campionato di 38 giornate creando accoppiamenti random ad ogni giornata (se numero_squadre << numero_girnate non ci sono problemi di fluttuazioni statistiche)
  - per ogni giornata recupera i voti della corrispettiva giornata nel campionato 2019/20
  - calcola il voto squadra per ogni rosa, schierando automaticamente la formazione migliore sulla base degli schemi disponibili e tenendo conto del modificatore difesa
  - calcola i punti di giornata secondo gli accoppiamenti
  - calcola la classifica finale e salva la rosa solo se il range di punti in classifica (+ tolleranza) e il range di quotazioni rosa sono piu' bassi di quelli della rosa simulata precedentemente
  - repeat
  
Cosi' dopo N_campionati simulati si trova la rosa che minimizza le differenze di prestazioni e di valore

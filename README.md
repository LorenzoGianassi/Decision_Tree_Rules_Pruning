# Progetto_AI
Elaborato per l'esame di Intelligena Artificiale
# Esecuzione
- Scaricare e  salvare nella cartella del Progetto un file .csv , in particolare il file Dataset.py si occuperà in modo specifico del dataset utilizzato (cioè Adult dataset, link :https://archive.ics.uci.edu/ml/datasets/adult) quindi saranno necessarie delle modifiche al codice presente in quella classe nel caso in cui si volesse utilizzare un altro dataset. Nel file .csv sarà necessario che nella prima riga siano presenti i nomi degli attributi del dataset. Per il parse del Dataset ho utilizzato Pandas, quindi sarà necessario scaricare anch'esso.
- Nel file Main.py eseguiremo più test per avere dei risultati omogenei, inoltre sarà necessario cambiare il nome del file (nel caso in cui si volesse cambiare dataset) e i valori realtivi alle classi che nel ostro caso saranno '<=50K', '>50K'. 
- Può essere inoltre modificato il numero di Test eseguibili, di default sono 3.

I tempi di esecuzione possono variare a seconda della dimensione del dataset e  dal numero di test svolti, nel mio caso per ciascuna iterazione impiega circa 10 minuti (l'operazione è quella che richiede maggior parte del tempo).

Per la realizzaione di questo progetto ho consultato le seguenti fonti:
- Una repository pubblica riadattata al mio problema : https://github.com/aimacode/aima-python/blob/master/learning.py
- Il paragrafo del libro fornito dalla richiesta del problema : Mitchell, 1997
- Libro di testo : 'Artificial Intelligence: A Modern Approach', di Stuart J. Russell and Peter Norvig

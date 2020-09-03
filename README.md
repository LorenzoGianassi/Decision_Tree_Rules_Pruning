# Progetto_AI
Elaborato per l'esame di Intelligena Artificiale
# Esecuzione
- Scaricare e  salvare nella cartella del Progetto un file .csv , in particolare il file Dataset.py si occuperà in modo specifico del dataset utilizzato (cioè Adult dataset, link :https://archive.ics.uci.edu/ml/datasets/adult) quindi saranno necessarie delle modifiche al codice presente in quella classe nel caso in cui si volesse utilizzare un altro dataset. Nel file .csv sarà necessario che nella prima riga siano presenti i nomi degli attributi del dataset. Per il parse del Dataset ho utilizzato Pandas, quindi sarà necessario scaricare anch'esso.
- Nel file Main.py eseguiremo più test in modo tale da analizzare più approfonditamente il problema. In particolare come variano le accuracy a variare della depth dell'albero e del numero di esempi che si utilizzano per creare e testare l'albero.

I tempi di esecuzione possono variare a seconda della dimensione del dataset e dalla profondità dell'albero(l'operazione di pruning è quella che richiede maggior parte del tempo).

Per la realizzaione di questo progetto ho consultato le seguenti fonti:
- Una repository pubblica riadattata al mio problema : https://github.com/aimacode/aima-python/blob/master/learning.py
- Il paragrafo del libro fornito dalla richiesta del problema : Mitchell, 1997
- Libro di testo : 'Artificial Intelligence: A Modern Approach', di Stuart J. Russell and Peter Norvig

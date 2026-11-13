# InForma — diario di allenamento

App mobile scritta in Python con Kivy, con interfaccia in italiano e dati salvati
localmente sul dispositivo. Il progetto condivide lo stesso codice tra Android e
iOS; un APK funziona solo su Android, mentre su iPhone va generata e installata
un'app iOS.

## Funzioni

- Catalogo di oltre 120 esercizi, con ricerca e categorie.
- Fino a 5 schede personalizzabili, ciascuna con 3 giorni iniziali e fino a 7;
  il giorno si sceglie prima di iniziare l'allenamento.
- Registrazione di ripetizioni e carico per ogni serie.
- Record per esercizio e grafico dei carichi degli ultimi 60 giorni.
- Registrazione del peso corporeo e grafico degli ultimi 60 giorni.
- Storico espandibile delle sessioni degli ultimi 30 giorni: mostra data e
  giorno dell'allenamento; toccando una sessione si vedono esercizi e valori
  registrati per ogni serie.
- Profilo locale con nome, sesso ed età; il nome personalizza il saluto iniziale.
- Preferenze salvate per i promemoria di allenamento e peso, con orario e
  frequenza configurabile per entrambi (allenamento: 1, 2, 3 o 7 giorni;
  peso: 1, 2 o 3 settimane).
- Nome personalizzabile per ogni giorno e azzeramento del contatore degli
  allenamenti completati senza cancellare sessioni, record o grafici.
- Svuotamento della cache temporanea dalle impostazioni, senza eliminare i dati
  salvati.
- Salvataggio privato in un file JSON nell'area dati dell'app.

Le preferenze di promemoria e frequenza sono memorizzate, ma l'invio automatico
a app chiusa richiede ancora l'integrazione con le notifiche locali native di
Android e iOS e la configurazione dei relativi permessi nella build.



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

## Android — APK

Buildozer compila su Linux. Su Windows si può usare WSL con una distribuzione
Linux; per l'installazione di Kivy e Buildozer seguire la documentazione
Buildozer per la propria distribuzione.

```bash
python3 -m pip install -r requirements.txt buildozer
buildozer android debug
```

L'APK di debug viene creato in `bin/`. Per distribuirlo fuori dal proprio
dispositivo di test occorre generare una build firmata per il rilascio.

## iPhone — app iOS

La build iOS richiede macOS, Xcode e gli strumenti `kivy-ios`. Su un Mac, dopo
aver installato gli strumenti richiesti dalla documentazione di Kivy:

```bash
python3 -m pip install kivy-ios
toolchain build python3 kivy
toolchain create InForma .
```

Aprire il progetto Xcode generato, configurare il proprio Team di firma e
compilare su un iPhone o creare un archivio da distribuire con TestFlight. Non
è possibile installare un APK su iPhone né produrre la build iOS direttamente
da Windows.

## Avvio sul computer

```bash
python -m pip install -r requirements.txt
python main.py
```

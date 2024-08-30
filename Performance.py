import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def add1d(Heute):
    Heute_datetime = datetime.strptime(Heute, '%Y-%m-%d')
    neuesDatum = Heute_datetime + timedelta(days=1)
    neuesDatum_str = neuesDatum.strftime('%Y-%m-%d')
    return neuesDatum_str


def sell(cash, Aktienkurs, anzahl, entnahme_verteilung):
    while cash < entnahme_verteilung:
        anzahl -= 1
        cash += Aktienkurs
    cash -= entnahme_verteilung
    return cash, anzahl


def Performance(LstPerson, LstPort, Entnahme):
    Name = LstPerson[0]
    Anlagevermögen = int(LstPerson[1])
    Startzeitpunkt = LstPerson[2]
    Endzeitpunkt = LstPerson[3]

    PortfolioString = LstPort[1]
    portfolio_list = eval(PortfolioString)

    Id = LstPort[0]

    Entnahme = float(Entnahme)
    Ticker = [ticker[0] for ticker in portfolio_list]
    Verteilung = [float(verteilung[1]) for verteilung in portfolio_list]

    # Aufteilung Anlagevermögen
    Anlagevermögen_Split = []
    for Verteilungswert in Verteilung:
        Eintrag = Anlagevermögen * Verteilungswert
        Anlagevermögen_Split.append(Eintrag)

    # Kursdaten herunterladen
    Kurswerte = []
    for tickers in Ticker:
        # Lade Kursdaten für den aktuellen Ticker herunter
        kursdaten = yf.download(tickers, start=Startzeitpunkt, end=Endzeitpunkt)
        # Füge den Ticker und die Kursdaten als Tupel zur Liste hinzu
        Kurswerte.append((tickers, kursdaten))

    # Startkurse filtern
    Startpreis = []
    for Kurswerte_Element in Kurswerte:
        startpreis = Kurswerte_Element[1].iloc[0]['Close']
        Startpreis.append(startpreis)


    # Simulation Wertpapierkauf
    Anzahl = []
    for startpreis, anlagevermoegen_split in zip(Startpreis, Anlagevermögen_Split):
        anzahl = int(anlagevermoegen_split / startpreis)
        Anzahl.append(anzahl)


    Cash = Anlagevermögen
    for anzahl, startpreis in zip(Anzahl, Startpreis):
        Cash = Cash - (anzahl * startpreis)

    # Entnahmewert aufteilen
    Entnahme_Verteilung = [verteilungswert * Entnahme for verteilungswert in Verteilung]

    Heute = Startzeitpunkt
    Dataframe_Master_Werte = []
    Dataframe_Slave_Werte = []
    for Add_Werte in Dataframe_Master_Werte:
        Dataframe_Slave_Werte.append(Add_Werte)

    # Füllung der Dataframe Listen
    for Kurswerte_Element, anzahl, entnahme_verteilung in zip(Kurswerte, Anzahl, Entnahme_Verteilung):
        Heute = Startzeitpunkt
        Entnahme_Count = 0
        Dataframe_Slave_Werte = []
        while Heute <= Endzeitpunkt:
            if Heute in Kurswerte_Element[1].index:
                Aktienkurs = Kurswerte_Element[1].loc[Heute, 'Close']
                if Entnahme_Count % 30 == 0:
                    Cash, anzahl = sell(Cash, Aktienkurs, anzahl, entnahme_verteilung)
                Vermögen = Aktienkurs * anzahl + Cash
                Dataframe_Slave_Werte.append((Heute, Vermögen))
            Heute = add1d(Heute=Heute)
            Entnahme_Count += 1
        Dataframe_Master_Werte.append(Dataframe_Slave_Werte)

    # Dataframes zusammenführen
    Dataframe_Ausgabe = []
    i = 0
    for j in range(len(Dataframe_Slave_Werte)):
        Vermögen = 0
        for Slave_Liste in Dataframe_Master_Werte:
            Vermögen += Slave_Liste[i][1]
            Heute = Slave_Liste[i][0]
        Dataframe_Ausgabe.append((Heute, Vermögen))
        i += 1

    # Daten in ein DataFrame umwandeln
    Dataframe = pd.DataFrame(Dataframe_Ausgabe, columns=['Date', 'Stock Price'])
    Dataframe['Date'] = pd.to_datetime(Dataframe['Date'])
    Dataframe.set_index('Date', inplace=True)

    # Plot erstellen
    Dataframe['Stock Price'].plot(figsize=(10, 6), title=Id)
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.show()

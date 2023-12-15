import os
import tkinter as tk
from tkinter.ttk import Treeview
from tkinter import ttk
import xml.etree.ElementTree as ET


class Serialisierung:
    @staticmethod
    def Speichern(liste, dateipfad):
        try:
            tree = ET.parse(dateipfad)
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            # Die Datei existiert nicht oder ist fehlerhaft, erstelle ein neues Element
            root = ET.Element("Liste")

        # Füge einen neuen "Array"-Eintrag hinzu
        array_element = ET.SubElement(root, "Array")

        # Füge neue Einträge hinzu
        for element in liste:
            eintrag = ET.SubElement(array_element, "Eintrag")
            eintrag.text = str(element)

        tree = ET.ElementTree(root)
        with open(dateipfad, "wb") as datei:
            tree.write(datei)

    @staticmethod
    def Laden(dateipfad):
        try:
            tree = ET.parse(dateipfad)
            root = tree.getroot()

            geladene_liste = []

            # Lade Einträge aus jedem "Array"-Element
            for array_element in root.findall("Array"):
                array = [Serialisierung._konvertiere_typ(eintrag.text) for eintrag in array_element.findall("Eintrag")]
                geladene_liste.append(array)

            return geladene_liste
        except FileNotFoundError:
            print(f"Die Datei {dateipfad} wurde nicht gefunden.")
            return None
        except ET.ParseError:
            print(f"Fehler beim Parsen der XML-Datei {dateipfad}.")
            return None

    @staticmethod
    def _konvertiere_typ(text):
        try:
            return int(text)
        except ValueError:
            try:
                return float(text)
            except ValueError:
                return text

    @staticmethod
    def Entferne_array_element(dateipfad, index):
        try:
            tree = ET.parse(dateipfad)
            root = tree.getroot()

            # Finde das "Array"-Element mit dem gegebenen Index und entferne es
            array_elements = root.findall("Array")
            if 0 <= index < len(array_elements):
                root.remove(array_elements[index])

                # Speichere die aktualisierte Datei
                tree = ET.ElementTree(root)
                with open(dateipfad, "wb") as datei:
                    tree.write(datei)

                print(f"Das 'Array'-Element mit dem Index {index} wurde entfernt.")
            else:
                print(f"Ungültiger Index: {index}")

        except (FileNotFoundError, ET.ParseError):
            print(f"Fehler beim Laden der XML-Datei {dateipfad} oder das 'Array'-Element konnte nicht entfernt werden.")

    @staticmethod
    def Create_xml(dateipfad):
        root = ET.Element("Daten")
        tree = ET.ElementTree(root)
        with open(dateipfad, "w", encoding="utf-8") as datei:
            tree.write(datei, encoding="unicode")


class Überschrift:
    def __init__(self, master, text, x, y):
        self.label_parameter = {
            'text': text,
            'bg': 'darkgrey',
            'fg': 'white',
            'font': ('Helvetica', 14, 'bold'),
        }

        self.label = tk.Label(master, **self.label_parameter)
        self.label.place(x=x, y=y)


class Beschriftung:
    def __init__(self, master, text, x, y):
        self.label_parameter = {
            'text': text,
            'bg': 'darkgrey',
            'fg': 'white',
            'font': ('Helvetica', 14),
        }

        self.label = tk.Label(master, **self.label_parameter)
        self.label.place(x=x, y=y)


class Button_Menu:

    def __init__(self, master, text, command=None, x=0, y=0):
        self.button_parameter = {
            'text': text,
            'bg': 'black',
            'fg': 'white',
            'font': ('Helvetica', 14),
        }

        if command is not None:
            self.button_parameter['command'] = command

        self.button = tk.Button(master, **self.button_parameter)
        self.button.place(x=x, y=y)


class Button_Standard:

    def __init__(self, master, text, command=None, x=0, y=0):
        self.button_parameter = {
            'text': text,
            'bg': 'white',
            'fg': 'black',
            'font': ('Helvetica', 10),
        }

        if command is not None:
            self.button_parameter['command'] = command

        self.button = tk.Button(master, **self.button_parameter)
        self.button.place(x=x, y=y)


def zeige_StartWindow():
    Frame_PersonErstellen.place_forget()
    Frame_Ausgabe.place_forget()
    Frame_PortfolioErstellen.place_forget()
    Frame_StartWindow.place(x=0, y=50)


def zeige_PersonAnlegen():
    Frame_StartWindow.place_forget()
    Frame_Ausgabe.place_forget()
    Frame_PortfolioErstellen.place_forget()
    Frame_PersonErstellen.place(x=0, y=50)


def zeige_PortfolioErstellen():
    Frame_StartWindow.place_forget()
    Frame_PersonErstellen.place_forget()
    Frame_Ausgabe.place_forget()
    Frame_PortfolioErstellen.place(x=0, y=50)


def zeige_Ausgabe():
    Frame_StartWindow.place_forget()
    Frame_PersonErstellen.place_forget()
    Frame_PortfolioErstellen.place_forget()
    Frame_Ausgabe.place(x=0, y=50)


def CreatePerson():
    Liste = [Entry_NameEingeben.get(), Entry_Anlagevermögen.get(), Entry_Startzeitpunkt.get(), Entry_Endzeitpunkt.get()]
    PersonListe.append(Liste)
    Serialisierung.Speichern(Liste, 'PersonListe.xml')
    Entry_NameEingeben.delete(0, 'end')
    Entry_Anlagevermögen.delete(0, 'end')
    Entry_Startzeitpunkt.delete(0, 'end')
    Entry_Endzeitpunkt.delete(0, 'end')
    Combobox_ElementePerson = [element[0] for element in PersonListe]
    ComboBox_Person['values'] = Combobox_ElementePerson


def On_comboboxPerson_select(event):
    selected_index = ComboBox_Person.current()
    selected_person_data = PersonListe[selected_index]
    print("Ausgewählte Daten:", selected_person_data)


def Remove_selected_person():
    selected_index = ComboBox_Person.current()
    print(selected_index)
    if selected_index != -1:  # Überprüfen, ob etwas ausgewählt wurde
        removed_person = PersonListe.pop(selected_index)
        print("Entfernte Person:", removed_person)
        # Aktualisiere die ComboBox-Optionen
        Combobox_ElementePerson = [element[0] for element in PersonListe]
        ComboBox_Person['values'] = Combobox_ElementePerson
        # Zelleninhalt leeren
        ComboBox_Person.set('')
    Serialisierung.Entferne_array_element('PersonListe.xml', selected_index)


def AddToPortfolio():
    data_grid.insert("", "end", values=(Entry_TickerEingeben.get(), Entry_VerteilungEingeben.get()))
    PortfolioListe1.append((Entry_TickerEingeben.get(), int(Entry_VerteilungEingeben.get())))
    Entry_TickerEingeben.delete(0, 'end')
    Entry_VerteilungEingeben.delete(0, 'end')


def FinishPortfolio():
    Summe_Anzahl = 0
    for Element in PortfolioListe1:
        Summe_Anzahl += Element[1]
    for Element in PortfolioListe1:
        Verteilungswert = Element[1] / Summe_Anzahl
        PortfolioListe2.append((Element[0], Verteilungswert))
    Liste = [Entry_PortfolioId.get(), PortfolioListe2]
    Serialisierung.Speichern(Liste, 'PortListe.xml')
    PortfolioListe3.append(Liste)
    Combobox_ElementePort = [element[0] for element in PortfolioListe3]
    ComboBox_Port['values'] = Combobox_ElementePort
    Entry_PortfolioId.delete(0, 'end')
    PortfolioListe1.clear()
    ClearDataGrid(data_grid)


def On_comboboxPort_select(event):
    selected_index = ComboBox_Port.current()
    selected_port_data = PortfolioListe3[selected_index]
    print("Ausgewählte Daten:", selected_port_data)


def Remove_selected_Port():
    selected_index = ComboBox_Port.current()

    if selected_index != -1:  # Überprüfen, ob etwas ausgewählt wurde
        removed_person = PortfolioListe3.pop(selected_index)
        print("Entfernte Person:", removed_person)
        # Aktualisiere die ComboBox-Optionen
        Combobox_ElementePort = [element[0] for element in PortfolioListe3]
        ComboBox_Port['values'] = Combobox_ElementePort
        # Leere den Zelleninhalt
        ComboBox_Port.set("")


def ClearDataGrid(self):
    for item in self.get_children():
        self.delete(item)


def startGUI():
    root.mainloop()


XML_PersonListe = "PersonListe.xml"
XML_PortListe = "PortListe.xml"
# Überprüfen, ob die Datei bereits existiert
if not os.path.exists(XML_PersonListe):
    # Falls nicht, erstelle die Datei mit einer leeren Liste
    Serialisierung.Create_xml(XML_PersonListe)
if not os.path.exists(XML_PortListe):
    # Falls nicht, erstelle die Datei mit einer leeren Liste
    Serialisierung.Create_xml(XML_PortListe)

PersonListe = Serialisierung.Laden('PersonListe.xml')

PortfolioListe1 = []
PortfolioListe2 = []
PortfolioListe3 = Serialisierung.Laden('PortListe.xml')

root = tk.Tk()
root.geometry("800x600")

Frame_StartWindow = tk.Frame(root, bg='darkgray', width=800, height=550)
Frame_StartWindow.place(x=0, y=50)
Label_StartWindow_1 = Überschrift(Frame_StartWindow, text='Willkommen im Portfolio Manager', x=250, y=3)

Frame_PersonErstellen = tk.Frame(root, bg='darkgray', width=800, height=550)

Label_NameEingeben = Beschriftung(Frame_PersonErstellen, text='Name eingeben:', x=40, y=40)
Entry_NameEingeben = tk.Entry(Frame_PersonErstellen)
Entry_NameEingeben.place(x=40, y=70)

Label_Anlagevermögen = Beschriftung(Frame_PersonErstellen, text='Anlagevermögen eingeben:', x=40, y=110)
Entry_Anlagevermögen = tk.Entry(Frame_PersonErstellen)
Entry_Anlagevermögen.place(x=40, y=140)

Label_Startzeitpunkt = Beschriftung(Frame_PersonErstellen, text='Startzeitpunkt eingeben:', x=40, y=180)
Entry_Startzeitpunkt = tk.Entry(Frame_PersonErstellen)
Entry_Startzeitpunkt.place(x=40, y=210)

Label_Endzeitpunkt = Beschriftung(Frame_PersonErstellen, text='Endzeitpunkt eingeben:', x=40, y=250)
Entry_Endzeitpunkt = tk.Entry(Frame_PersonErstellen)
Entry_Endzeitpunkt.place(x=40, y=280)

Button_PersonErstellen = Button_Standard(Frame_PersonErstellen, text='Person erstellen', command=CreatePerson, x=300,
                                         y=50)

Frame_PortfolioErstellen = tk.Frame(root, bg='darkgray', width=800, height=550)

Label_PortfolioId = Beschriftung(Frame_PortfolioErstellen, 'Id eingeben:', x=40, y=40)
Entry_PortfolioId = tk.Entry(Frame_PortfolioErstellen)
Entry_PortfolioId.place(x=40, y=70)

Label_TickerEingeben = Beschriftung(Frame_PortfolioErstellen, 'Ticker eingeben:', x=240, y=40)
Entry_TickerEingeben = tk.Entry(Frame_PortfolioErstellen)
Entry_TickerEingeben.place(x=240, y=70)

Label_VerteilungEingeben = Beschriftung(Frame_PortfolioErstellen, 'Verteilung eingeben:', x=440, y=40)
Entry_VerteilungEingeben = tk.Entry(Frame_PortfolioErstellen)
Entry_VerteilungEingeben.place(x=440, y=70)

Btn_AddTo_Port = Button_Standard(Frame_PortfolioErstellen, 'Zu Portfolio hinzufügen', x=550, y=140,
                                 command=AddToPortfolio)
Btn_Finish_Port = Button_Standard(Frame_PortfolioErstellen, 'Portfolio fertigstellen', x=550, y=200,
                                  command=FinishPortfolio)

data_grid = Treeview(Frame_PortfolioErstellen, columns=("Ticker", "Verteilung"))
data_grid.heading("#1", text="Ticker")
data_grid.heading("#2", text="Verteilung")
data_grid.place(x=10, y=140, width=500, height=300)
data_grid.column("#0", width=0)

Frame_Ausgabe = tk.Frame(root, bg='darkgray', width=800, height=550)

Label_PersonAuswahl = Beschriftung(Frame_Ausgabe, 'Person Auswahl', x=40, y=40)
ComboBox_Person = ttk.Combobox(Frame_Ausgabe)
ComboBox_Person.place(x=40, y=70)
ComboBox_Person.bind("<<ComboboxSelected>>", On_comboboxPerson_select)
Button_del_Person = Button_Standard(Frame_Ausgabe, 'Person löschen', command=Remove_selected_person, x=300, y=60)

Label_PortfolioAuswahl = Beschriftung(Frame_Ausgabe, 'Portfolio Auswahl', x=40, y=120)
ComboBox_Port = ttk.Combobox(Frame_Ausgabe)
ComboBox_Port.place(x=40, y=150)
ComboBox_Port.bind("<<ComboboxSelected>>", On_comboboxPort_select)
Button_del_Port = Button_Standard(Frame_Ausgabe, 'Portfolio löschen', command=Remove_selected_Port, x=300, y=140)

Label_Entnahme = Beschriftung(Frame_Ausgabe, 'Entnahme eingeben (30 Tage Periode):', x=40, y=220)
Entry_Entnahme = tk.Entry(Frame_Ausgabe, )
Entry_Entnahme.place(x=40, y=250)
Button_PlotterAnzeigen = Button_Standard(Frame_Ausgabe, 'Plotter anzeigen', x=40, y=300)

btn_StartWindow = Button_Menu(root, 'Startseite', zeige_StartWindow, 1, 2)
btn_PersonAnlegen = Button_Menu(root, 'Person anlegen', zeige_PersonAnlegen, 120, 2)
btn_PortfolioErstellen = Button_Menu(root, 'Portfolio Erstellen', zeige_PortfolioErstellen, 290, 2)
btn_Ausgabe = Button_Menu(root, 'Ausgabe', zeige_Ausgabe, 470, 2)
Combobox_Elemente_Person = [element[0] for element in PersonListe]
ComboBox_Person['values'] = Combobox_Elemente_Person
Combobox_Elemente_Port = [element[0] for element in PortfolioListe3]
ComboBox_Port['values'] = Combobox_Elemente_Port
startGUI()

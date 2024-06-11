# -*- coding: iso-8859-1 -*-

# Importiere alles aus der tkInter-Bibliothek (Oberfläche)
from tkinter import *
# Minidom zur Interpretation der XML-Daten für die Bilddatei
from xml.dom import minidom

# Importiere gemeinsam genutzte Datentypen
from KartenTypen import *




# Gui-Klasse (vor allem für Dijkstra-Algorithmus)
# Auf den eingegebenen Startort (bzw. Zielort) kann mit <guiobjekt>.Startort.get() zugegriffen werden.
# Die Operation, die für btnExec ausgeführt wird, muss im Hauptprogramm mit <guiobjekt>.btnExec.bind(...) definiert werden.

class KartenGUI:
    def __init__(self, master, graph, Datei, Fensterbreite, Fensterhoehe):

        self.Debug=0

        self.parentControl=master
        self.g = graph
        # Bilddaten
        self.bgBild = PhotoImage(file="%s.gif" % Datei)
        # Leinwand mit Scrollbars
        self.canBild=Canvas(master, width=Fensterbreite, height=Fensterhoehe, scrollregion=(0, 0, self.bgBild.width(), self.bgBild.height()))
        self.canBild.create_image(0,0,image=self.bgBild,anchor="nw")
        self.sbary=Scrollbar()
        self.sbary.config(command=self.canBild.yview)
        self.canBild.config(yscrollcommand=self.sbary.set)

        self.sbarx=Scrollbar()
        self.sbarx.config(command=self.canBild.xview, orient=HORIZONTAL)
        self.canBild.config(xscrollcommand=self.sbarx.set)


        # Labels und Entry Widgets für die Eingabe von Start und Ziel
        self.lblStart=Label(master, text="Start:")
        self.lblStart.grid(column=0,row=0,sticky=E)
        # Stringvariable, die die Starteingabe beinhaltet
        self.Startort=StringVar()
        self.Startort.set("TRIER - VERTEILERKREIS (A 602)")
        #self.Startort.set("Trier-Verteilerkreis")
        self.entStart=Entry(master,width=25, textvariable=self.Startort)
        self.entStart.grid(column=1,row=0,sticky=W)


        self.lblZiel=Label(master, text="Ziel:")
        self.lblZiel.grid(column=2,row=0,sticky=E)
        # Stringvariable, die die Zieleingabe beinhaltet
        self.Zielort=StringVar()
        self.Zielort.set("KREUZ MÜNCHEN - WEST")
        #self.Zielort.set("Kreuz München-West")
        self.entZiel=Entry(master,width=25, textvariable=self.Zielort)
        self.entZiel.grid(column=3,row=0,sticky=W)
        

        # Button zur Ausführung eines Kommandos (Aktion im Hauptprogramm zu definieren)
        self.btnExec = Button(master,text="Route berechnen")
        self.btnExec.bind('<Button-1>', self.ausfuehren)
        self.btnExec.grid(column=4, row=0)

        self.btnClose = Button(master,text="Ende")
        self.btnClose.bind("<Button-1>", self.btnCloseClick)
        self.btnClose.grid(column=5, row=0, sticky=E)

        self.canBild.grid(columnspan=6)
        self.sbary.grid(column=6,row=1, sticky=N+S)
        self.sbarx.grid(columnspan=6,sticky=E+W)

        # Fenster darf nicht in der Größe geändert werden
        master.resizable(0,0)

        # Textdatei in XML-Struktur einlesen
        try:
            baum = minidom.parse("%s.xml" % Datei)

            L=baum.getElementsByTagName("sued")[0]
            self.cSued=float(L.getAttribute("wert"))
            L=baum.getElementsByTagName("nord")[0]
            self.cNord=float(L.getAttribute("wert"))
            L=baum.getElementsByTagName("west")[0]
            self.cWest=float(L.getAttribute("wert"))
            L=baum.getElementsByTagName("ost")[0]
            self.cOst =float(L.getAttribute("wert"))
        except Exception as e:
            print("!!!FEHLER in XML-Beschreibung:", e.message)
            cNord=cSued=cWest=cOst=0.0
            raise e

    def btnCloseClick(self, event):
        self.parentControl.destroy()
        
    # Daten in Datenbankgespeichert in Grad (keine Minuten, sondern Gradanteile)
    # Umrechnung in Bildschirmkoordinaten
    def InPixelWO(self,Grad):
      l=self.canBild.cget("scrollregion").rsplit()   # Das geht bestimmt noch einfacher!
      width=int(l[2])
    #  width=int(Canv.cget("width"))   # Funktioniert nicht mehr, da das Bild scrollt
      erg=width-round((Grad-self.cOst)* width/(self.cWest-self.cOst))
      return erg

    def InPixelNS(self,Grad):
      l=self.canBild.cget("scrollregion").rsplit()
      height=int(l[3])
      erg=height-round((Grad-self.cSued)*height/(self.cNord-self.cSued))
      return erg

    def ZeichneOrt(self, Ort):
        if self.Debug:
            print("Call ZeichneOrt", Ort.tupel())
        Groesse=2  #Ort.Einwohner//10000
        latOrt = float(self.g.getKnotenDaten(Ort, 'lat'))
        lonOrt = float(self.g.getKnotenDaten(Ort, 'lon'))
        x=self.InPixelWO(latOrt)
        y=self.InPixelNS(lonOrt)
        self.canBild.create_oval(x-Groesse,y-Groesse,x+Groesse,y+Groesse, fill = "red")
        #self.canBild.create_text(x+5,y,text=Ort.Name, fill='black', anchor="nw")


    def ZeichneWeg(self,Breite1,Laenge1,Breite2,Laenge2, Farbe="red", Dicke=1):
        if self.Debug:
            print("Call ZeichneWeg", (Breite1,Laenge1),(Breite2,Laenge2))
        x1=self.InPixelWO(Laenge1)
        x2=self.InPixelWO(Laenge2)
        y1=self.InPixelNS(Breite1)
        y2=self.InPixelNS(Breite2)
        self.canBild.create_line(x1,y1,x2,y2,fill=Farbe, width=Dicke)
 		
    def ZeichneWegListe(self,Ortsliste):
        if self.Debug:
            print("Call ZeichneWegListe", Ortsliste)
        Ort1=Ortsliste[0]
        for Ort2 in Ortsliste[1:]:
            latOrt1 = float(self.g.getKnotenDaten(Ort1, 'lat'))
            lonOrt1 = float(self.g.getKnotenDaten(Ort1, 'lon'))
            latOrt2 = float(self.g.getKnotenDaten(Ort2, 'lat'))
            lonOrt2 = float(self.g.getKnotenDaten(Ort2, 'lon'))
            self.ZeichneWeg(latOrt1,lonOrt1,latOrt2,lonOrt2)
            Ort1=Ort2

    def ausfuehren(self, event):
        print('Weg wird berechnet ...')
        startOrt = self.entStart.get()
        zielOrt = self.entZiel.get()
        ergebnis = self.g.kuerzesterWegDijkstra(startOrt, zielOrt)
        weg = ergebnis[0]
        laenge = ergebnis[1]
        for w in weg:
            ort1 = w[0]
            ort2 = w[1]
            self.ZeichneOrt(ort1)
            self.ZeichneOrt(ort2)
            self.ZeichneWegListe([ort1,ort2])
            daten = (self.g.getKantenDaten(w[0], w[1], 'A'), float(self.g.getGewichtKante(w[0], w[1])))
            print(w, daten)
        print('Weglänge:', laenge)

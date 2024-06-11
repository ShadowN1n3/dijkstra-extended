# -*- coding: iso-8859-1 -*-

# Gemeinsame Datentypen aller Elemente z.B. des Dijkstra-Algorithmus


class OrtKnoten:
    def __init__(self, ONR='MZ', Name='Mainz', Breite=50.0, Laenge=8.26, Einwohner=4711):
        self.ONR       = ONR
        self.Name      = Name
        self.Breite    = Breite
        self.Laenge    = Laenge
        self.Einwohner = Einwohner

    # Ausgabefunktion als Tupel (z.B. für print)
    def tupel(self):
        return (self.Name, self.Laenge, self.Breite, self.Einwohner)

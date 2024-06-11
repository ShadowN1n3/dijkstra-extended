from tkinter import *
from KartenGUI import *
from graph_dijkstra import *

g = GraphDijkstra()
print('Autobahndaten werden geladen ...')

f_xml = open("graph_bab.xml", "r", encoding="iso-8859-1")
xml_quelltext = f_xml.read()
g.graphmlToGraph(xml_quelltext) 

root = Tk ( )
app=KartenGUI(root, g, "Deutschland", 506, 600)

root.mainloop()

# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 10:07:27 2024

@author: miett
"""

import warnings
import sympy as sym
from sympy import *
from sympy.utilities.exceptions import SymPyDeprecationWarning
import math
from sympy.solvers import solve

warnings.filterwarnings(
    # replace "ignore" with "error" to make the warning raise an exception.
    # This useful if you want to test you aren't using deprecated code.
    "ignore",
    # message may be omitted to filter all SymPyDeprecationWarnings
    message=r"(?s).*<regex matching the warning message>",
    category=SymPyDeprecationWarning,
    module=r"<regex matching your module>"
  )

# 'Liike_12gui.ipynb' laskee 1-dim ja 2-dim liikeopin sanallisia lasku-
# tehtäviä. (Ei voimia. Myös tehtävien 'raketeissa' oletetetaan, että ne 
# ovat heitteitä ilman käynnissä olevaa rakettimoottoria)
# Tämä koodi tarvitsee  moduleiksi tiedostot Liike_1b.py ja Liike_2b.py.
# Tehtäviä löytyy 'Liike_tehtäviä'-tiedostosta
# Heikki Miettinen 1924

vi22 = 'Raketti ammutaan 70 asteen kulmassa vaakatasoon nähden \
alkunopeudella 350 m/s. Kuinka korkealle raketti lensi?' # 5520 m

import sys
import tkinter as tk 
root=tk.Tk()                   # Pohjataso

import Liike_1b as l1
import Liike_2b as l2
global txt
txt = ''
global suurelista
suurelista = ''
# Suureille Sympyn symbolit
t,tn,xt,yt,y0,ym,v0,v0x,v0y,v,vx,vy,bt0,bt = sym.symbols('t,tn,xt,yt,y0,ym, \
v0,v0x,v0y,v,vx,vy,bt0,bt')

def ratkaise():
    #global suurelista
    global txt
    txt =  teksti1.get("1.0", "end-1c")
    global q_laji
    q_laji =  l1.kumpi_dim(txt)
    #print(q_laji)
    if q_laji == 'dim1':
        vastaus = l1.AJO1(txt)        
    if q_laji == 'dim2': 
        vastaus = l2.AJO2(txt) 
    entry1.insert(5, vastaus)
    
    
def reset():
    teksti1.delete('1.0', tk.END)
    entry1.delete(0, tk.END)
    global q_laji
    q_laji = ''
    l2.quvh = {'bt0':[bt0,'na','astetta', 'Heittokulma'],
'v0':[v0,'na','m/s','Alkunopeus'],'v0x':[v0x,'na','m/s','Alkunop.x-komp.'],
'v0y':[v0y,'na','m/s','Alkunop. y-komp.'], 'y0':[y0,0,'m','Alkukorkeus'],
'ym':[ym,'na','m','Lakikorkeus'],'vx':[vx,'na','m/s','Vaakanopeus'],
't':[t,'na','s','Aika'],'tn':[tn,'na','s','Nousuaika'],
'vy':[vy,'na','m/s','Pystynopeus'],'yt':[yt,0,'m','Korkeus'],
'xt':[xt,'na','m','Kantama'], 'v':[v,'na','m/s','Loppunopeus'],
'bt':[bt,'na','astetta','Maahantulokulma']}   # Perusssanakirja vinon heittoliikkeen suureille
    l2.avail = []

# Luodaan ikkunointi (root + Framet):
root.title("LIIKEOPPILASKIN")                 
root.geometry("1050x450") 

frame=tk.Frame(root)                          # Perus-Frame pohjatason päälle
frame1=tk.Frame(root, pady= 20,  borderwidth=5)
frame1.pack()
frame2=tk.Frame(root, pady= 20,  borderwidth=5)
frame2.pack()
frame3=tk.Frame(root, borderwidth=10)       
frame3.pack()
frame4=tk.Frame(root, pady= 20, borderwidth=10)       
frame4.pack()

ohj = tk.StringVar() 
ohje = tk.Label(frame1, textvariable=ohj, justify=tk.LEFT, font=("Arial",14))
ohj.set('Ratkaisee liikeopin sanallisia tehtäviä (ei voimia). \n\
Vain yksi tehtävä kerrallaan. \nLaita kiihtyvyydelle yksiköksi m/s2.')


# syöttökenttä tehtävänannolle 'frame2'-alustaan  :
label1=tk.Label(frame2, padx= 40, text="Kirjoita tehtävä", font= ("Arial",14))                       
teksti1=tk.Text(frame2,
             padx = 10,
             width=55,
             height= 4,
             bg = "light yellow",
             font= ("Arial",14)) 


# nappula 'Ratkaise' 'frame3'-alustaan:
button1=tk.Button(frame3, text="Ratkaise",
               padx=30,
               width=10,               
               font= ("Arial",14),
               command= lambda:ratkaise())  

# nappula 'Reset' 'frame3'-alustaan:
button2=tk.Button(frame3, text="Reset",
               padx = 30,
               width=10,
               font= ("Arial",14),
               command=reset)

# tuloskenttä 'teksti2' 'frame4' alustaan luodaan 'Entry':llä:
label2=tk.Label(frame4,padx= 40, text="Tulos",  font= ("Arial",14))                      
entry1=tk.Entry(frame4, width=30, bg = "light cyan", font= ("Arial ",16)) # Vastauskenttä 

# Komponentit pakataan näkyviksi
frame.pack() 
ohje.pack()
label1.pack(side=tk.LEFT)  
teksti1.pack(side=tk.LEFT)

button1.pack(side=tk.LEFT) 
label2.pack(side=tk.LEFT)
entry1.pack(side=tk.LEFT)
button2.pack(side=tk.RIGHT)

root.mainloop()
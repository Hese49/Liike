# -*- coding: utf-8 -*-
"""
Liike_2b.py 
Created on Sat Oct  5 10:03:01 2024
# Laskee  heittoliikkeen laskuja (2-dim) (ei voimia).
# Toimii Jupyter Notebookin: Liike_12_gui.ipynb :n toisena modulina
@author: Heikki Miettinen

# OHJE: Kysy vain yhtä asiaa kerrallaan ( ei siis a),b),c) -kohtia)
# Putoamiskiihtyvyyttä ei tarvitse antaa (= 9.81 m/s2)
"""

# ALUSTUSTA  
import math
import sympy as sym

# Suureille Sympyn symbolit
t,tn,xt,yt,y0,ym,v0,v0x,v0y,v,vx,vy,bt0,bt = sym.symbols('t,tn,xt,yt,y0,ym, \
v0,v0x,v0y,v,vx,vy,bt0,bt')
# missä: tn=nousuaika, ym=nousukorkeus, bt0=heittokulma,  
# Tunnistussanat vinolle heittoliikkeelle                                                       
pro_vihe = ('kulma', 'aaka', 'suunta', 'aste')
pro_vaaka = ('vaakasuoraan','laakana','vaakasuoralla','vaakanopeus')
# Tekstissä olevan luvun suure tunnistetaan (alustavasti) sen yksiköstä:                                                      
yk_sy = {'m/s':'v0','km/h':'v0','s':'t','m/s**2':'g','m/s2':'g','m':'y0',
'cm':'y0','astetta':'bt0','asteen':'bt0'} #!!g ei ole mukana suureissa.
# Suureet vinolle heittoliikkeelle, perussanakirja, arvojen tallennus  
quvh = {'bt0':[bt0,'na','astetta', 'Heittokulma'],
'v0':[v0,'na','m/s','Alkunopeus'],'v0x':[v0x,'na','m/s','Alkunop.x-komp.'],
'v0y':[v0y,'na','m/s','Alkunop. y-komp.'], 'y0':[y0,0,'m','Alkukorkeus'],
'ym':[ym,'na','m','Lakikorkeus'],'vx':[vx,'na','m/s','Vaakanopeus'],
't':[t,'na','s','Aika'],'tn':[tn,'na','s','Nousuaika'],
'vy':[vy,'na','m/s','Pystynopeus'],'yt':[yt,0,'m','Korkeus'],
'xt':[xt,'na','m','Kantama'], 'v':[v,'na','m/s','Loppunopeus'],
'bt':[bt,'na','astetta','Maahantulokulma']} 
# Esiasetuksena on että heitto ja osuma ovat molemmat samassa 0-tasossa.
global avail      # Tähän listaan kerätään ne suureet, joille löytyy arvo..
avail = []        # suuresanakirjasta quvh. Hyödynnetään etsittäessä sopivaa
                  # ratkaisumenetelmää ('heitto1', heitto2,..).
def available():  # Poimitaan käytettävissä olevat suureet 'quvh':sta  
    for key in quvh:
        if quvh[key][1] != 'na':
            avail.append(key)        
    
def muokkaa1(txt):  
    txt = txt.casefold()                        # kaikki kirjaimet pieniksi
    txt = txt.replace(',', '.')                 # desim.pilkut pisteiksi.
    txt = txt.replace('**2', '2')               # kiihtyv.yksikkö muotoon m/s2
    txt = txt.replace('^2', '2')                #    --- " ---
    txt = txt.replace('vauhtiin', 'nopeuteen')
    txt = txt.replace('vauhti', 'nopeus')         # 'vauhti' 'nopeudeksi'
    txt = txt.replace('vauhdilla', 'nopeudella')  #    --- " ---
    txt = txt.replace('asteen', 'astetta') 
    txt = txt.replace('lentoaika', 'lenaika')     # vrt.'lentomatka'
    txt = txt.replace('yhdessä','1')              # lukusanat luvuiksi(str)
    txt = txt.replace('kahdessa','2') 
    txt = txt.replace('kolmessa','3')
    txt = txt.replace('neljässä','4')
    txt = txt.replace('viidessä','5')
    txt = txt.replace('kuudessa','6')
    txt = txt.replace('seitsemässä','7')
    txt = txt.replace('kahdeksassa','8')
    txt = txt.replace('yhdeksässä','9')
    txt = txt.replace('kymmenessä','10')
    txt = txt.replace(' yksi ',' 1 ')             # lukusanat luvuiksi(str)
    txt = txt.replace(' kaksi ',' 2 ') 
    txt = txt.replace(' kolme ',' 3 ')
    txt = txt.replace(' neljä ',' 4 ')
    txt = txt.replace(' viisi ',' 5 ')
    txt = txt.replace(' kuusi ',' 6 ')
    txt = txt.replace(' seitsemän ','7')
    txt = txt.replace(' kahdeksan ','8')
    txt = txt.replace(' yhdeksän ','9')
    txt = txt.replace(' kymmenen ','10')
    txt = txt.replace('sekunnissa','s')
    txt = txt.replace(' minuutissa',' min aikana')
    txt = txt.replace(' metriä', 'm')
    txt = txt.replace(' puoli','0.5')
    txt = txt.replace('a)','a) ')
    txt = txt.replace('b)','b) ')
    txt = txt.replace('c)','c) ')
    return txt

def onko_vinoheitto(sanat):
    for san in pro_vaaka:
        #print(san)
        if san in sanat:           # Vaakaheitot heitto4(),heitto5(),heitto6()                                       
            quvh['y0'][1] = 'na'   # Vaakaheitto tarvitsee alkukorkeuden
            quvh['v0x'][1] =  quvh['v0'][1]    # Vaakanopeus = alkunopeus
            quvh['bt0'][1] = 0                 # Heittokulma on 0 astetta
            return 'vihe_vaa'                  # Vaakaheitto
    else:
        return 'vihe' 
            
def muokkaa2(txt):
    global sanat
    sanat = []
    sanat = txt.split()              # Splittaus erillisten sanojen listaksi
    for r, sa in enumerate(sanat):
        if sa[0] == '(':             # alkusulku pois
            sanat[r] = sanat[r][1:]
        if sa[-1] == '?':            # '?'-merkki omaksi sanakseen
            sanat[r] = sanat[r][:-1] # listan r:nen sanan viimeinen merkki
            sanat.insert((r+1), '?*')
        if sa[-1] in ['.', ',']:     # sanojen perästä pisteet ja pilkut pois   
            sanat[r] = sanat[r][:-1]        
        if sa[-2:] == ':n':          # genetiivi-n  pois
            sanat[r] = sanat[r][:-2]
        if sa[-2:] == '.n':          # genetiivi-n  pois
            sanat[r] = sanat[r][:-2]
        if sa.endswith(':ssa'):      # ':ssa'-loppu  pois
            sanat[r] = sanat[r][:-4]
        if sa.endswith(':ssä'):      # ':ssä'-loppu  pois
            sanat[r] = sanat[r][:-4]
        if 'sekun' in sa:            # yksikkösanat yksikkölyhenteiksi
            sanat[r] = 's'
        if 'minu' in sa: 
            sanat[r] = 'min'
        if 'tunti' in sa  or 'tunnin' in sa: 
            sanat[r] = 'h'
        if 'kilometr' in sa: 
            sanat[r] = 'km'        
        if 'metrin' in sa: 
            sanat[r] = 'm' 
        if 'metriä' == sa: 
            sanat[r] = 'm' 
    # Irrotetaan yksikkö luvusta omaksi sanakseen
    for ind, sa in enumerate(sanat):    
        if sa[0].isnumeric(): 
            if sa[-1].isnumeric() == False or sa[-4:] == 'm/s2':    
                luku = sa                      
                yks  = sa
                i = 1
                while sa[i].isnumeric() or sa[i] == '.': 
                    i += 1                                   
                luku = sa[:i]   
                yks  = sa[i:]            
                sanat[ind] = luku  
                sanat.insert((ind+1),yks)            
    return txt, sanat  # modifioitu splittaamaton teksti, lista sanoista

# Sanan naapurisanat
def ymp(i, vas, oik):             # ('sanat'-indeksi, vasemmalle, oikealle)
    naapurit = []
    a = i-vas
    if a < 0:                     # ettei mene listan alle ulkopuolelle
        a=0        
    b = i+oik+1
    if b>len(sanat):              # ettei mene listan yli ulkopuolelle
        b=len(sanat)
    for k in range (a, b):        
        naapurit.append(sanat[k])
    naapurit.remove(sanat[i])     # sana itse ei kuulu ympäristöönsä    
    # Naapurisanoista muodostetaan myös yksi stringi 'naap':
    naap = ''
    for na in naapurit:           # katenoidaan 'naapurit'-listan sanat
        naap = naap+' '+na
    #print(naapurit)
    #print(naap)              
    return naapurit, naap         # sanan(=luvun) 'vas' sanaa vasemmalta, ja..
    #..'oik' sanaa oikealta: listana(naapurit), stringinä(naap)

def mikä_m(ind):             # Onko m alkukorkeus 'y0' vaikko lentomatka 'xt'?
    # Puuttuu nousukorkeus 'ym'!!!
    naapurit, naap = ymp(ind, 2,2)          #lukusanan ympäriltä 2+2 sanaa
    #print('TÄHÄN1') 
    #print(naapurit, naap) 
    pro_xt = ('lentää','päähän','maali','kuulaa', 'palloa', 'kiveä', 
              'keihästä', 'pesäpalloa', 'leveän')
    for sa in pro_xt:
        #print(sa) 
        if sa in naapurit:
            #print('TÄHÄN2') 
            return 'xt'
    #print('TÄHÄN3') 
    return 'y0'

def mikä_kulma(ind):                     # Alkukulma 'bt0' vai loppukulma 'bt'
    naapurit, naap = ymp(ind, 2,2)       # Lukusanan ympäriltä 2+2 sanaa
    pro_bt = ('osuu','maahan')           # Kysymys on loppukulmassta
    for sa in pro_bt:
        #print(sa) 
        if sa in naapurit:
            #print('TÄHÄN2') 
            return 'bt'
    #print('TÄHÄN3') 
    return 'bt0'

def tunnetut(sanat):    # Täyttää sanakirjaa 'quvh'
    tunnetut = []       # loc: Tunnettujen suureiden symboleille ('xt','t', v0,...)
    luvut = []          # loc: Tähän listaan poimitaan tehtävän luvut..
    units = []          # loc: .. ja tähän niitä vastaavat alkuperäisyksiköt
    pro_vaakaheit = ('vaakasuoraan','vaakasuoralla','vaakasuora','laakana',
                    'vaakanopeus')
    for sa in pro_vaakaheit:  
        if sa in sanat:
            tunnetut.append('v0y')
            luvut.append(0)
            units.append('m/s')
            quvh['bt0'][1] = 0
            
    for ind, sa in enumerate(sanat): #juostaan tehtävän sanat, ind = sanan..        
        # Normitunnetut määritetään yksikkönsä perusteella
        try:                           # 'Try..except' virhetoipumismenettely.
            luvut.append(float(sa))    # Jos luku, lisätään listaan,..
                                       #..ts. jos ei tule virheilmoitusta.           
            yksikkö = sanat[ind+1]     # Yksikkö on lukua seuraava sana.            
            units.append(yksikkö)      # Lisätään yksikkö 'units'-listaan 
            if yksikkö == 'm':         #  y0 vai xt (entä nousukorkeus!!?)   
                suure = mikä_m(ind)    # 'ind' on lukusanan indeksi
            elif yksikkö == 'astetta': # Alkukulma vai loppukulma
                suure = mikä_kulma(ind)              
            else:                      # Kun ei tarvita erityisselvittelyjä
                suure = yk_sy[yksikkö] # Yksikköä (=sanat[ind+1]) vastaava..
                                       #..suuresymboli sanakirjasta 'yk_sy'.        
            tunnetut.append(suure) # 'tunnetut'-listaan nopeus (vk,v0 tai v)         
        except ValueError: # Jos olisi kirjainsana, tulisi virheilmoitus,..
            pass       #..jolloin ohitetaan ja jatketaan seuraavaan sanaan.
    
    # Lisätään tunnetut suureet sanakirjaan 'quvh':
    for r in range(0, len(tunnetut)):
        quvh[tunnetut[r]][1] = luvut[r]        # missä tunnetut[r] on symboli..
        # ..ja [1] viittaa sanakirjan arvona olevan listan 1. paikkaan, jossa..
        # ..alunperin oli 'na'.
        quvh[tunnetut[r]][2] = units[r] # yksikkö sanakirjaan 
    if q_laji == 'vihe_vaa' and str(quvh['v0'][1])[0].isnumeric():
        quvh['v0x'][1] = quvh['v0'][1]    #Vaakaheitossa alkunopeuden vaaka-..
        quvh['v0x'][2] = quvh['v0'][2]    #komponentti on sama kuin alkunopeus.
        quvh['vx'][1] = quvh['v0'][1]     #Vaakaheitossa alkunopeuden vaaka-..
        quvh['vx'][2] = quvh['v0'][2] 
    return quvh                   # Käytetään jatkossa laskutoimituksia varten.
   
    
# KYSYTTY
# Kysytyn suureen tallennus sanakirjaan.
def kys_talteen(x):
    # quvh[x][1] = '?'
    global kys   # Kysytty suure talteen 
    kys = x
      
# Kysytyn suureen x tunnistaminen. Etsitään kysymyssana ja sen indeksi'indx'.
# Niiden perästä löytyy kysytty suure. Kysytty tallennetaan 'quvh'-
# sanakirjaan.
def kysytty(sanat, txt):
    q1 = False  # Tilamuuttuja sille, onko tuntematon suure löytynyt. 
    kysym = ['kuink', 'laske','millä','mikä','määri','ilmoi','minkä',
    'milloin','paljo','kauan','missä','mihin']
    suure_symb = {'etäällä':'xt','lentomatka':'xt','maaliennakko':'xt',
    'etäisyys':'xt','kantama':'xt','pitkä':'xt','kauas':'xt','kauaksi':'xt',
    'kantama':'xt','kohtaa':'xt','lentomatka':'xt','lakikorkeus':'ym',
    'nousukorkeus':'ym','maksimikorkeus':'ym','korkealle':'ym',
    'korkeus':'ym','korkealla':'yt','korkealle':'ym','putoaa':'yt',
    'alkunopeus':'v0','alkunopeudella':'v0','lähtönopeus':'v0',
    'nopeus':'v','nopeudella':'v','pudotuskorkeus':'y0','suunta':'bt',
    'kulmassa':'bt','ajassa':'t','pitkään':'t', 'ajanhetkellä':'t',
    'lenaika':'t', 'paikka':'xt'}
    pro_lakiyt = ('lakikorkeus', 'maksimikorkeus', 'nousukorkkeus', 
    'korkealle', 'korkeudelle')
    pro_kantama = ('kantama', 'pitkälle','kauas', 'kauaksi','lentomatka',
    'etäällä','etäälle','kauaksi')
    pro_lenaika = ('lenaika','ajassa','pitkään')
    
    
    # Etsitään kysymyssanaa, koska sen perästä löytyy etsittävä suure:
    # Spesiaalit:
    for ind, sa in enumerate(sanat):         # 'ind' ottaa sanan 'sa' indeksin.      
        if sanat[ind] in ['milloin', 'kauanko']:    # Pelkkä 'milloin' ja ..
        #..'kauanko' kysyvät aikaa';perässä ei seuraa aikaa ilmaisevaa sanaa.
            kys_talteen('t')
            q1 = True
            return             
        
    # Normitapaukset:
    # Etsitään ensin kysymyssanaa.
    for ind, sa in enumerate(sanat):# 'ind' ottaa sanan 'sa' indeksin. 
        sa_5 = sa[:5].casefold()    # sanan 'sa' 5-alku pienillä kirjaimilla.
        if sa_5 in kysym:           # Jos 5-alku löytyy kysymysten luettelosta:
            # print("Kysymyssana '{}' löytyi indeksillä {}.".format(sa_5,ind))
            indx = ind+1  # Tätä indeksiä etsittiin ts. 1.indeksi, josta..
                          #..kysytyn suuresana voi löytyä.
            sana_5 = sanat[indx][:5] # Kysymyssanaa seuraavan sanan 5-alku
            break  # 1. löydetty kysymyssana pääsee jatkoon. Jos muita on,..
                   # ne eivät (vielä) löydy.

    # Kun kysymyssana on löydetty, etsitään kysyttyä suuretta 
    # kysymyssanan indeksistä eteenpäin vertaamalla sanan 5-kirjaimista
    # alkua 'suure_symb'-sanakirjan avaimiin:     
    # 'indx' on tässä jo kysymyssanaa seuraavan sanan indeksi. 
    #print('******', len(sanat))
    while indx < len(sanat):         # Kunnes sanojen lista on käyty loppuun.    
        sana_5 = sanat[indx][:5]     #'sanat'-sanan 5-alku tunnistettavaksi        
        #print('sana_5 = ',sana_5)
        for suure in suure_symb:     # Käy läpi suureiden avaimia sanakirjasta
                                     # 'suure_symb'
            suure_5 = suure[:5]      # avaimen 5-alku
            #print('TÄHÄN1')
            if sana_5 == suure_5:    # Jos sanan alku vastaa avainalkua, niin
                x = suure_symb[suure] # x:ksi tulee löydetyn suureen
                                      # symboli sanakirjan 'suure_symb' arvosta
                            
                # Spesiaalit
                if sana_5 == 'pitkä': # oletus 's'                   
                    if sanat[indx+1][:5] == 'ajan':
                        x = 't'
                    if sanat[indx+1][:5] == 'aika': 
                        x = 't'
                    if sanat[indx+1][:5]== 'kestä':
                        x = 't'
                    if sanat[indx] == 'pitkään':
                        x = 't'
                    if sanat[indx] == 'pitkälle':
                        x = 'xt'
                if sana_5 == 'korke':                  
                    if 'pudotushetk' in sanat[indx+1]:
                        x = 'y0'                    
                    if 'korkealla' == sanat[indx]:                      
                        x = 'yt'
                    if 'korkealla' == sanat[indx] and 'käy' in sanat:                      
                        x = 'ym'   
                 
                #Kysytty ilmaisee lisäehtoja:
                if  sanat[indx] in pro_lakiyt:      # lakikorkeudessa vy  = 0
                    quvh['vy'][1] = 0
                    quvh['vy'][2] = 'm/s'
                if  sanat[indx] in pro_kantama:     # Tällöin   yt = 0
                    quvh['yt'][1] = 0               # Katso ettei lähtönolla.. 
                    quvh['yt'][2] = 'm'             #..kelpaa ratkaisuksi!!??
                if  sanat[indx] in pro_lakiyt:      # lakikorkeudessa vy  = 0
                    quvh['yt'][1] = 0
                    quvh['yt'][2] = 'm'
                if  sanat[indx] == 'paikka':
                    quvh['xt'][1] = '?'
                    quvh['xt'][2] = 'm'
                    quvh['yt'][1] = '?'
                    quvh['yt'][2] = 'm'
                q1 = True   # Tuntematon ja sen symboli on löytynyt, jolloin..
                break       # .. 'for'-solmukka voidaan lopettaa                                
            if q1 == True:  # Tällöin 'while'-silmukka  lopetetaan:
                break                         
        if q1 == True:      # Tällöin 'while'-silmukka voidaan lopettaa:
            break           # while
        indx += 1           # Indeksointi siirtyy 'sanat'-listaan seuraavaan..
                            # ..sanaan uudelle while-kierrokselle.
    if 'ajanhetkellä' in txt and 'lakikorkeudessa' in txt:
        x = 'tn'
        q1 = True
    if q1 == False:      # While on käyty loppun, kysytty suure ei selvinnyt.                  
        print("Mikä on kysytty suure? ")
    kys_talteen(x)
    return 
        
# LASKUT
# YKSIKÖT SI-järjestelmään
def SI():
    if quvh['y0'][2] == 'cm':
        quvh['y0'][2] = 'm'
        quvh['y0'][1] /= 100
    if quvh['v0'][2] == 'km/h':
        quvh['v0'][2] = 'm/s'
        quvh['v0'][1] /= 3.6
        quvh['v0'][1] = round(quvh['v0'][1],2)
    if quvh['vx'][2] == 'km/h':
        quvh['vx'][2] = 'm/s'
        quvh['vx'][1] /= 3.6 
        quvh['vx'][1] = round(quvh['vx'][1],2)
    if quvh['v0x'][2] == 'km/h':
        quvh['v0x'][2] = 'm/s'
        quvh['v0x'][1] /= 3.6 
        quvh['v0x'][1] = round(quvh['v0x'][1],2)
# Yhtälösetti heittoliikkeelle      
eq3 = sym.Eq(v0y - v0*sym.sin(bt0*0.0174533),0)        # Alkunopeuden y-kompon.
eq4 = sym.Eq(vx - v0x,0)                   # Vaakanop. = alkunopeuden x-kompon.
eq5 = sym.Eq((vy - v0y + 9.81*t) , 0)                     # Pystynopeus
eq6 = sym.Eq(xt - v0x*t,0)                                # xt = x-koordinaatti
eq7 = sym.Eq(yt - y0 - v0y*t + 4.905*t**2,0)              # yt = y-koordinaatti
eq8 = sym.Eq(bt - sym.atan2(vy, vx),0)                    # lentokulma
eq9 = sym.sympify(sym.Eq(v - sym.sqrt(vx**2 + vy**2),0))  # kok.nopeus                                     ### TEE TÄSTÄ LASKU
eq10 = sym.sympify(sym.Eq(v0y**2 - vy**2 - 19.62*yt, 0))  # Energiaperiaate..                              ### TEE TÄSTÄ LASKU

def yht5(eq5,x):         
    return  sym.solveset(eq5, x)
def yht6(eq6,x):         
    return  sym.solveset(eq6, x)
def yht7(eq7,x):         
    return  sym.solveset(eq7, x)
def yht8(eq8,x):         
    ratk = sym.solveset(eq8, x)
    return ratk 
def yht9(eq9,x):         
    return  sym.solveset(eq9, x)
def yht10(eq10,x):
    return  sym.solveset(eq10, x)

def mikä_heitto():     # Etsitään laskumenettelyjä, joihin tunnetut suureet..
                       # antavat mahdollisuuden ('heitto1', heitto2,...)
    h_ehd = {'heitto2':['t','bt0','v0','y0',], 'heitto1':['bt0','v0', 'y0'],
    'heitto3':['bt0','y0','xt'],'heitto4':['v0','xt'],
    'heitto5':['v0x','t'],'heitto6':['v0x','bt'],'heitto7': ['t']}
    
    heitot = []            # Kaikki ne heitot, joihin alkutiedot riittävät.
    for key in h_ehd:      # Juoksee ratkaisumenetelmät: 'heitto1', heitto2,..
        q = 1              # Esiastuksena kukin heitto on ON-asennossa
        for suu in h_ehd[key]: # Juoksee yhden menetelmän vaatimussuureet
            if suu in avail:  # Tämä suure on käytettävissä
                #print(suu)
                continue
            else:        # Ko. tarvittavalle suureelle ei ole arvoa, joten..
                q = 0    # menossa oleva heitto hyppää OFF -asentoon..
                break    # ja siirrytään seuraavaan heittoon (for key..)
        if q == 1:       # Kaikki tarvittavat suureet löytyvät, joten.. 
            # ko. heitto on säilyttänyt ON asentonsa ja on käytettävissä.      
            heitot.append(key) # Listaan käytettävissä olevista heitoista
    return heitot       

def alkukomponentit():
    # ['bt0', 'v0'] --> ['v0x','v0y','vx']
    # Lasketaan alkunopeuden komponentit sanakirjaan 'quvh'.
    alk_kulma = quvh['bt0'][1]               # Heittokulma
    quvh['v0x'][1] = quvh['v0'][1]*\
    math.cos(math.radians(alk_kulma))        # Alkunopeuden x-komponentti
    quvh['v0x'][1] = round(quvh['v0x'][1],2)
    quvh['v0y'][1] = quvh['v0'][1]*\
    math.sin(math.radians(alk_kulma))        # Alkunopeuden y-komponentti
    quvh['v0y'][1] = round(quvh['v0y'][1],2)
    quvh['vx'][1] = quvh['v0x'][1]           # Vaakanopeus pysyy vakiona 
    
    
def heitto1():                              # "Perusheittto" 
    global eq8
    #['bt0', 'v0', y0] -->
    # ['v0x','v0y','vx', 't', 'xt', 'ym','tn','yt','vy','v',bt]
    # Tarvitsee lähtönopeuden '0' ja heittokulman bt0 (>0)!
    # Esiastus lähtö ja paluu samassa tasossa y0=yt=0.
    # Lasketaan lentoaika, kantama, lakikorkeus, nousuaika, y-koordinaatti,
    # nopeuden y-komponentti, loppunopeus ja maahantulokulma.
    # Aluksi lasketaan alkunopeuden komponentit sanakirjaan 'quvh'.
    alkukomponentit() # saadaan talteen [v0x, v0y, vx]
    #a) Lentoaika t lasketaan yhtälöstä eq7:sta ehdolla 
    # y-koordinaatti = 'yt' = 0 (esiasetus)
    # eq7:   yt - y0 - v0y*t + 4.905*t**2 = 0
    eq7 = sym.Eq(yt - y0 - v0y*t + 4.905*t**2,0)  # y-koordinaatti 'yt'
    x = 't'                           # Ratkaistava suure
    x1 = quvh['yt'][1];  x2=quvh['y0'][1];  x3=quvh['v0y'][1]                                                         
    sijoit = [('yt',x1),('y0',x2),('v0y',x3)] 
    eq7 = eq7.subs(sijoit)                                                      
    ratk = list(yht7(eq7,x))          # Ratkaisun muoto on 'FiniteSet'..                                                     
    ratk = max(ratk)                  # 2. asteen yhtälön suurempi ratkaisu
    ratk = abs(ratk)  
    quvh['t'][1] = ratk               # Päivitetään suuresanakirja lentoajalla.
                                     
    #b) Kantama xt voidaan nyt laskea eq6:sta, kun lentoaika t tunnetaan.
    eq6 = sym.Eq(xt - v0x*t,0)        # x-koordinaatti 'xt'
    x = 'xt'                          # Ratkaistava suure
    x1=quvh['v0x'][1];  x2=quvh['t'][1]
    sijoit = [('v0x',x1),('t',x2)]
    eq6 = eq6.subs(sijoit)
    ratk = list(yht6(eq6,x))          # Ratkaisun muoto on 'FiniteSet'..
    ratk =round(ratk[0],2)            #.. siksi 'list':ksi.
    ratk = abs(ratk) 
    quvh['xt'][1] = ratk              # Päivitetään suuresanakirja lentoajalla.
   
    #c)Nousukorkeus 'yt' saadaan eq10:stä energiaperiaatteella asettamalla
    # nousukorkeudessa y-nopeus nollaksi ts. vy = 0. 
    #   eq10:    v0y**2 - vy**2 - 19.62*yt = 0  Energiaperiaate.
    eq10 = sym.sympify(sym.Eq(v0y**2 - vy**2 - 19.613*yt, 0)) 
    x = 'yt' # Ratkaistava suure
    x1=quvh['v0y'][1];  x2=0
    sijoit = [('v0y',x1),('vy',x2)]
    eq10 = eq10.subs(sijoit)
    ratk = list(yht10(eq10,x))        # Ratkaisun muoto on 'FiniteSet'..
    ratk = round(ratk[0],2)           #.. siksi 'list':ksi.
    ratk = abs(ratk) 
    quvh['ym'][1] = ratk         # Päivitetään suuresanakirja nousukorkeudella 
    
    #d) Nousuaika tn voidaan nyt laskea eq5:sta, ehdolla vy = 0.
    # eq5: vy - v0y + 9.8066*t = 0)           # Pystynopeus
    eq5 = sym.Eq((vy - v0y + 9.8066*t) , 0)   # Pystynopeus
    x = 't' # Ratkaistava suure
    x1 = 0;  x2=quvh['v0y'][1]
    sijoit = [('vy',x1),('v0y',x2)]
    eq5 = eq5.subs(sijoit)
    ratk = list(yht5(eq5,x))                 # Ratkaisun muoto on 'FiniteSet'..
    ratk =round(ratk[0],2)                   #.. siksi 'list':ksi.
    ratk = abs(ratk) 
    quvh['tn'][1] = ratk              # Päivitetään suuresanakirja lentoajalla.
    
    #e) y -koordinaatti
    eq7 = sym.Eq(yt - y0 - v0y*t + 4.905*t**2,0)   # yt = y-koordinaatti
    x = 'yt'                                       # Ratkaistava suure
    x1=quvh['v0y'][1];  x2= quvh['t'][1]; x3= quvh['y0'][1]
    sijoit = [('v0y',x1),('t',x2),('y0',x3) ]      # sijoitussetti
    eq7 = eq7.subs(sijoit)                         # sijoitus
    ratk = list(yht7(eq7,x))                 # Ratkaisun muoto on 'FiniteSet'..
    ratk = round(ratk[0],2)                  #.. siksi 'list':ksi.
    #ratk = abs(ratk) 
    quvh['yt'][1] = ratk         # Päivitetään suuresanakirja y-koordinaatilla
    
    # f) Loppunopeuden y-komponentti vy yhtälöstä eq5  
    # eq5:  vy - v0y - 9.81*t = 0 Kiihtyvän liikkeen nopeusyhtälö 'vy':lle
    eq5 = sym.Eq((vy - v0y + 9.8066*t) , 0) 
    x = 'vy'    # Ratkaistava suure
    x1=quvh['v0y'][1];  x2=quvh['t'][1]
    sijoit5 = [('v0y',x1),('t',x2)]
    eq5 = eq5.subs(sijoit5)
    ratk = list(yht5(eq5,x)) #Ratkaisun muoto on 'FiniteSet'..
    ratk = round(ratk[0],2)       #.. siksi 'list':ksi.
    quvh['vy'][1] = ratk   # Päivitetään suuresanakirja vy:n arvolla
    #print('Loppunopeuden y-komponentti on', round(ratk),'m/s')

    #g) Loppunopeus (kokonaisnopeus Pythagoraalla komponenttinopeuksista)
    # eq9:  v - sqrt(vx**2 + vy**2) = 0
    eq9 = sym.sympify(sym.Eq(v - sym.sqrt(vx**2 + vy**2),0)) # nopeus
    x = 'v'    # Ratkaistava suure
    x1=quvh['vx'][1]; x2=quvh['vy'][1] 
    sijoit9 = [('vx',x1), ('vy',x2)]  
    eq9 = eq9.subs(sijoit9)
    ratk = list(yht9(eq9, x))
    ratk = round(ratk[0],2)     
    ratk = abs(ratk) 
    quvh['v'][1] = ratk   # Päivitetään suuresanakirja loppunopeudella 'v'.

    #h) Maahantulokulma
    eq8 = sym.Eq(bt - sym.atan2(vy, vx),0)
    x = 'bt'    # Ratkaistava suure
    x1=quvh['vx'][1]; x2=quvh['vy'][1] 
    #print(x, x1, x2)                                                                     
    sij8 = [('vx',x1), ('vy',x2)]
    #print('eq8', eq8)                                                                       
    #print('sij8***', sij8)                                                                
    eq8 = eq8.subs(sij8)
    #print('eq8 sijoituksen jälkeen', eq8)                                                        
    ratk = list(yht8(eq8, x))
    ratk = round(ratk[0]*180/3.14159,2)
    quvh['bt'][1] = ratk   # Päivitetään suuresanakirja maahantulokulmalla 'bt'.
    #print('Maahantulokulma:', round(ratk),'astetta')

def heitto2(): # "Lentotila" t sekunnin kuluttua: 
    #  paikka (xt,yt),  nopeus v, suunta bt
    # ['v0','bt0','y0','t']  --> ['v0x','v0y','vx','xt','yt','v','bt']
    # x-koordinaatti:
    global eq8
    alkukomponentit()                        # --> ['v0x','v0y','vx']
    eq6 = sym.Eq(xt - v0x*t,0)               # xt = x-koordinaatti
    x = 'xt'                                 # Ratkaistava suure
    x1=quvh['v0x'][1];  x2= quvh['t'][1]     # Tunnetut otetaan sanakirjasta
    sijoit = [('v0x',x1),('t',x2)]           # sijoitussetti
    eq6 = eq6.subs(sijoit)                   # sijoitus
    ratk = list(yht6(eq6,x))                 # Ratkaisun muoto on 'FiniteSet'..
    ratk = round(ratk[0],2)                  #.. siksi 'list':ksi.
    #ratk = abs(ratk) 
    quvh['xt'][1] = ratk       # Päivitetään suuresanakirja x-koordinaatilla
    # print()
    # print('Kun lentoaika on', quvh['t'][1], 's:')
    # print('x :', round(ratk),'m')
  #y -koordinaatti
    eq7 = sym.Eq(yt - y0 - v0y*t + 4.905*t**2,0)   # yt = y-koordinaatti
    x = 'yt'                             # Ratkaistava suure
    x1=quvh['v0y'][1];  x2= quvh['t'][1]; x3= quvh['y0'][1]
    sijoit = [('v0y',x1),('t',x2),('y0',x3) ]       # sijoitussetti
    eq7 = eq7.subs(sijoit)               # sijoitus
    ratk = list(yht7(eq7,x))        #Ratkaisun muoto on 'FiniteSet'..
    ratk = round(ratk[0],2)         #.. siksi 'list':ksi.
    quvh['yt'][1] = ratk   # Päivitetään suuresanakirja y-koordinaatilla
    #print('y :', round(ratk),'m')
  #Hetkellinen lentonopeus
    #Tarvitsee ensin laskea loppunopeuden y-komponentti 'vy' yhtälöstä eq5     # d) 
    # eq5:  vy - v0y - 9.81*t = 0 Kiihtyvän liikkeen nopeusyhtälö 'vy':lle
    eq5 = sym.Eq((vy - v0y + 9.8066*t) , 0) 
    x = 'vy'    # Ratkaistava suure
    x1=quvh['v0y'][1];  x2= quvh['t'][1]
    sijoit5 = [('v0y',x1),('t',x2)]
    #print('sijoit5:', sijoit5)
    eq5 = eq5.subs(sijoit5)
    ratk = list(yht5(eq5,x))            # Ratkaisun muoto on 'FiniteSet'..
    #print('heitto2():sta', ratk)
    ratk = round(ratk[0],2)             #.. siksi 'list':ksi.
    #ratk = abs(ratk) 
    quvh['vy'][1] = ratk               # Päivitetään suuresanakirja vy:n arvolla
   #Kokonaisnopeus Pythagoraalla komponenttinopeuksista)
    # eq9:  v - sqrt(vx**2 + vy**2) = 0
    eq9 = sym.sympify(sym.Eq(v - sym.sqrt(vx**2 + vy**2),0)) # nopeus
    x = 'v'    # Ratkaistava suure
    x1=quvh['vx'][1]; x2=quvh['vy'][1] 
    sijoit9 = [('vx',x1), ('vy',x2)]  
    eq9 = eq9.subs(sijoit9)
    ratk = list(yht9(eq9, x))
    ratk = round(ratk[0],2)     
    ratk = abs(ratk) 
    quvh['v'][1] = ratk   # Päivitetään suuresanakirja loppunopeudella 'v'.
    
        
  #Suunta:  Käänteisellä tangentilla komponenttinopeuksien suhteesta.    
    # eq8:  bt - atan2(vy, vx)
    eq8 = sym.Eq(bt - sym.atan2(vy, vx),0)            # lentokulma
    x = 'bt'                                          # Ratkaistava suure
    x1=quvh['vx'][1]; x2=quvh['vy'][1] 
    sijoit8 = [('vx',x1), ('vy',x2)]  
    #print(sijoit8)
    eq8 = eq8.subs(sijoit8)
    ratk = list(yht8(eq8, x))
    ratk = round(ratk[0]*180/3.14159,2) 
    quvh['bt'][1] = ratk  # Päivitetään suuresanakirja maahantulokulmalla 'bt'.
    #print('Lentokulma:', round(ratk),'astetta')
    
def heitto3():         # "Alkunopeus=?".  Kantama, heittokulma ja y0 annettuja.
    # ['bt0','y0', 'xt'] --> ['t','v0x','v0y','v0']
    eq6 = sym.Eq(xt - v0x*t,0)                         # xt = x-koordinaatti
    eq7 = sym.Eq(yt - y0 - v0y*t + 4.905*t**2,0)       # yt = y-koordinaatti
    
    # Sijoitetaan eq6:aan annettu kantama xt, jää v0x ja t.
    # Sijoitetaan yhtälöön eq7 v0y = tan(bt0)*v0x, yt=0 ja y0
    # Saadaan yhtälöpari, jonka tuntemattomia ovat v0x ja t, josta edelleen
    # saadaan etsitty v0 = v0x/cos(bt0) 
    x1 = quvh['xt'][1]
    eq6 = eq6.subs(xt,x1)
    #print(eq6)
    bt0_r = quvh['bt0'][1]*3.14159/180
    x2 = round(sym.tan(bt0_r),4)
    x2 = x2*v0x
    x3 = quvh['y0'][1] 
    sijoit7= [(v0y,x2), (yt,0), (y0,x3)]
    eq7 = eq7.subs(sijoit7)
    #print(eq7)
    ratk = sym.nonlinsolve([eq6, eq7], [v0x,t])  
    ratk = list(ratk)
    #print(ratk)
    aika = round(ratk[1][1],3)
    quvh['t'][1] = aika                  # lentoaika tallennetaan sanakirjaan
    ratk = ratk[1][0]                    # v0x
    quvh['v0x'][1] = round(ratk,3)
    quvh['v0y'][1] = round(ratk*sym.tan(bt0_r),3)
    ratk = ratk/sym.cos(bt0_r)
    quvh['v0'][1] = round(ratk,3)
    ratk = round(ratk,1)    

def heitto4(): # "Paljonko vaakaheitto putoaa?"
    # ['v0','xt'] +  ehto v0y=0 --> ['v0x','vx','t','yt']
    # Vaakaheitto nopeus v0=v0x ja matka xt tunnettuja.
    # Kysytään  putoamista tällä matkalla. (txt_vi4)
    # y0=0 v0y=0. Lasketaan aika t = xt/v0x (eq6). Sitten yt eq7:sta. 
    quvh['v0x'][1] = quvh['v0'][1]
    quvh['vx'][1] = quvh['v0'][1]
    matka = float(quvh['xt'][1])
    nopeus = float(quvh['v0x'][1])
    aika = matka/nopeus
    quvh['t'][1] = round(aika,3)
    eq7 = sym.Eq(yt - y0 - v0y*t + 4.905*t**2,0)        # yt = y-koordinaatti 
    eq7 = eq7.subs([('y0',0), ('v0y',0), ('t', aika)])
    putous = list(sym.solveset(eq7))
    putous = round(putous[0],4)
    quvh['yt'][1] = putous
   

def heitto5(): #"Vaakanopeus + aika --> pudotuskorkeus"
    # ['v0x','t'] +  ehto v0y=0 --> ['y0']
    # sitten heitto1() antaa loput. (txt_vi6)
    eq7 = sym.Eq(yt - y0 - v0y*t + 4.905*t**2,0)          # yt = y-koordinaatti 
    eq7 = eq7.subs([('yt',0), ('t',11.2), ('v0y', 0)])
    korkeus = list(sym.solveset(eq7, y0))   #!!Vaihda tämä 'yht7()' funktiolle 
    korkeus = round(korkeus[0],2)
    quvh['y0'][1] = korkeus
   
def heitto6(): # Vaakanopeus, loppukulma --> pudotuskorkeus (txt_vi7)
    #['v0x','bt'] + ehto 'v0y'=0 -->  ['vy', 't', 'y0']
    # heitto1() antaa loput.
  #1) Lopuunopeuden y-komponentti
    kulma = quvh['bt'][1]*0.0174533      # Radiaaneina
    xnop = quvh['vx'][1]                 # Nopeuden x-komponentti lopputilassa.
    ynop =  xnop*sym.tan(kulma)          # Nopeuden y-komponentti lopputilassa.
    ynop = round(ynop,2)
    quvh['vy'][1] = ynop
  #2) Putoamisaika kiihtyvän liikkeen nopeusyhtälöstä eq5.   
    eq5 = sym.Eq((vy - v0y + 9.8066*t) , 0) 
    x = 't'    # Ratkaistava suure
    x1= ynop; x2=quvh['v0y'][1]
    sijoit5 = [('vy',x1),('v0y',x2)]
    eq5 = eq5.subs(sijoit5)
    ratk = list(yht5(eq5,x))         #funktio Ratkaisun muoto on 'FiniteSet'..
    ratk = round(ratk[0],2)          #.. siksi 'list':ksi.
    ratk = abs(ratk)
    quvh['t'][1] = ratk              # Päivitetään suuresanakirja t:n arvolla
  #3) Alkukorkeus y0 eq7:sta  
    eq7 = sym.Eq(yt - y0 - v0y*t + 4.905*t**2, 0)
    x = 'y0'
    x1 = 0; x2 = quvh['v0y'][1]; x3 = quvh['t'][1]
    sijoit7 =[('yt',x1),('v0y',x2),('t',x3)]
    eq7 = eq7.subs(sijoit7)
    #print(eq7)
    ratk = list(yht7(eq7, x))[0]
    quvh['y0'][1] = round(ratk, 2)
    
def heitto7(): #lentoaika t --> alkupystynopeus v0y ja maksimikorkeus ym.
    # ['t']  --> ['v0y',ym]
  # Alkunopeus  
    # eq5: vy - v0y + 9.8066*t = 0                       # Pystynopeus
    eq5 = sym.Eq((vy - v0y + 9.8066*t) , 0)              # Pystynopeus
    x = 'v0y' # Ratkaistava suure
    x1 = 0;  x2=quvh['t'][1]/2                           # Lentoajan puolikas
    sijoit = [('vy',x1),('t',x2)]
    eq5 = eq5.subs(sijoit)
    ratk = list(yht5(eq5,x))       # Ratkaisun muoto 'FiniteSet' 'list':ksi.
    ratk =round(ratk[0],2)   
    #ratk = abs(ratk) 
    quvh['v0y'][1] = ratk          # Päivitetään suuresanakirja alkunopeudella.
  # Nousukorkeus
    # Nousukorkeus 'yt' saadaan eq10:stä energiaperiaatteella asettamalla
    # nousukorkeudessa y-nopeus nollaksi ts. vy = 0. 
    # eq10:    v0y**2 - vy**2 - 19.62*yt = 0  Energiaperiaate.
    eq10 = sym.sympify(sym.Eq(v0y**2 - vy**2 - 19.613*yt, 0)) 
    x = 'yt' # Ratkaistava suure
    x1=quvh['v0y'][1];  x2=0
    sijoit = [('v0y',x1),('vy',x2)]
    eq10 = eq10.subs(sijoit)
    ratk = list(yht10(eq10,x))    # Ratkaisun muoto 'FiniteSet''list':ksi.
    ratk = round(ratk[0],2)      
    ratk = abs(ratk) 
    quvh['ym'][1] = ratk          # Päivitetään suuresanakirja nousukorkeudella
      
def laskut():
    heitot = mikä_heitto()
    if 'heitto2' in heitot and kys in ['v0x','v0y','vx','xt','yt','v','bt']:
        heitto2()
        ###he2 = True  # Tulostusta varten
    elif  'heitto1'  in heitot and kys in ['v0x','v0y','vx', 't', 'xt', 
                                     'ym','tn','yt','vy','v','bt']:
        heitto1()
    elif 'heitto3' in heitot and kys in ['t','v0x','v0y','v0']:
        heitto3()
    elif 'heitto4' in heitot and kys in ['v0x','vx','t','yt']:
        heitto4()
    elif 'heitto5' in heitot and kys in ['y0']:
        heitto5()
    elif 'heitto6' in heitot and kys in ['vy', 't', 'y0']:
        heitto6()
    elif 'heitto7' in heitot and kys in ['v0y','ym']:
        heitto7()
    elif 'heitto5' in heitot:
        heitto5()
        heitto1()
    elif 'heitto3' in heitot:
        heitto3()
        heitto1()
    else:
        print('Laskumenetelmää ei löytynyt!')

def sigfiground(number:float, ndigits=3)->float:     
    return float(f"{number:.{ndigits}g}")
# Näissä pyöristyksissä on päällekkäisyyttä, mutta toimii.
def pyöristys(luku): 
    if luku == 0:
        print('VIRHE')
    luku = sigfiground(luku)
    merkits_num = 3                  # Pyöristys kolmeen merkitsevään numeroon
    luku =  round(luku, merkits_num - \
    int(math.floor(math.log10(abs(luku)))) - 1)
    luku = str(luku)
    if luku[-2:] == '.0' and len(luku) > 4:
        luku = luku[:-2]             # Jättää ylimääräisen .0 :n pois
    return luku
    
def tulostus(vast):                                                   
    if vast != 'na':
        global koords                              # Onko Koordinaattitulostus
        if koords == True:                         # Koordinaattitulostus
            # Pyöristykset kolmeen merkitsevään numeroon
            vasx = pyöristys(quvh['xt'][1])
            vasy = pyöristys(quvh['yt'][1])
            vastaus1 = f" x-koord. = {vasx} m, y-koord. = {vasy} m"
            #print(vastaus1)
            return vastaus1
        else:
            # Pyöristys kolmeen merkitsevään numeroon
            vast = pyöristys(vast)
            vastaus2 = f" {quvh[kys][3]}  on {vast} {quvh[kys][2]}"
            return vastaus2
    else:
        # print('Ei riittävästi tietoa!')
        return('Ei riittävästi tietoa!')                          
        
def AJO2(txt):
    txt = muokkaa1(txt)
    global q_laji
    q_laji = onko_vinoheitto(txt)
    txt, sanat = muokkaa2(txt)
    tunnetut(sanat) 
    kysytty(sanat, txt)
    #print_suureet()                                  ##### TESTAUKSEEN
    #sanakirja()          # Tulostaa sanakirjan       ##### TESTAUKSEEN                        
    SI()
    global koords                            # Koordinaatttitulostuksen lippu
    koords = False                           # Normitulostus
    #print(quvh['yt'][1], quvh['yt'][1])
    if quvh['yt'][1]== '?' and  quvh['yt'][1]=='?':   # kysytään (x,y)
        koords = True                        # Koordinaattitulostus
    available()
    laskut()    
    vast = quvh[kys][1]            # Tulostettava vastaus otetaan sanakirjasta.
    vastaus = tulostus(vast) 
    print(vastaus)
    return vastaus


if __name__ == "__main__":         # Kun käytetään itsenäisenä ohjelmana
    
    vi19 = 'Kiväärin luoti ammutaan alkunopeudella 750 m/sekunnissa. \
Lähtösuunta muodostaa 30 asteen kulman vaakatason kanssa. Määritä \
luodin paikka 4 s kuluttua  lukien.' #   x: 2600 m     y: 1420 m
    vi20 = 'Yleisurheilun GP -kisojen miesten kuulan voittotyönnössä \
   kuula lähti 180 cm korkeudelta 45 asteen kulmassa lähtönopeudella \
   14.10 m/s. Kuinka pitkälle työntö kantoi?'  # 21,9 m
    vi29 = 'Eräs EM-kisojen kilpailija työnsi harjoituksissa kuulaa 18,0 m. \
Kuulan lähtökulma oli 45 astetta ja lähtökorkeus maanpinnasta 2,0 m. \
Millä nopeudella kuula osui maahan?' #14.1 m/s 

# Yksittäinen testiajo tällä modulilla itsenäisenä ohjelmana
    AJO2(vi19)                                                        

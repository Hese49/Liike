# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 10:19:33 2024

@author: Heikki Miettinen  
"""
# Ohjelma laskee 1-dim liikeopin laskuja (ei voimia) sanallisesti annetuista tehtävistä.
# Esim. 'Auto ajoi nopeudella 85km/h  5 h ajan. Kuinka pitkälle päästiin?'
# Tämä tiedosto tarvitaan graafisen käyttöliittymän Jupyter Notebook Liike_12_gui.ipbynb':n moduliksi,
# (modulin 'Liike_2b.py' ohella) mutta toimii myös itsenäisenä Pyhthon ohjelmana  (if __name__ == "__main__":).
 
# KIRJOITA TEHTÄVÄ KOODIN LOPPUUN 
# ITSENÄINEN AJO  koodin lopussa AJO1(txt), AJO1(t18), ... )

import math
import sympy as sym
from sympy import *
from sympy.solvers import solve

# -------------------------------------------------------------------------------------

# ALUSTUSTA
# Suureille Sympyn symbolit
t,a,s,vk,v,v0, z = sym.symbols('t,a,s,vk,v,v0, z')
suur_list = [t,a,s,vk,v,v0]
global quantities
quantities = {'t':[t,'na','na','aika'], 'a':[a,'na','na','kiihtyvyys'],
         's':[s,'na','na','matka'],  'vk':[vk,'na','na','keskinopeus'],
        'v0':[v0,'na','na','alkunopeus'], 'v':[v,'na','na','loppunopeus']}

def kumpi_dim(txt):
    pro_1dim_1 = ('auto','Auto','pyörä','juna','Juna','atkustaja',
    'keskivauh','keskinop','kävelynopeus','lentonopeus','putoava',
    'pudotetaan','tippuu','ajaa','hidastuvuus','kiihtyvyy','kiihdytt',
    'ylöspäin','äänen', 'km:n','liukupor','uimahypp','pystysuoraan',
    'jyrkänteeltä')
    pro_2dim = ('ammus','luoti','kuula','keihäs','pommi','kivi',
            'kiven','kantama','kulma','suuntaan','vaaka','laaka', 
            'aste','lyödään','heitt','heitetään','pallo')     
    pro_1dim_2 = ('putoaa')
    for pro in pro_1dim_1:   # Pro juoksee tunnistussanoja ('auto', pyörä',..)
        if pro in txt:       # Jos dim1-tunnistussana on tehtävätekstissä..
            return 'dim1'
    for pro in pro_2dim:     # Pro juoksee tunnistussanoja ('ammus', luoti',..)
        if pro in txt:       # Jos dim1-tunnistussana on tehtävätekstissä..
            return 'dim2'
    for pro in pro_1dim_2:   # Pro juoksee tunnistussanoja ('auto', pyörä',..)
        if pro in txt:       # Jos dim1-tunnistussana on tehtävätekstissä..
            return 'dim1'             
    print ('Ei selvinnyt, onko 1dim vai 2dim !??')       
                                  
# TEKSTI --> SANAT
def muokkaa_teksti(txt):    
    txt = txt.casefold()                        # kaikki kirjaimet pieniksi
    txt = txt.replace("'", '')                  
    txt = txt.replace(',', '.')                 # desim.pilkut pisteiksi.
    txt = txt.replace('**2', '2')               # kiihtyv.yksikkö muotoon m/s2
    txt = txt.replace('^2', '2')                #    --- " ---
    txt = txt.replace('vauhtiin', 'nopeuteen')
    txt = txt.replace('vauhti', 'nopeus')       # 'vauhti' 'nopeudeksi'
    txt = txt.replace('vauhdilla', 'nopeudella')  #    --- " ---
    txt = txt.replace('yhdessä','1')            # lukusanat luvuiksi(str)
    txt = txt.replace('kahdessa','2') 
    txt = txt.replace('kolmessa','3')
    txt = txt.replace('neljässä','4')
    txt = txt.replace('viidessä','5')
    txt = txt.replace('kuudessa','6')
    txt = txt.replace('seitsemässä','7')
    txt = txt.replace('kahdeksassa','8')
    txt = txt.replace('yhdeksässä','9')
    txt = txt.replace('kymmenessä','10')
    txt = txt.replace(' yksi ',' 1 ')           # lukusanat luvuiksi(str)
    txt = txt.replace(' kaksi ',' 2 ') 
    txt = txt.replace(' kolme ',' 3 ')
    txt = txt.replace(' neljä ',' 4 ')
    txt = txt.replace(' viisi ',' 5 ')
    txt = txt.replace(' kuusi ',' 6 ')
    txt = txt.replace(' yhden ',' 1 ')          # lukusanat luvuiksi(str)
    txt = txt.replace(' kahden ',' 2 ') 
    txt = txt.replace(' kolmen ',' 3 ')
    txt = txt.replace(' neljän ',' 4 ')
    txt = txt.replace(' viiden ',' 5 ')
    txt = txt.replace(' kuuden ',' 6 ')
    txt = txt.replace(' seitsemän ','7')
    txt = txt.replace(' kahdeksan ','8')
    txt = txt.replace(' yhdeksän ','9')
    txt = txt.replace(' kymmenen ','10')
    txt = txt.replace(' sekunnissa',' s aikana')
    txt = txt.replace(' minuutissa',' min aikana')
    txt = txt.replace(' tunnissa',' h aikana')
    txt = txt.replace(' vuorokaudessa',' 24 h aikana')
    txt = txt.replace(' metriä', 'm')
    txt = txt.replace('puoli','0.5')
    txt = txt.replace(' kilometrin',' km')
    txt = txt.replace(' ?','?')
    txt = txt.replace(' .','.')
    sanat = txt.split()              # Splittaus erillisten sanojen listaksi
    for r, sa in enumerate(sanat):
        if sa[0] == '(':
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
        #print('r93_sa[0]:',sa[0])
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
        #Auto kulki tunnissa/minuutissa
        if sa == 'h' and sanat[ind-1][-1].isnumeric() == False:            
            sanat[ind] = '1'
            sanat.insert(ind+1, 'h') 
        if sa == 'min' and sanat[ind-1][-1].isnumeric() == False:            
            sanat[ind] = '1'
            sanat.insert(ind+1, 'min') 
        if sa == 'km' and sanat[ind-1][-1].isnumeric() == False:            
            sanat[ind] = '1'
            sanat.insert(ind+1, 'km')
        if sa == 'numeron':
            del sanat[ind-2:ind+2]
    return txt, sanat       # modifioitu splittaamaton teksti, lista sanoista


# MIKÄ LIIKELAJI
def liikelaji(txt): 
    # (txt = muokattu splittaamaton stringi 'muokkaa_teksti'-funktiolta)
    #Tasainen vai kiihtyvä liike muuttujaan 'q_laji' = 'tas'/'kii'.
    # kiihtyvä tunnistetaan. Jos ei ole kiihtyvä, niin on tasainen. 
    q_laji = 'tas'  # oletusarvo tasainen liike
    pro_kii =['jarru', 'kiih', 'hidast', 'jarru', 'pysä', 'nopeuteen',
              'putoa', 'ylös', 'levosta', 'alkunop','lähtönop', 'loppunop',
              'nopeudesta','nopeuteen', 'nopeuden', 'maahan' ,
              'liikkeelle', 'heit', 'saavuttaa','arvosta', 'kasvaa',
              'pienenee','m/s2', 'hyppää'] 
    for sa in pro_kii:    # Löytyykö tekstistä kiihtyvyyttä indikoivia sanoja
        if sa in txt:
            q_laji = 'kii'
            break
    return q_laji      # 'tas'/'kii'

# NAAPURISANAT
# Luo listan sanan naapurisanoista listana ja yhtenä stringinä
def ymp(i, vas, oik): #('sanat'-indeksi luvulle, vasemmalle, oikealle)
    naapurit = []     
    a = i-vas
    if a < 0:                         # ettei mene listan alle ulkopuolelle
        a=0        
    b = i+oik+1
    if b>len(sanat):                  # ettei mene listan yli ulkopuolelle
        b=len(sanat)
    for k in range (a, b):        
        naapurit.append(sanat[k])
    naapurit.remove(sanat[i])         # sana (luku) itse ei kuulu ympäristöönsä    
    # Naapurisanoista yksi stringi 'naap':
    naap = ''
    for na in naapurit:               # katenoidaan 'naapurit'-listan sanat
        naap = naap+' '+na            
    return naapurit, naap             #sanan(=luvun) kaksi sanaa vasemmalta,..
                                      # .. listana , stringinä

# KUMPI_NOP
# Selvittää onko kiihtyvän liikkeen nopeusluku v0 vai v.
def kumpi_nop(tunnetut, sanat, ind):
    naapurit, naap = ymp(ind,2,0)     # Kutsuu 'ymp'-funktiota antamaan lukua..
                                      #..edeltävät 2 sanaa listana ja stringinä.
    if 'v0' in tunnetut:              # Alkunopeus on jo aiemmin todettu           
        return 'v'                    # Loppunopeus on jo aiemmin todettu
    if 'v' in tunnetut:
        return 'v0'
    if 'alku' in naap:       
        return 'v0'
    if 'nopeudesta' in naap:
        return 'v0'
    if 'nopeudella' in naap:
        return 'v0'
    if 'nopeus on'  in naap:
        return 'v0'
    if 'nopeuteen' in naap:       
        return 'v'
    if 'nopeuden' in naap:       
        return 'v' 
    return 'Ei selvinnyt!?'

# TUNNETUT
# Poimitaan 'sanat'-listasta luvut ja yksiköt ja päätellään suuresymboli.
# Kirjataan suureet, luvut ja yksiköt 'qantities'-sanakirjaan.
def tunnetut(sanat, q_laji):
    tunnetut = []    # Tunnettujen suureiden 'symboleille'
    luvut = []       # Tähän listaan poimitaan tehtävän luvut..
    units = []       # .. ja tähän niitä vastaavat yksiköt
    # Sanakirja  'yksikkö':'suure'. 
    yk_sy = {'km/h':'vk','km/s':'vk', 'm/s':'vk', 's':'t', 'h':'t',
             'min':'t','tunnin':'t' ,'tuntia':'t', 'm/s^2':'a',
             'm/s**2':'a', 'm/s2':'a', 'm':'s', 'km':'s', 'cm':'s'}
    # Seuraavat sanat ilmaisevat v0:n 0:ksi:
    pro_v0_0 = ['levosta','paikaltaan','putoaa','putoava', 'putoamiseen',
          'putosi', 'nollasta','putoavalta','liikkeellelähdön','ammuksen',
       'putoaminen', 'piipussa','lähdöstä','liikkeellelähdöstä','hyppää']
    # Seuraavat sanat ilmaisevat v:n 0:ksi:
    pro_v_0 = ['pysähdyksiin','pysähtyi','pysäyttäminen','nousi',
               'korkeuteen','korkeus']
    # Seuraavat sanat ilmaisevat putoamiskiihtyvyyden:
    pro_a_g = ['putoaa', 'putoava', 'putosi', 'pudotettiin','putoavalta',
      'ylöspäin','tippui', 'nousi','korkeuteen', 'heitettiin','heitetty',
     'heitetään','heitetyn','putoaminen', 'hyppää', 'putoamiseen']
    # Etsitään tehtävän luvut -> yksikkö -> suure
    for ind, sa in enumerate(sanat): #'ind' ottaa sanan 'sa' listaindeksin.
        if q_laji == 'kii':        # Kiihtyvässä liikkeessä levosta lähteville
            if sa in pro_v0_0:
                tunnetut.append('v0')
                luvut.append(0)
                units.append('m/s')                
        if q_laji == 'kii':        # Kiihtyvässä liikkeessä pysähtyville
            if sa in pro_v_0:
                tunnetut.append('v')
                luvut.append(0)
                units.append('m/s')  
        if q_laji == 'kii':        # Maan vetovoiman kiihtyvyys
            if sa in pro_a_g:
                tunnetut.append('a')
                luvut.append(-9.81)
                units.append('m/s2')     
        # Jos sana on luku: laita listaan, katso yksikkö, päättele suure.
        try:                         # 'Try..except' on virhetoipumismenettely.
            luvut.append(float(sa))  # Lisätään 'luvut'-listaan, jos on..
                                     # luku ts. jos ei tulisi virheilmoitusta.
            yksikkö = sanat[ind+1]   # Yksikkö on lukua seuraava sana.      
            units.append(yksikkö)    # Lisätään yksikkö 'units'-listaan                                 
       
            suure = yk_sy[yksikkö]   # Yksikköä (=sanat[ind+1]) vastaava..
                                     #..suuresymboli sanakirjasta 'yk_sy'.        
        # Jos suuren symboli on vk, oletussuure tasaisen liikkeen..
        # nopeudelle, niin oletus vk on OK, mikäli liikelaji q_laji = 'tas'.
        # Mutta jos liikelaji q_laji = 'kii', luvulle kuuluva suure onkin..
        # .. joko v0 tai v. Tämän selvittää funktio 'kumpi_nop(sanat, ind)',..
        # missä ind on luvun indeksi 'sanat'-listassa.
        # Apufunktiona toimii luvun naapurisanat poimiva 'ymp(i, vas, oik)'-
        # funktio, missä i on luvun indeksi ind. Siis:        
            if suure == 'vk' and q_laji == 'kii' : 
                # nopeus ja kiihtyvä liike
                suure = kumpi_nop(tunnetut, sanat, ind) # ind on luvun indeksi          
            tunnetut.append(suure) # 'tunnetut'-listaan nopeus (vk,v0 tai v)         
        except ValueError: # Jos olisi kirjainsana, tulisi virheilmoitus,..
            pass       #..jolloin ohitetaan ja jatketaan seuraavaan sanaan.
    # Laitetaan tunnettuja suureita vastaavat luvut 'quantities'-sanakirjaan
    for r in range(0, len(tunnetut)): 
        quantities[tunnetut[r]][1] = luvut[r] # missä tunnetut[r] on symboli..
        # ..ja [1] viittaa sanakirjan arvona olevan listan 1. paikkaan, jossa..
        # ..alunperin oli 'na'.
        quantities[tunnetut[r]][2] = units[r] # yksikkö sanakirjaan
    return quantities # Käytetään jatkossa laskutoimituksia varten.

def kys_talteen1(x):
    # quvh[x][1] = '?'
    global kys1   # Kysytty suure talteen 
    kys1 = x
    
# KYSYTTY
# Kysytyn suureen tunnistaminen. Etsitään kysymyssana ja sen indeksi'indx'.
# Niiden perästä löytyy kysytty suure.
def kysytty(sanat, q_laji):
    kysym = ['kuink',  'laske', 'millä', 'mikä', 'määri', 'ilmoi', 'minkä',
         'milloin','paljo', 'kauan', 'missä', 'mihin'] 
    # Etsitään kysymyssanaa, koska sen perästä löytyy etsittävä suure:
    for ind, sa in enumerate(sanat): # 'ind' ottaa sanan 'sa' indeksin.      
        if sanat[ind] in ['milloin', 'kauanko']: # Pelkkä 'milloin' ja ..
                                  #..'kauanko' kysyvät aikaa';perässä ei  ..
                                  #..seuraa aikaa ilmaisevaa sanaa.
            kys1 = 't'            # globaaliin muuttujaan 'kys1'
            return('t')                 
        sa_5 = sa[:5].casefold()  # sanan 'sa' 5-alku pienillä kirjaimilla.                                           
        if sa_5 in kysym:         # Jos 5-alku löytyy kysymysten luettelosta:
            indx = ind+1          # Tätä indeksiä etsittiin
            sana_5 = sanat[indx][:5] # Kysymyssanaa seuraavan sanan 5-alku
            break   #1.** löydetty kysymyssana pääsee jatkoon. Jos muita on,..
                    # ne eivät (vielä) löydy.

                
    # Kun kysymyssana on löydetty, etsitään kysyttyä suuretta 
    # kysymyssanan indeksistä eteenpäin vertaamalla sanan 5-kirjaimista
    # alkua 'suure_symb'-sanakirjan avaimiin:
    suure_symb = {'matka':'s', 'korkeus':'s','korkealle':'s',
    'kaukana':'s', 'kauas':'s','paikka':'s', 'pitkälle':'s', 'pituus':'s',
    'syvyys':'s', 'etäälle':'s','missä':'s','aika':'t','aikaa':'t',
    'ajan':'t','ajassa':'t', 's':'t', 'min':'t', 'h':'t','hetkellä':'t',
    'kestää':'t', 'kauan':'t','nousuaika':'t','kiihtyvyys':'a','hidastuvuus':'a',
    'keskinopeus':'vk','nopeus':'v','loppunopeus':'v','putoamisnopeus':'v',
    'alkunopeus':'v0', 'lähtönopeus':'v0'}
    q1 = False      # Tilamuuttuja sille, onko tuntematon suure löytynyt. 
                    # 'indx' on tässä jo kysymyssanaa seuraavan sanan indeksi.
  
    while indx < len(sanat):           # Kunnes sanojen lista on käyty loppuun.    
        sana_5 = sanat[indx][:5]       #'sanat'-sanan 5-alku tunnistettavaksi        
        for suure in suure_symb:       # Käy läpi suureiden avaimia sanakirjasta.
            suure_5 = suure[:5]        # avaimen 5-alku
            if sana_5 == suure_5:      # Jos sanan alku vastaa  avainta, niin:
                x = suure_symb[suure]  # x:ksi tulee löydetyn suureen
                if sana_5 == 'pitkä':  # oletus 's'
                    if sanat[indx+1][:5] == 'ajan':
                        x = 't'
                    if sanat[indx+1][:5] == 'aika': 
                        x = 't'
                    if sanat[indx+1][:5]== 'kestä':
                        x = 't'
                if sana_5 == 'keski':
                    if sanat[indx][5:10] == 'kiiht': 
                        x = 'a'              
                kys_talteen1(x)   # globaaliin muuttujaan 'kys1'
                q1 = True    # Tuntematon ja sen symboli on löytynyt, jolloin..
                break        # .. 'for'-solmukka voidaan lopettaa        
            elif sana_5 == 'nopeu':    # Kysymyssanan perässä on ..
                                       #..nopeus/nopeudella.
            # Onko v vai vk? Pyritään löytämään kaikki kiihtyvän liikkeen..
            # ..tehtävät ja oletetaan loput tasaisen liikkeen tapauksiksi.            
                if q_laji == 'kii':    # 'nopeu' ja kiihtyvä liike
                    x = 'v'
                    q1 = True          # Kysytty suure on löytynyt
                else:  # Jos ei ole kiihtyvää, niin on tasaista
                    x = 'vk'
                    q1 = True
            if q1 == True:   # Tällöin 'while'-silmukka  lopetetaan:
                break        # for-                           
        if q1 == True:       # Tällöin 'while'-silmukka voidaan lopettaa:
            break            # while
        indx += 1            # Indeksointi siirtyy 'sanat'-listaan seuraavaan..
                             # ..sanaan uudelle while-kierrokselle.
    if q1 == False:        # While on käyty loppun, kysytty suure ei selvinnyt.                  
        print("Mikä on kysytty suure?  : (t,a,s,vk,v0,v): ")
    kys_talteen1(x)                            # globaaliin muuttujaan 'kys1'
    return x
 
def special(sanat, kys1):
    if (('palaa' in sanat) or ('palasi' in sanat)) and (kys1 == 't'):          
        quantities['v'][1] = -quantities['v0'][1]     # Alku-ja loppunopeus..
        quantities['v'][2] = quantities['v0'][2]       # ovat vastakkaiset.
    # Jos kysytään nousuaikaa, niin ehtona v=0:
    if kys1 == 't' and 'nousuaika' in sanat:
        quantities['v'][1] = 0
    # Jos kysytään 'kuinka korkealle', niin ehtona v=0:
    if kys1 == 's' and 'korkealle' in sanat:
        quantities['v'][1] = 0
     # Jos ylös+alas -aika on annettu ja alkunopeutta v0 kysytään, niin..
    if (('palaa' in sanat) or ('palasi' in sanat)or ('iskeytyi' in sanat))      and (kys1 == 'v0'):   
        quantities['v'][1] = 'x'
    if (('palaa' in sanat) or ('palasi' in sanat)or ('iskeytyi' in sanat))      and (kys1 == 'v'):   
        quantities['v0'][1] = 0 
    
#YKSIKÖT SI-järjestelmään
def SI(quantities):
    if quantities['t'][2] == 'h':
        quantities['t'][2] = 's'
        quantities['t'][1] *= 3600
    if quantities['t'][2] == 'min':
        quantities['t'][2] = 's'
        quantities['t'][1] *= 60
    if quantities['s'][2] == 'km':
        quantities['s'][2] = 'm'
        quantities['s'][1] *= 1000    
    if quantities['vk'][2] == 'km/h':
        quantities['vk'][2] = 'm/s'
        quantities['vk'][1] /= 3.6 
    if quantities['v0'][2] == 'km/h':
        quantities['v0'][2] = 'm/s'
        quantities['v0'][1] /= 3.6 
    if quantities['v'][2] == 'km/h':
        quantities['v'][2] = 'm/s'
        quantities['v'][1] /= 3.6
    if quantities['v'][2] == 'km/s':
        quantities['v'][2] = 'm/s'
        quantities['v'][1] *= 1000 
    return quantities

# Eri tilanteita varten eri ratkaisemisfunktiot:
def solve_1(eq1,x):
    return sym.solveset(eq1, x)      # SymPyn 'solveset' ratkaisee   
def solve_2(eq2,x):
    return sym.solveset(eq2, x)   
def solve_3(eq3,x):
    return sym.solveset(eq3, x)
#Kiihtyvän Liikkeellä on epälineaarinen yhtälöpari, koska on t**2

    # Tasaisen liikkeen laskut
def ratkaise1_tas(x):
    kys1 = x
    eq1 = sym.Eq(s - t*vk,0)
    sijoitukset = [] #Tunnetut tähän ja sitten sijoitukset yhtälöihin.
    for key in quantities:
    # Onko arvona kokonaisluku tai float, siis onko luku:
        if type(quantities[key][1]) == int or type(quantities[key][1]) == float:
            sijoitukset.append((quantities[key][0],quantities[key][1] ))  
    eq1 = eq1.subs(sijoitukset)
    ratk = list(solve_1(eq1,x))      # Kutsutaan ratkaisufunktiota. Ratkaisun..
    ratk = round(ratk[0],1)          #..muoto on 'FiniteSet', siksi 'list':ksi.
    vastaus = tulosta(ratk, kys1)    # Käy muokkaamassa ratkaisun vastaukseksi
    return vastaus                   # --> AJO1

def ratkaise1_kii(x):                                    
    eq2 = sym.Eq(a*t - v + v0 , 0)
    eq3 = sym.Eq(0.5*a*t**2 -s + t*v0 , 0)
    sijoitukset = []          #Tunnetut tähän ja sitten sijoitukset yhtälöihin.                                     
    for key in quantities:    # Poimitaan tunnettut pareiksi kuten (a, 12.5)..
                              #..listaan 'sijoitukset'
        if type(quantities[key][1]) == int or type(quantities[key][1]) == float:
            sijoitukset.append((quantities[key][0],quantities[key][1] ))
        if quantities[key][1] == 'x':
            sijoitukset.append((quantities[key][0],-v0 ))
        if quantities[key][1] == 'zz':
            sijoitukset.append((quantities[key][0],-v ))
                                             
    if quantities['s'][1] == 'na':   # Jos matka 'not available',riittää 'eq2'.
        eq2 = eq2.subs(sijoitukset)
        ratk = list(solve_2(eq2,x))  # Ratkaisu kaavalla eq2: v=v0+at. ..
        #..Muutetaan FiniteSet-tulosmuoto listaksi..
        ratk = ratk[0]
        if x == 't':
            ratk = str(ratk)  # string
            if ratk[-2:] == '*I':                    
                ratk = ratk[:-2]
            ratk = float(ratk)
        ratk = round(ratk,1)      
        vastaus = tulosta(ratk, kys1)
           
    else:  # Jos matka on mukana joko tunnettuna tai kysyttynä:      
        count = 0  # Lasketaan montako viidestä on tunnettuja + '?'):
        for key in ['t','a','s','v0','v']: # tas.liikkeen 'vk' jätetty pois 
            if quantities[key][1] != 'na':
                count +=1                                        
        if count == 5:       # Jos mukana on kaikki kiihtyvän liikkeen viisi..
                             #..suuretta, riittää yhtälö 'eq3':
            eq3 = eq3.subs(sijoitukset)
            ratk = list(solve_3(eq3,x))
            ratk = round(ratk[0],1) 
            if x == 't':
                ratk = abs(ratk)
            vastaus = tulosta(ratk)
                            
        elif count == 4 and quantities['v'][1] == 'na':             
            eq3 = eq3.subs(sijoitukset)
            ratk = list(solve_3(eq3,x))
            ratk = ratk[0]
            #print(ratk)         
            if x == 't':                       # Kysytään t:tä
                ratk = str(ratk)
                if ratk[-2:] == '*I':                    
                    ratk = ratk[:-2]
                ratk = float(ratk)
            ratk = abs(ratk)
            ratk = round(ratk,1)     
            vastaus = tulosta(ratk, kys1)
                
        elif count == 4: # Jos mukana on vain neljä ja t:tä ei kysytä, tarvitaan 'eq2' ja 'eq3'.                                      
            # Etsitään se muuttuja, jota ei tunneta, ja tehdään siitä
            # muuttujasta toinen ratkaistava suure yhtälöpariin.
            for key in quantities:
                if key != 'vk' and quantities[key][1] == 'na':                                       
                    quantities[key][1] = '?*' # arvoksi aputuntemattomalle              
                    y = key  # Tämä avain on kysytyn lisäksi tuntematon suure,.
                             #.. jota varten tarvitaan toinenkin yhtälö.                                                  
            eq2 = eq2.subs(sijoitukset) # eq2 = sym.Eq(a*t - v + v0 , 0)                                              
            eq3 = eq3.subs(sijoitukset) # eq3 = sym.Eq(0.5*a*t**2 -s + t*v0 , 0)                                              
            ratk = solve([eq2, eq3], x, y, dict=True)                       
            suur_list = [t,a,s,vk,v,v0]
            z = sympify(kys1)
            for sr in suur_list:
                if z.compare(sr) == 0:
                    ratk = ratk[0][sr]                                                 
            
            if x == 't': 
                ratk = str(ratk)
                if ratk[-2:] == '*I':   # Välillä ratkaisu tulee kertolaskuna                  
                    ratk = ratk[:-2]
                ratk = float(ratk)
            ratk = abs(ratk)
            ratk = round(ratk,1)  
            
            if x == 't'or  x == 'v0':
                ratk = abs(ratk)
            vastaus = tulosta(ratk, kys1)                      
        else:
            print('Liian vähän dataa!')
    return vastaus                  

def pyöristys1(luku):    
        merkits_num = 3              # Pyöristys kolmeen merkitsevään numeroon
        luku =  round(luku, merkits_num - int(math.floor(math.log10(abs(luku)))) - 1)
        luku = str(luku)
        if luku[-2:] == '.0' and len(luku) > 4:
            luku = luku[:-2]         # Jättää ylimääräisen .0 :n pois
        return luku

def sigfiground(number:float, ndigits=3)->float:     
    return float(f"{number:.{ndigits}g}")

def tulosta(ratk, kys1):    
    ratk = sigfiground(ratk)                        
    tim = ''
    kmh = '' 
    km = ''
    if kys1 == 't':
        # AIKA: tunnit, minuutit, sekunnit
        ratk = abs(ratk)
        if ratk >= 3600: 
            # tunteja+minuutteja:
            m, s = divmod(ratk, 60) 
            h, m = divmod(m, 60)
            if s >= 30:
                m += 1
            tim = '= '+str(int(h))+' h '+str(int(m))+' min ' 
            vastaus = ' '+ quantities[kys1][3]+' '+ tim
            return vastaus
        elif ratk >= 60:
            # minuutteja + sekuntteja:
            m, s = divmod(ratk, 60)
            tim = '= '+str(int(m))+' min '+str(round(s))+' s'
            vastaus = ' '+ quantities[kys1][3]+' '+ tim
            return vastaus
        else:
            # sekuntteja:
            tim = '= '+str(round(ratk,1))+' s'
            vastaus = ' '+ quantities[kys1][3]+' '+ tim
            return vastaus
    if kys1 == 's':
        if ratk > 1000:
            ratk = pyöristys1(ratk/1000) # 3 num. tarkkuuteen moduli liike2.ssa
            km = ' = '+' '+str(ratk) + ' '+'km'
            vastaus = ' '+ quantities[kys1][3]+' '+ km
            return vastaus
        else:
          ratk = pyöristys1(ratk) 
    if kys1 == 'v':
        if ratk >= 10:
            ratk = round(ratk*3.6) 
            ratk = pyöristys1(ratk)
            kmh = ' = '+' '+str(ratk) + ' '+'km/h'
            vastaus = ' '+ quantities[kys1][3]+' '+ kmh
            return vastaus
        else:
          ratk = pyöristys1(ratk)     
    if kys1 == 'vk':
            ratk = round(ratk*3.6)  
            kmh = ' = '+' '+str(ratk) + ' '+'km/h'
            vastaus = ' '+ quantities[kys1][3]+' '+ kmh
            return vastaus
    if kys1 == 'a':
        for sa in sanat:
            if 'jarrut' in sa or 'pysäht' in sa:
                ratk = -ratk
        ratk = pyöristys1(ratk)  
        if float(quantities['v'][1]) < float(quantities['v0'][1]):
            ratk = '-' + ratk       
    sy_yk = {'vk':'m/s', 'v0':'m/s','v':'m/s', 't':'s', 'a':'m/s2', 's':'m'}
    # Kysytyn suureen kys1 yksikkö saadaan..'sy_yk'-sanakirjasta 
    vastaus = ' '+ quantities[kys1][3]+' '+' = '+' '+ str(ratk)+' '+ sy_yk[kys1]+kmh+tim+km
    return vastaus           #--> def ratkaise1_tas(x) / def ratkaise1_kii(x)

def sanakirja1():  # Tulostetaan 'quantities'
    for key in quantities:
        print(key, '=', quantities[key][1],  quantities[key][2])
    
def reset1():
    global q_laji  # Tallentaa liikelajin 
    q_laji = ''    # <-- liikelaji(txt)
    global txt     # Tehtäväteksti, käy läpi  muokkauksen 'muokkaa_teksti(txt)'
    txt = ''
    global sanat
    sanat = []
    global kys1    # Kysytty suure talteen 
    kys1 = ''
    global quantities # Suureiden symbolit arvot ja yksiköt
        
    quantities = {'t':[t,'na','na','aika'], 'a':[a,'na','na','kiihtyvyys'],
                  's':[s,'na','na','matka'],  'vk':[vk,'na','na','keskinopeus'],
                  'v0':[v0,'na','na','alkunopeus'], 'v':[v,'na','na','loppunopeus']}
    
    
def AJO1(txt):
    reset1()
    global sanat
    txt, sanat = muokkaa_teksti(txt)        # Muokattu teksti, splitattu teksti
    #print(sanat)
    global q_laji                           # Tallentaa liikelajin 
    q_laji = liikelaji(txt)                 # Tasainenko vaiko kiihtyvä liike
    quantities = tunnetut(sanat, q_laji)    # Tunnetut suureet 
    x = kysytty(sanat, q_laji)
    global kys1                             # Kysytty suure t,a,s,vk,v,v0
    kys1 = x
    quantities[x][1] = '?'                  # Kysytyn suureen arvoksi '?'
    quantities[x][2] = ''                   # Kysytyn suureen yksiköksi tyhjä
    special(sanat, kys1)
    SI(quantities)
    if q_laji == 'tas':
        vastaus = ratkaise1_tas(x)
        print(vastaus)
        return vastaus
    if q_laji == 'kii':
        vastaus = ratkaise1_kii(x)
        print(vastaus)
        return vastaus

if __name__ == "__main__":         # Kun tiedosto toimii itsenäisenä ohjelmana
    
    # OHJE: Kysy vain yhtä asiaa kerrallaan ( ei siis a),b),c) -kohtia )
    # Putoamiskiihtyvyyttä ei tarvitse antaa (= 9.81 m/s2)
    txt1 = 'Auto ajoi nopeudella 85km/h  5 h ajan. Kuinka pitkälle päästiin?'
    txt2 = 'Auto kiihtyy 150 m matkalla nopeudesta 15 km/h nopeuteen 80 km/h. Mikä on auton kiihtyvyys?'
    txt3 = 'Auto kiihdytti levosta vauhtiin 100 km/h 12 s aikana. Kuinka pitkän matkan auto kulki tänä aikana?'    
    txt4 = 'Syöksylaskijan nopeus on 63 km/h. Kuinka kauan aikaa kuluu häneltä 3 km:n matkaan?' # 2 min 51 s
    txt5 = 'Burj Khalifa on maailman korkein rakennus. Se on 828 metriä korkea. \
            Ilmanvastusta ei oteta laskuissa huomioon. Samppanjapullo pudotetaan huipulta. \
            Kuinka kauan putoaminen kestää?'
    test = 'Auto kiihtyy 150 m matkalla nopeudesta 15 km/h nopeuteen 80 km/h. Laske auton kiihtyvyys?'
    t89 = 'Avaruussukkulan kantoraketin kiihdytysvaihe lähdöstä kestää 124 sekuntia \
ja sukkulan tasainen kiihtyvyys on n. 5,6 m/s2. Tässä vaiheessa rakettiosa \
irtoaa. Mihin loppunopeuteen sukkula pääsee rakettinsa avulla?' 

# Tehtäviä löytyy 'Liike_tehtäviä.ipynb'-tiedostosta.

# A. Yksittäisen tehtävän ajaminen:   
    vastaus = AJO1(t89)                  
    #print(quantities) 
    print()
    print(vastaus)
    
# # B. Kaikki 101 kpl  1-dim esimerkkitehtävää ajetaan kerralla.
# # Tehtävät löytyvät tiedostosta 'Liike_tehtäviä.ipynb'.
# # Kopioi ensin tehtävät ja niiden lista 'dim1' tämän tiedoston alkuun,
# # jotta ne tulevat luetuiksi.
#     ind = 0
#     for kys in dim1:  
#         vastaus = AJO1(kys)
#         ind += 1
#         print(ind, vastaus)   
     
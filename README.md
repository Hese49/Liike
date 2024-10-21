**'Liike.py'  ReadMe**

This program is in Finnish. The program solves problems of motion of the given Finnish verbal problems.

Ohjelma laskee liikeopin laskuja syötetyistä sanallisista tehtävistä. 
(ei voimia) 

OHJELMAAN KUULUVAT  TIEDOSTOT
- **Liike.py**  tai (Jupyter  Liike.ipynb) muodostaa ajo-ohjelmaksi Tkinter graafisen käyttöliittymän  (GUI),
  jonka tekstikenttään laskutehtävä syötetään ja jonka tulostuskenttään laskettu tulos annetaan.
  Lisäksi tarvitaan allamainitut kaksi modulia suorittamaan varsinaisen tehtävänratkaisun. Kumpaakin moduleista voidaan käyttää myös itsenäisinä ohjelmina if ( if __name__ == "__main__": ).
- **Liike1b.py  (l1)**. Ratkaisumoduli yksidimensionaalisille liikkeille (esim. kulkuneuvojen  matka, aika, nopeus, kiihtyvyys sekä putoamisliikkeet ja  pystysuorat heitot).

- **Liike2b.py  (l2**). Ratkaisumoduli kaksidimensionaalisille liikkeille. Esim. kuulantyöntö, pallon heitto, ammusten lento jne. Liikkeille voidaan laskea kantama, lakikorkeus, lentoaika, lähtönopeus, lähtökulma, maahantulokulma, nopeuksien komponentit, koordinaatit annetulla hetkellä jne., kunhan vain  on annettu riittävästi lähtötietoja.

- **LiikeTehtäviä.rtf**, joka sisältää 144 esimerkkitehtävää  (mm. oppikirjoista ja internetistä), joita on käytetty ohjelman  kehittämisessä. (Esimerkkitehtävissä esiintyvät 'raketit' tulkitaan 'heitteiksi', joissa rakettimoottori ei työnnä liikkeen aikana)

OHJELMAN TOIMINTA
Ohjelma analysoi syötetyn tehtävätekstin siivilöiden niistä esiin tunnetut suureet ja kysytyn suureen. Sitten etsitään tehtävään sopivat yhtälöt ja käytetään symbolisen laskennan SymPy- modulia ratkaisemaan kysytty suure.
Ohjelman luonnollista kieltä 'ymmärtävä tekoäly' on tässä siis vain rajattun aihepiiriin tekstiin kohdistuvaa algoritmista prosessointia.

Ohjelman toiminnan pääpiirteisiin voi tutustua seuraavan esimerkitehtävän kautta. 

" Eräs EM-kisojen kilpailija työnsi harjoituksissa kuulaa 18,0 m. Kuulan lähtökulma oli 45 astetta ja lähtökorkeus maanpinnasta 2,0 m.  Kuinka suuri oli kuulan lähtönopeus?"   
 
- Aluksi GUI:n ratkaise-funktio lähettää tehtävätekstin modulille l1:lle, joka selvittää onko kyseessä yksi- vai kaksidimensionaalinen liike. Tämä tapahtuu vertaamalla annetun tekstin sanoja kummallekin eri liikemuodolle ominaisiin sanoihin/sanojen osiin. Esimerkissä sanat 'kuula' ja 'kulma' ovat sanoja, jotka ohjaavat 2-dim liikkeeseen. Saatuaan tämän tiedon GUI lähettää tehtävätekstin Liike2.py  (l2) modulille laskettavaksi.

- l2-modulissa tehtävän teksti muokataan ensin allaolevan kaltaiseksi sanojen, lukujen ja yksiköiden listaksi (sanat), josta on sitten helpompi tunnistaa kysytty suure sekä tunnetut suureet. (funktiot muokkaa1(txt) ja muokkaa2(txt)):

sanat = ['eräs', 'em-kisojen', 'kilpailija', 'työnsi', 'harjoituksissa', 'kuulaa', '18.0', 'm', 'kuulan', 'lähtökulma', 'oli', '45', 'astetta', 'ja', 'lähtökorkeus', 'maanpinnasta', '2.0', 'm', 'kuinka', 'suuri', 'oli', 'kuulan', 'lähtönopeus', '?']

-  Poimitaan sanat-listasta luvut ja yksiköt ja päätellään suuresymboli (funktio tunnetut()). Suureiden tunnistamisessa käytetään hyväksi suureiden yksiköitä,  naapurisanoja (funktio ymp(),  esim. lähtökulma on luvun 45 naapurustossa) sekä tyypillisten sanojen listoja. Kysyttyä suuretta tunnistetaan etsimällä kysymyssanaa (tässä löytyy 'kuinka') tai 'laske' sanaa,  jonka  perästä kysytty suure löytyy (tässä: lähtönopeus).

Suureet:
bt0 = 45.0 astetta
y0 = 2.0 m
yt = 0 m
xt = 18.0 m
v0 = ? 

- Kirjataan tehtävän luvut sanakirjaan quvh:
quvh = {'bt0':[bt0, 45,'astetta', 'Heittokulma'],
'v0':[v0,'?','m/s','Alkunopeus'],'v0x':[v0x,'na','m/s','Alkunop.x-komp.'],
'v0y':[v0y,'na','m/s','Alkunop. y-komp.'], 'y0':[y0, 2.0, 'm','Alkukorkeus'],
'ym':[ym,'na','m','Lakikorkeus'],'vx':[vx,'na','m/s','Vaakanopeus'],
't':[t,'na','s','Aika'],'tn':[tn,'na','s','Nousuaika'],
'vy':[vy,'na','m/s','Pystynopeus'],'yt':[yt,0,'m','Korkeus'],
'xt':[xt,18,'m','Kantama'], 'v':[v,'na','m/s','Loppunopeus'],
'bt':[bt,'na','astetta','Maahantulokulma']}

- Seuraavassa vaiheessa etsitään ( mikä_heitto() ), laskumenettelyjä ('heitto1', heitto2,...),  joihin tunnetut suureet riittävät. Kullekin laskumenettelylle on sanakirjassa h_ehd  oma listansa vaadittavista suureista. 
Esimerkin tilanteessa, kun käytettävissä ovat suureet   avail = ['bt0', 'y0', 'yt', 'xt'],
h_ehd -sanakirjasta löytyy avain:arvo -pari  'heitto3':['bt0','y0','xt'],  johon tuntemamme suureet riittävät. 

- Funktio heitto3() laskee  sitten SymPy -yhtälöparia 

   eq6 = sym.Eq(xt - v0x*t, 0)         &nbsp; &nbsp;         # xt = 18 m
  
   eq7 = sym.Eq(yt - y0 - v0y*t + 4.905*t**2, 0)   &nbsp; &nbsp;       # yt = 0 m, y0 = 0 m

käyttäen lähtönopeuden v0:
  - Sijoitetaan yhtälöön eq6 annettu kantama xt = 18 , jää v0x ja t.
  - Sijoitetaan yhtälöön eq7:   v0y = tan(bt0)*v0x,  yt=0  ja  y0 = 0.
  - Saadaan yhtälöpari, jonka tuntemattomat v0x ja t ratkaistaan.    
  -  etsitty  v0 = v0x/cos(bt0) 

- Kun ratkaisu (v0) on löydetty, moduli l2 pyöristää sen ( pyöristys() ) ja muotoilee vastauksen ( tulotus() ) lähettäen sitten  vastauksen käyttöliittymälle GUI tulostettavaksi tulostuskenttään. (Lähtönopeus = 12.6 m/s)
------------------------- 
Huom. Olen koodaajana vain harrastelija, joten koodissa olisi varmaan paljonkin parantamisen varaa, ja otan huomautuksia ja parannusehdotuksia mielelläni vastaan.  Koodi kuitenkin toimii kohtuullisen hyvin  laajalle valikoimalle sanallisia tehtäviä. :)
H.M.

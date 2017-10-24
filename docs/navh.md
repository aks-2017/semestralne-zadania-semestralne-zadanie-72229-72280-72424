# Slovenská Technická Univerzita v Bratislave
## Dynamic Traffic Diversion in SDN: Testbed vs Mininet
<br />

### Lukáš Mastiľák, Ján Pánis, Andrej Vaculčiak

#### Analýza článku
Táto časť dokumentu sa venuje opisu pôvodného riešenia podľa referenčného článku, spolu s výsledkami testovania.

##### Úvod
Pre vývoj v oblasti sieťových zariadení je pomerne často využívaný emulovaný systém. Má množstvo výhod, no tak isto aj svoje nevýhody. Pre SDN siete paltí podobné pravidlo. Avšak, naskytá sa otázka, či je emulovaný systém dôveryhodným zdrojom výsledkov.
Overenie tejto problematiky bolo témou článku, ktorý sme si vybrali. Porovnáva reálne prostredie, tvorené fyzickými prepínačmi s podporou SDN a emulátorom Mininet.

###### Software Defined Networks
Posledných niekoľko rokov sa do popredia v oblasti sietí dostali tzv. SDN, čiže softvérovo definované siete. Základnou myšlienkou týchto sietí je oddelenie riadiacej časti od dátovej. Každá dnes bežná sieť je zložená z komponentov, ktoré obsahujú hardvérovú časť, zabezpečujúcu smerovanie a prepínanie a softvérovú časť, ktorá rieši spracovanie požiadaviek, prípadne výpočty pre smerovacie protokoly a pod.
Problém ale je napr. v pomerne zložitom spôsobe zabezpečenia kompatibility, potrebe nastavovania každého prvku siete samostatne ale aj závislosti na podpore od výrobcu.
Preto sa prišlo s myšlienkou oddelenia kontrolnej časti sieťových prvkov a vytvoriť jeden centrálny prvok (tzv. controller), ktorý zabezpečí kontrolu nad sieťou. Výhodou takéhoto prístupu je, o. i. centralizovaná konfigurácia siete, možnosť videnia celej topológie s pohľadu controllera, čím sa napríklad odstraňuje potreba smerovacích protokolov prítomných v každom zo sieťových zariadení a zbytočne dlhá konvergencia siete pri výpadku. Ako ďalšie pozítívum sa vníma aj oveľa zjedonušená možnosť aplikácie tzv. traffic engineering-u. 

##### Topológia
V návrhu topológie boli použité tri prepináče a OpenDaylight kontrolér.
Topológia bola implementovaná v prostredí Mininet a tiež reálne vytvorená
pomocou Cisco prepínačov podporujúcich SDN.  Sieť bola tiež pripojená k
Internetu.
Základnú časť topológie tvoria tri SDN prepínače, ktoré sú navzájom prepojené.
Prepínače sú označené číslami od 1 do 3. K prepínačom 1 a 3 sú pripojené dve
koncové zariadenia. Daný návrh topológie ponúka pri komunikácií medzi koncovými
zariadeniami na rôznych prepínačov viacero ciest, ktorými môže komunikácia
prebiehať. Jedna cesta slúži ako primárna cesta a v prípade, že táto cesta je
preťažená, tak sa premávka presmeruje cez záložnú cestu. Takto je možné udržať
latenciu a jitter na minimum. V návrhu tiež sa počíta s tým, že redundantné
cesty sú blokované, aby sa vyhlo zahladeniu na prepínačoch, kvôli možným
slučkám.
Ďalším prvkom topológii bol kontrolér OpenDaylight, ktorý bežal na virtuálnom
servery s OS Ubuntu. Výber daného kontroléra bol ovplyvnení širokou podporou
Java na rôznych zariadeniach. OpenDaylight bol použitý aj pre reálnu
implementáciu, ako aj pre prostredie Mininet.
Pre realizáciu topológie boli vybrané prepínače Cisco Catalyst 3650, ktoré
bežali na skorej trial verzií IOS-XE s podporou pre OpenFlow. Mala byť
podporovaná verzia OpenFlow 1.3, ale autorom   nefungovala komunikácia
prepínačov s kontrolórom. Preto sa rozhodli pre vyskúšanie verzie 1.0, kde
komunikácia už bola funkčná.  Všetky porty na prepínačoch boli 100 Mbps. Koncové
zariadenia bežali na OS Lubuntu a na každom z nich bol nainštalovaný nástroj na
meranie Iperf. 
##### Algoritmus DTD

##### Testovanie a výsledky
Obsahom testovania bolo overenie hypotézy o dôveryhodnosti výsledkov, ktoré ponúka Mininet oproti reálnemu prostrediu tvorenému Cisco prepínačmi s podporou SDN. Prenosová rýchlosť liniek bola nastavená na 100Mb/s.
Testované boli 3 scenáre:

1. Základný test
2. Výkonnostný test bez DTD
3. Výkonnostný test s použitím DTD

###### Základný test
Úlohou základného testu je zistiť počiatočné podmienky a vlastnosti (jitter) danej topológie. Spočíva v UDP komunikácií uzlov H1 a H3. Uzol H1 posiela 600MB dát rýchlosťou 50Mb/s a nakoľko tam nie je žiadna iná premávka, nedochádza k strate paketov a jitter je sposobený len oneskorením na linkách.

###### Výkonnostný test bez DTD
Hlavným cieľom tohto scenára bolo určiť správanie sa siete počas zahltenia. Uzly H1 a H3 komunikujú rovnako ako v prípade 1. testu. Okrem nich však do siete pribudla komunikácia ulzov H2 a H, ktoré si posielajú veľké množstvo UDP dát rýchlosťou 95Mb/s. Táto skutočnosť zapríčiní zahltenie linky medzi prepínačmi a teda zvýši sa stratovosť paketov a zvýši jitter.

###### Výkonnostný test s použitím DTD

#### Návrh projektu

#### Mininet

#### Reálne prostredie

#### Zhodnotenie a porovnanie emulovaných a reálnych výsledkov

#### Literatúra

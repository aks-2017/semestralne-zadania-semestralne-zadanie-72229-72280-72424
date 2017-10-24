# Slovenská Technická Univerzita v Bratislave
## Dynamic Traffic Diversion in SDN: Testbed vs Mininet
<br />

### Lukáš Mastiľak, Ján Pánis, Andrej Vaculčiak

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

##### Algoritmus DTD
Algoritmus DTD (Dynamic Traffic Diversion) bol vytvorený pre testovacie účely, pomocou ktorého je možné dynamicky meniť tok premávky, za účelom zníženia straty paketov a jitter-u.

Strata paketov je zlyhanie odosielaných paketov, ktoré prichádzajú do cieľa, zatiaľ čo jitter je meranie odchýlky v čase medzi doručením paketu.

Úlohou algoritmu je v pravidelných intervaloch vyhodnocovať vyťaženosť portov na smerovačoch a v prípade zahltenia (resp. prekročenia stanovenej hranice), odľahčiť tok dát záložnou linkou. Ak v nejakom okamihu klesne hranica vyžaženosti opäť na prijateľnú, záložná linka sa prestane využívať a premávka bude posielaná cez prioritnú linku. Popis algoritmu je tiež možno vidieť v aktivity diagrame č. X pod odstavcom.

![DTD_algo][DTD_algo]

[DTD_algo]: https://github.com/aks-2017/semestralne-zadania-semestralne-zadanie-xmastilak-xpanis-xvaculciak/blob/master/docs/pictures/DTD_algo.png
Obr. X - Aktivity diagram algortimu DTD

Tieto hranice boli vyčíslené na hodnoty:
* Horná hranica - 90% kapacity linky (v prípade, že ide o 100Mbit/s pri prekročení 90Mbit/s, nastane presmerovanie toku)
* Dolná hranica - 70% kapacity linky.

Na vytvorenie aplikácie sa rozhodli využiť Python z dôvodu, že pri základnom testovaní využívali klasický program príkazového riadku - cURL, ktorý je možné využívať aj v Python-e. Ten bol využitý aj na získavanie informácií o portoch dostupný pomocou OpenDaylight Northbount REST API.

Pre otestovanie tohto algoritmu, zostrojili testovaciu topológiu skladajúcu sa z 3-ch hlavných prepínačov prepojených každý s každým (jedna cesta je primárna, druhá sekundárna). Viac o topológií je písané v kapitole Topológia.

Na testovanie rýchlosti, straty paketov a jitter-u využili program IPerf, ktorý je zároveň generátorom paketov ako aj nástrojom pre rôzne merania v sieti. Daný program sa využíva na ladenie výkonu v sieťach a medzi jeho hlavné výhodny patria:
* Schopnosť fungovania na rôznych platformách (Windows, Unix, Linux)
* Otvorený zdrojový kód napísaný v jazyku C
* Umožňuje jednostranné ale aj obojsmerné merania
* Dáta môžu byť vysielané protokolom UDP ale aj TCP s nastaviteľnými veľkosťami okien

##### Testovanie
Obsahom testovania bolo overenie hypotézy o dôveryhodnosti výsledkov, ktoré ponúka Mininet oproti reálnemu prostrediu tvorenému Cisco prepínačmi s podporou SDN. Prenosová rýchlosť liniek bola nastavená na 100Mb/s.
Túto hypotézu overovali pomocou implementácie DTD algoritmu a sledovaní správania sa siete v rôznych scenároch.
Testované boli 3 scenáre:

1. Základný test
2. Výkonnostný test bez DTD
3. Výkonnostný test s použitím DTD

###### Základný test
Úlohou základného testu je zistiť počiatočné podmienky a vlastnosti (jitter) danej topológie. Spočíva v UDP komunikácií uzlov H1 a H3. Uzol H1 posiela 600MB dát rýchlosťou 50Mb/s a nakoľko tam nie je žiadna iná premávka, nedochádza k strate paketov a jitter je sposobený len oneskorením na linkách.

Porovnanie hodnôt jitteru pre obe testované prostredia (scenár 1):
 
![Test 1 Graph][test_1]

[test_1]: https://github.com/aks-2017/semestralne-zadania-semestralne-zadanie-xmastilak-xpanis-xvaculciak/blob/master/docs/pictures/test_1.PNG

###### Výkonnostný test bez DTD
Hlavným cieľom tohto scenára bolo určiť správanie sa siete počas zahltenia. Uzly H1 a H3 komunikujú rovnako ako v prípade 1. testu. Okrem nich však do siete pribudla komunikácia ulzov H2 a H4, ktoré si posielajú veľké množstvo UDP paketov rýchlosťou 95Mb/s. Táto skutočnosť zapríčiní zahltenie linky medzi prepínačmi a teda zvýši sa stratovosť paketov a zvýši jitter, čo je predpokladaný jav. Okrem toho sa začnú strácať pakety, pričom táto stratovosť dosiahla v priemere 50% pre reálne prostredie a 34% v Mininete.

Porovnanie hodnôt jitteru pre obe testované prostredia (scenár 2):
 
![Test 2 Graph][test_2]

[test_2]: https://github.com/aks-2017/semestralne-zadania-semestralne-zadanie-xmastilak-xpanis-xvaculciak/blob/master/docs/pictures/test_2.PNG

###### Výkonnostný test s použitím DTD
Cieľom tohto testu bolo overiť hypotézu, či aplikácia za použitia DTD dokáže znížiť čas potrebný na doručenie paketov (jitter) a zvýši celkovú doručiteľnsoť paketov (packet loss). Scenár je v podstate identický s predchádzajúcim, no pribudla v ňom situácia, v ktorej, keď dojde k zahlteniu linky na viac, ako 90%, presmeruje sa premávka z H1 do H3 na záložnú linku, čím sa má dosiahnuť spomínaný cieľ.

Porovnanie hodnôt jitteru pre obe testované prostredia (scenár 3):
 
![Test 3 Graph][test_3]

[test_3]: https://github.com/aks-2017/semestralne-zadania-semestralne-zadanie-xmastilak-xpanis-xvaculciak/blob/master/docs/pictures/test_3.PNG

Ako už bolo spomenuté, maximálna hodnota využitia linky, ktorá sa považuje za kritickú, je 90%, čiže 90Mb/s. Avšak, v prípade, že využitie linky kleslo, tým pádom už zahltenie na prioritnej ceste nemáme, premávka sa zo záložnej linky presmeruje opäť na štandardnú. Táto situácia nastane, ak je využitie danej linky pod 70%, a teda 70Mb/s.

##### Vyhodnotenie testovania
Ako môžeme vidieť na grafoch zobrazujúcich výsledky meraní, autori prišli k záveru, že ich hypotéza o dôveryhodnosti výsledkov, ktoré poskytuje Mininet oproti reálnemu prostrediu a faktu, že nedochádzalo k stratám paketov pri aplikovaní DTD, bola správna. Avšak, pri testovaní 3. scenára sa objavila veľmi malá hodnota jitteru v Mininet prostredí, čo sa ale dá odôvodniť faktom, že Mininet je integrovaný na jednom stroji. Okrem toho neaplikovali do Mininetu oneskorenie na linkách, čo koniec koncov tak isto ovplyvnilo výsledky meraní a rozdiel v priemerných hodnotách.

#### Návrh projektu
Náš projekt sa skladá z dvoch hlavných častí, ktoré overujú referenčný článok (otestovanie algoritmu DTD, porovnanie oneskorení, rýchlosti a jitter-u):
1. v emulátore Mininet,
2. a na reálnych zariadeniach Soekris net6501.

Architektúra daného SDN prostredia sa skladá z nasledujúcich prvkov a je pre oba prípady totožná. RYU SDN kontrolér, ktorého úlohou je poskytovať medzivrstvu medzi prepínačmi (či už reálnymi, alebo emulovanými v Mininet-e ktoré podporujú OpenFlow) a externou aplikáciou. Okrem iného korektne riadiť tok dát v sieti, ktorý môže byť dynamicky upravený pomocou aplikácie. Táto aplikácia s RYU kontrolérom komunikuje pomocou REST API a následne cez tohto prostredníka sa dostávajú riadiace informácie do prepínačov. Tento opis je taktiež možno vidieť na nasledujúcom.

(OBRÁZOK architektúry SND - app + ryu + Oflow)!!!

##### Mininet

##### Reálne prostredie

#### Zhodnotenie a porovnanie emulovaných a reálnych výsledkov

#### Literatúra

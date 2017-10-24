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

#### Mininet

#### Reálne prostredie
Na testovanie SDN siete v reálnom prostredí používame zariadenia Soekris net6501, na ktorých je OS Debian. Architektúra je podobná s Mininet architektúrou. Rozdiel je v použití fyzických SDN prepínačov namiesto Mininet emulátora. V prepínači je na OS Debian spustený proces Open vSwitch, ktorý podporuje OpenFlow. Daný prepínač komunikuje s controllerom, ktorý je implementovaný pomocou RYU a nad ním je aplikácia, ktorá implementuje DTD algoritmus a pomocou RYU API dáva inštrukcie konkrétnym prepínačom, aby sa vytvorila cesta pre konkrétne pakety záložnou cestou.

**(OBRÁZOK architektúry)!!!**

Čo sa ale týka zapojenia a samotnej topológie, bolo potrebné pristúpiť k zmenám, nakoľko nemáme k dispozícií taký počet SDN prepínačov a ani portov na prepínačoch.
Je teda pravepodobné, že nebude možné vykonať merania na fyzickej topológií tak, aby ju bolo možné porovnať s Mininet topológiou. Vykoná sa len zapojenie a testovanie funkčnosti zapojenia SDN reálnej siete.

Navrhovaná topológia vyzerá nasledovne:
**(OBRÁZOK fyz. topológie)!!!** 


#### Zhodnotenie a porovnanie emulovaných a reálnych výsledkov

#### Literatúra
https://www.rfc-editor.org/rfc/pdfrfc/rfc7426.txt.pdf
# Slovenská Technická Univerzita v Bratislave
## Dynamic Traffic Diversion in SDN: Testbed vs Mininet
<br />

### Lukáš Mastiľak, Ján Pánis, Andrej Vaculčiak

#### Analýza článku
Táto časť dokumentu sa venuje opisu pôvodného riešenia podľa referenčného článku, spolu s výsledkami testovania.

##### Úvod
Pre vývoj v oblasti sieťových zariadení je pomerne často využívaný emulovaný systém. Má množstvo výhod, no tak isto aj svoje nevýhody. Pre SDN siete platí podobné pravidlo. Avšak, naskytá sa otázka, či je emulovaný systém dôveryhodným zdrojom výsledkov.

Overenie tejto problematiky bolo témou článku, ktorý sme si vybrali. Porovnáva reálne prostredie, tvorené fyzickými prepínačmi s podporou SDN a emulátorom Mininet.

###### Software Defined Networks
Posledných niekoľko rokov sa do popredia v oblasti sietí dostali tzv. SDN, čiže softvérovo definované siete. Základnou myšlienkou týchto sietí je oddelenie riadiacej časti od dátovej. Každá dnes bežná sieť je zložená z komponentov, ktoré obsahujú hardvérovú časť, zabezpečujúcu smerovanie a prepínanie a softvérovú časť, ktorá rieši spracovanie požiadaviek, prípadne výpočty pre smerovacie protokoly a pod.
Problém ale je napr. v pomerne zložitom spôsobe zabezpečenia kompatibility, potrebe nastavovania každého prvku siete samostatne ale aj závislosti na podpore od výrobcu [1, 2].

Preto sa prišlo s myšlienkou oddelenia kontrolnej časti sieťových prvkov a vytvoriť jeden centrálny prvok (tzv. controller), ktorý zabezpečí kontrolu nad sieťou. Výhodou takéhoto prístupu je, o. i. centralizovaná konfigurácia siete, možnosť videnia celej topológie z pohľadu controllera, čím sa napríklad odstraňuje potreba smerovacích protokolov prítomných v každom zo sieťových zariadení a zbytočne dlhá konvergencia siete pri výpadku. Ako ďalšie pozítívum sa vníma aj oveľa zjednodušená možnosť aplikácie tzv. traffic engineering-u [2]. 

##### Topológia
Základnú časť topológie siete na Obr. 1 tvoria tri SDN prepínače, ktoré sú
navzájom prepojené kvôli redundantným cestám. Prepínače sú označené číslami od 1
do 3. K prepínačom 1 a 3 sú pripojené dve koncové zariadenia. Daný návrh
topológie ponúka pri komunikácií medzi koncovými zariadeniami viacero ciest, ktorými môže komunikácia prebiehať. Jedna z nich slúži ako primárna cesta a v prípade, že na nej vznikne zahltenie premávka sa presmeruje cez záložnú cestu. Takto je možné udržať jitter a straty paketov na minimum. V návrhu topológie sa počíta aj s ošetrením proti možnému vzniku slučiek.

Ďalším prvkom topológie je controller OpenDaylight, ktorý beží na virtuálnom
serveri s OS Ubuntu. Výber daného controllera bol ovplyvnení širokou podporou Java na rôznych platformách. OpenDaylight bol použitý tak pre reálnu implementáciu, ako aj pre prostredie Mininet [1].

Pri realizáciu topológie boli vybrané prepínače Cisco Catalyst 3650, na ktorých bežala trial verzia IOS-XE s podporou pre OpenFlow. Autori počítali s podporou verzie OpenFlow 1.3, ale komunikácia medzi prepínačmi a controllerom nefungovala, preto sa rozhodli pre vyskúšanie verzie 1.0, kde komunikácia už bola funkčná.  Všetky porty na prepínačoch boli nastavené na 100 Mbps. Koncové zariadenia bežali na OS Lubuntu a na každom z nich bol nainštalovaný nástroj na meranie výkonu siete Iperf [1, 3, 4].

<img align="center" alt="Topology picture" src="https://github.com/aks-2017/semestralne-zadania-semestralne-zadanie-xmastilak-xpanis-xvaculciak/blob/navrh_luka/docs/pictures/topology.png" width="400">

Obr. 1 - Návrh topológie [1]

##### Algoritmus DTD
Algoritmus DTD (Dynamic Traffic Diversion) bol vytvorený pre testovacie účely. Je pomocou neho možné dynamicky meniť tok premávky, za účelom zníženia straty paketov a jitter-u [1].

Strata paketov je spôsobená zlyhaním prenosu paketov, ktoré prichádzajú do cieľa, zatiaľ čo jitter je kolísanie veľkosti oneskorenia paketov počas prenosu sieťou [1].

Úlohou algoritmu je v pravidelných intervaloch vyhodnocovať vyťaženosť portov na smerovačoch a v prípade zahltenia (resp. prekročenia stanovenej hranice vyťaženia linky), odľahčiť tok dát použitím záložnej linky. Ak v nejakom okamihu klesne hranica vyťaženosti opäť na prijateľnú, záložná linka sa prestane využívať a premávka bude posielaná cez prioritnú linku. Popis algoritmu je tiež možné vidieť v aktivity diagrame na Obr. 2 pod odstavcom [1].

<img align="center" alt="DTD_algo" src="https://github.com/aks-2017/semestralne-zadania-semestralne-zadanie-xmastilak-xpanis-xvaculciak/blob/master/docs/pictures/DTD_algo.png" width="400">

Obr. 2 - Aktivity diagram algoritmu DTD [1]

Hranice boli vyčíslené na hodnoty:
* Horná hranica - 90% kapacity linky (v prípade, že ide o 100Mb/s pri prekročení 90Mb/s, nastane presmerovanie toku)
* Dolná hranica - 70% kapacity linky [1].

Na vytvorenie aplikácie sa rozhodli využiť Python z dôvodu, že pri základnom testovaní využívali klasický program príkazového riadku - cURL, ktorý je možné využívať aj v Python-e. Ten bol využitý aj na získavanie informácií o portoch dostupných pomocou OpenDaylight Northbount REST API [1].

Pre otestovanie algoritmu zostrojili testovaciu topológiu skladajúcu sa z 3 hlavných prepínačov, prepojených každý s každým (jedna cesta je primárna, druhá sekundárna). Viac o topológií je písané v kapitole Topológia [1].

Na testovanie rýchlosti, straty paketov a jitter-u využili program Iperf, ktorý je zároveň generátorom paketov ako aj nástrojom pre rôzne merania v sieti. Daný program sa využíva na ladenie výkonu v sieťach a medzi jeho hlavné výhody patria:
* Schopnosť fungovania na rôznych platformách (Windows, Unix, Linux)
* Otvorený zdrojový kód napísaný v jazyku C
* Umožňuje jednosmerné, ale aj obojsmerné merania
* Dáta môžu byť vysielané protokolom UDP ale aj TCP s nastaviteľnými veľkosťami okien [1, 3, 4]

##### Testovanie
Obsahom testovania bolo overenie hypotézy o dôveryhodnosti výsledkov, ktoré ponúka Mininet oproti reálnemu prostrediu, tvorenému Cisco prepínačmi s podporou SDN. Prenosová rýchlosť liniek bola nastavená na 100Mb/s [1].
Túto hypotézu overovali pomocou implementácie DTD algoritmu a sledovaní správania sa siete v rôznych scenároch.
Testované boli 3 scenáre:

1. Základný test
2. Výkonnostný test bez DTD
3. Výkonnostný test s použitím DTD [1]

###### Základný test
Úlohou základného testu je zistiť počiatočné podmienky a vlastnosti (jitter, stratovosť paketo a ich oneskorenie) danej topológie. Spočíva v UDP komunikácií uzlov H1 a H3. Uzol H1 posiela 600MB dát rýchlosťou 50Mb/s a nakoľko tam nie je žiadna iná premávka, nedochádza k strate paketov a jitter je spôsobený len oneskorením na linkách [1].
 
![Test 1 Graph][test_1]

[test_1]: https://github.com/aks-2017/semestralne-zadania-semestralne-zadanie-xmastilak-xpanis-xvaculciak/blob/master/docs/pictures/test_1.PNG
Obr. 3 - Porovnanie hodnôt jitter-u pre obe testované prostredia (scenár 1) [1]

###### Výkonnostný test bez DTD
Hlavným cieľom tohto scenára bolo určiť správanie sa siete počas zahltenia. Uzly H1 a H3 komunikujú rovnako ako v prípade 1. testu. Okrem nich však do siete pribudla komunikácia ulzov H2 a H4, ktoré si posielajú veľké množstvo UDP paketov rýchlosťou 95Mb/s. Táto skutočnosť zapríčiní zahltenie linky medzi prepínačmi a teda zvýši sa stratovosť paketov a aj jitter, čo je predpokladaný jav. Začnú sa strácať pakety, pričom táto stratovosť dosiahla v priemere 50% pre reálne prostredie a 34% v Mininete [1].
 
![Test 2 Graph][test_2]

[test_2]: https://github.com/aks-2017/semestralne-zadania-semestralne-zadanie-xmastilak-xpanis-xvaculciak/blob/master/docs/pictures/test_2.PNG
Obr. 4 - Porovnanie hodnôt jitter-u pre obe testované prostredia (scenár 2) [1]

###### Výkonnostný test s použitím DTD
Cieľom tohto testu bolo overiť hypotézu, či aplikácia za použitia DTD dokáže znížiť jitter a zvýšiť celkovú doručiteľnsoť paketov (packet loss). Scenár je v podstate identický s predchádzajúcim, no pribudla v ňom situácia, v ktorej, keď dôjde k zahlteniu linky na viac ako 90%, presmeruje sa premávka z H1 do H3 na záložnú linku, čím sa má dosiahnuť spomínaný cieľ [1].
 
![Test 3 Graph][test_3]

[test_3]: https://github.com/aks-2017/semestralne-zadania-semestralne-zadanie-xmastilak-xpanis-xvaculciak/blob/master/docs/pictures/test_3.PNG
Obr. 5 - Porovnanie hodnôt jitter-u pre obe testované prostredia (scenár 3) [1]

Ako už bolo spomenuté, maximálna hodnota využitia linky, ktorá sa považuje za kritickú, je 90%, čiže 90Mb/s. Avšak, v prípade, že využitie linky kleslo, tým pádom už zahltenie na prioritnej ceste nemáme, premávka sa zo záložnej linky presmeruje opäť na prioritnú linku. Táto situácia nastane, ak je využitie danej linky pod 70%, a teda 70Mb/s [1].

##### Vyhodnotenie testovania
Ako môžeme vidieť na grafoch zobrazujúcich výsledky meraní, autori prišli k záveru, že ich hypotéza o dôveryhodnosti výsledkov, ktoré poskytuje Mininet oproti reálnemu prostrediu a faktu, že nedochádzalo k stratám paketov pri aplikovaní DTD, bola správna. Avšak, pri testovaní 3. scenára sa objavila veľmi malá hodnota jitteru v Mininet prostredí, čo sa ale dá odôvodniť faktom, že Mininet je integrovaný na jednom stroji. Okrem toho neaplikovali do Mininetu oneskorenie na linkách, čo koniec koncov tak isto ovplyvnilo výsledky meraní a rozdiel v priemerných hodnotách [1].

#### Návrh projektu
Náš projekt sa skladá z dvoch hlavných častí, ktoré overujú referenčný článok (otestovanie algoritmu DTD, porovnanie oneskorení, rýchlosti a jitter-u):
1. v emulátore Mininet,
2. a na reálnych zariadeniach Soekris net6501 [1].

Architektúra daného SDN prostredia sa skladá z nasledujúcich prvkov a je pre oba prípady totožná. 
* RYU SDN controller, ktorého úlohou je poskytovať medzivrstvu medzi prepínačmi (či už reálnymi, alebo emulovanými v Mininet-e ktoré podporujú OpenFlow) a externou aplikáciou. Okrem iného korektne riadi tok dát v sieti, ktorý môže byť dynamicky upravený pomocou aplikácie. 
* Aplikácia s RYU controllerom komunikuje pomocou REST API a následne cez tohto prostredníka sa dostávajú riadiace informácie do prepínačov. Tento opis je taktiež možno vidieť na nasledujúcom obrázku [1].

<img align="center" alt="architecture_design" src="https://github.com/aks-2017/semestralne-zadania-semestralne-zadanie-xmastilak-xpanis-xvaculciak/blob/navrh_luka/docs/pictures/architecture.png" width="400">

Obr. 6 - Návrh architektúry

##### Mininet
V návrhu našej topológie sme sa rozhodli trochu upraviť pôvodnú topológiu tým, že niektoré časti sme sa rozhodli vynechať. Konfigurácia siete bude na základe controllera. Chceme minimalizovať akúkoľvek konfiguráciu na prepínačoch. Určenie primárnej a v prípade potreby sukundárnej cesty sa bude riešiť cez controller podobne ako v pôvodnom riešení.

<img align="center" alt="Mininet_topology" src="https://github.com/aks-2017/semestralne-zadania-semestralne-zadanie-xmastilak-xpanis-xvaculciak/blob/navrh_luka/docs/pictures/topology1.png" width="400">

Obr. 7 - Návrh topológie pre Mininet


##### Reálne prostredie
Na testovanie SDN siete v reálnom prostredí používame zariadenia Soekris net6501, na ktorých je OS Debian. Architektúra je podobná s Mininet architektúrou. Rozdiel je v použití fyzických SDN prepínačov namiesto Mininet emulátora. V prepínači je na OS Debian spustený proces Open vSwitch, ktorý podporuje OpenFlow. Daný prepínač komunikuje s controllerom, ktorý je implementovaný pomocou RYU a nad ním je aplikácia, ktorá implementuje DTD algoritmus. Aplikácia pomocou RYU API dáva inštrukcie konkrétnym prepínačom, aby sa vytvorila cesta pre konkrétne pakety záložnou cestou.

Čo sa ale týka zapojenia a samotnej topológie, bolo potrebné pristúpiť k zmenám, nakoľko nemáme k dispozícií taký počet SDN prepínačov a ani portov na prepínačoch.
Je teda pravdepodobné, že nebude možné vykonať merania na fyzickej topológií tak, aby ju bolo možné porovnať s Mininet topológiou. Vykoná sa len zapojenie a testovanie funkčnosti zapojenia SDN reálnej siete. Navrhovaná topológia vyzerá nasledovne:

<img align="center" alt="Real_topology" src="https://github.com/aks-2017/semestralne-zadania-semestralne-zadanie-xmastilak-xpanis-xvaculciak/blob/navrh_luka/docs/pictures/topology2.png" width="400">

Obr. 8 - Návrh topológie pre reálne prostredie

#### Zhodnotenie a porovnanie emulovaných a reálnych výsledkov

Výsledky práce v prvom rade dospeli k tomu, že navrhovaný algoritmus DTD je vhodné použiť na minimalizáciu jitteru a stratovosti paketov. Ďalej je tento algoritmus vhodný na riešenie zahltenia na primárnej linke. Takto je možné dosiahnuť, aby premávka s vysokou prioritou nebola blokovaná premávkou s nižšou prioritou na primárnej linke.

Druhý výsledok práce sa zaoberá porovnaním výsledkov meraní z prostredia Mininet a reálneho prostredia. Dosiahnuté hodnoty v obidvoch prostredí sú porovnateľné. Z čoho je možné predpokladať, že prostredie Mininet je dostatočné na to, aby sa priblížilo dosiahnutými výsledkami k reálnemu prostrediu [1].

#### Literatúra
[1] BARRETT, Robert, et al. Dynamic Traffic Diversion in SDN: testbed vs Mininet. In: Computing, Networking and Communications (ICNC), 2017 International Conference on. IEEE, 2017. p. 167-171 (http://ieeexplore.ieee.org/document/7876121/references).

[2] HALEPLIDIS, Evangelos, et al. Software-defined networking (SDN): Layers and architecture terminology. 2015 (https://www.rfc-editor.org/rfc/pdfrfc/rfc7426.txt.pdf).

[3] Schroder Carla, Measure Network Performance with iperf [online]. Január 2007. Dostupné na internete: <http://www.enterprisenetworkingplanet.com/netos/article.php/3657236/Measure-Network-Performance-with-iperf.htm>

[4] Iperf - The TCP/UDP Bandwidth Measurement Tool, Online:
(http://sourceforge.net/projects/iperf2/)

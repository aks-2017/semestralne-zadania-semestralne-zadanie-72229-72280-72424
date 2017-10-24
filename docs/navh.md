# Slovenská Technická Univerzita v Bratislave
## Dynamic Traffic Diversion in SDN: Testbed vs Mininet
<br />

### Lukáš Mastiľák, Ján Pánis, Andrej Vaculčiak

#### Analýza článku

##### Úvod

##### Topológia

##### Algoritmus DTD
Algoritmus DTD (Dynamic Traffic Diversion) bol vytvorený pre testovacie účely, pomocou ktorého je možné dynamicky meniť tok premávky, za účelom zníženia straty paketov a jitter-u.

Strata paketov je zlyhanie odosielaných paketov, ktoré prichádzajú do cieľa, zatiaľ čo jitter je meranie odchýlky v čase medzi doručením paketu.

Úlohou algoritmu je v pravidelných intervaloch vyhodnocovať vyťaženosť portov na smerovačoch a v prípade zahltenia (resp. prekročenia stanovenej hranice), odľahčiť tok dát záložnou linkou. Ak v nejakom okamihu klesne hranica vyžaženosti opäť na prijateľnú, záložná linka sa prestane využívať a premávka bude posielaná cez prioritnú linku. Popis algoritmu je tiež možno vidieť v aktivity diagrame č. X pod odstavcom.

[DTD_algo]:https://github.com/aks-2017/semestralne-zadania-semestralne-zadanie-xmastilak-xpanis-xvaculciak/blob/master/docs/pictures/DTD_algo.png
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

##### Testovanie a výsledky

#### Návrh projektu

#### Mininet

#### Reálne prostredie

#### Zhodnotenie a porovnanie emulovaných a reálnych výsledkov

#### Literatúra

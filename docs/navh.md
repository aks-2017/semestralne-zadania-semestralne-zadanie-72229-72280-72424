# Slovenská Technická Univerzita v Bratislave
## Dynamic Traffic Diversion in SDN: Testbed vs Mininet
<br />

### Lukáš Mastiľák, Ján Pánis, Andrej Vaculčiak

#### Analýza článku

##### Úvod

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
##### Algoritmus DTD

##### Testovanie a výsledky

#### Návrh projektu

#### Mininet

#### Reálne prostredie

#### Zhodnotenie a porovnanie emulovaných a reálnych výsledkov

#### Literatúra

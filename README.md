# RayTracing
## Benutzung
Bsp.: `python raytracing.py OpticalSystems/Uebung.txt`

## Ziele
Berechnungen:
- [x] Bild: Lage und Höhe
- [x] Austrittspupille: Lage und Größe
- [x] Eintrittspupille: Lage und Größe
- [x] objektiv- und bildseitige Numerische Apertur
- [x] Haupt- und Randstrahl
- [x] effective, front und back focal length (efl, ffl, bfl)
- [x] f-Zahl
- [x] Lage Hauptebenen
- [x] Abbildungsverhältnis
- [x] Seidelaberrationen

Exceptions abfangen:
- [x] R = 0 -> Fehlerausgabe sowie R = inf
- [x] Werte und Datentypen in optischem System prüfen
- [x] optisches System darf nur ein *Stop* besitzen
- [x] optisches System darf nur ein *Objekt* besitzen
- [x] optisches System darf nur aus folgenden Typen bestehen: O (Object), L (Lens), S (Stop), I (Image)
- [x] optisches System darf nur ein *Image* besitzen, welches sich am Ende befinden muss

Verschönerungen:
- [x] Objekt(-ebene) einzeichnen
- [x] Bild(-ebene) einzeichnen
- [x] Haupt- und Randstrahl einzeichnen
- [ ] Hauptebenen einzeichnen (auf Wunsch)
- [ ] EP/AP einzeichnen (auf Wunsch)
- [ ] Strahlen in unterschiedlichen Farben darstellen
- [x] Kommentare erweitern, sodass bspw. *help(rt.calcBFL)* hilfreich ist
- [ ] Spiegel implementieren

Damit wir Kekse bekommen:
- [ ] GUI
  - Tkinter?
  - Browserbasiert/Webserver?
  - Drag'n'Drop von Elementen in optisches System (anstelle von Tabelle)
  - Glasdatenbank?
  - Linsen abspeichern?
  
  
## To-Do
- [ ] Vorzeichenkonvention beim Rückwärtsrechnen beachten (ffl, dEP positiv)  
    - beim Rückwärtsrechnen werden die Vorzeichen aller Abstände umgedreht
# RayTracing
## Benutzung
Bsp.: `python raytracing.py OpticalSystems/Uebung.txt`

## Ziele
Berechnungen:
- [x] Bild: Lage und Höhe
- [x] Austrittspupille: Lage und Größe
- [x] Eintrittspupille: Lage und Größe
- [ ] objektiv- und bildseitige Numerische Apertur
- [x] Haupt- und Randstrahl
- [x] effective, front und back focal length (efl, ffl, bfl)
- [ ] f-Zahl
- [ ] Lage Hauptebenen
- [ ] Abbildungsverhältnis
- [ ] (wenn frühzeitig fertig: Seidelaberrationen)

Exceptions abfangen:
- [ ] R = 0 -> Fehlerausgabe sowie R = infty
- [ ] Werte und Datentypen in optischem System prüfen
- [ ] optisches System darf nur ein *Stop* besitzen
- [ ] optisches System darf nur ein *Objekt* besitzen
- [ ] optisches System darf nur aus folgenden Typen bestehen: O (Object), L (Lens), S (Stop), I (Image)

Verschönerungen:
- [x] Objekt(-ebene) einzeichnen
- [x] Bild(-ebene) einzeichnen
- [ ] Haupt- und Randstrahl einzeichnen
- [ ] Hauptebenen einzeichnen (auf Wunsch)
- [ ] EP/AP einzeichnen (auf Wunsch)
- [ ] Strahlen in unterschiedlichen Farben darstellen
- [ ] Kommentare erweitern, sodass bspw. *help(rt.calcBFL)* hilfreich ist

Damit wir Kekse bekommen:
- [ ] GUI
  - Tkinter?
  - Browserbasiert/Webserver?
  - Drag'n'Drop von Elementen in optisches System (anstelle von Tabelle)
  - Glasdatenbank?
  - Linsen abspeichern?
  
  
## To-Do
- [x] Richtung für Strahlen angeben bei calcYNU
  - dadurch sollen Vorzeichen von Brechungsindex und Krümmungsradien gedreht werden und die Abstände von hinten kommend passen
- [x] Strahl bis zum Bild darstellen
  - erst Position des Bildes berechnen und dann *table* um Bildebene erweitern
  

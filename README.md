# RayTracing
## Benutzung
Bsp.: `python raytracing.py OpticalSystems/Uebung.txt`

## Ziele
Berechnungen:
- [ ] Bild: Lage und Höhe
- [x] Austrittspupille: Lage und Größe
- [ ] Eintrittspupille: Lage und Größe
- [ ] objektiv- und bildseitige Numerische Apertur
- [ ] Haupt- und Randstrahl
- [ ] effective, front und back focal length (efl, ffl, bfl)
- [ ] f-Zahl
- [ ] Lage Hauptebenen

Exceptions abfangen:
- [ ] R = 0 -> Fehlerausgabe sowie R = infty
- [ ] Werte und Datentypen in optischem System prüfen
- [ ] optisches System darf nur ein *Stop* besitzen
- [ ] optisches System darf nur ein *Objekt* besitzen
- [ ] optisches System darf nur aus folgenden Typen bestehen: O (Object), L (Lens), S (Stop), I (Image)

Verschönerungen:
- [x] Objekt(-ebene) einzeichnen
- [ ] Bild(-ebene) einzeichnen
- [ ] Haupt- und Randstrahl einzeichnen
- [ ] Hauptebenen einzeichnen (auf Wunsch)
- [ ] EP/AP einzeichnen (auf Wunsch)

Damit wir Kekse bekommen:
- [ ] GUI
  - Tkinter?
  - Browserbasiert/Webserver?
  - Drag'n'Drop von Elementen in optisches System (anstelle von Tabelle)
  
  
## To-Do
- [ ] Richtung für Strahlen angeben bei calcYNU
  - dadurch sollen Vorzeichen von Brechungsindex und Krümmungsradien gedreht werden und die Abstände von hinten kommend passen
- [ ] Strahl bis zum Bild darstellen
  - erst Position des Bildes berechnen und dann *table* um Bildebene erweitern
  

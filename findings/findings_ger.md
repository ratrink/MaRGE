# Erkenntnisse vom 26.11.2024

## Zusammenfassung der Tests

Während der Tests der Gradienten ist uns aufgefallen, dass diese den Gradientenverstärker sofort an seine Grenzen bringen und dabei ein erhebliches Offset erzeugen. Trotz verschiedener Shimming-Sequenzen und manuellem Shimming war es nicht möglich, dieses Problem vollständig zu beheben.

Unsere weiteren Tests ergaben, dass die DACs beim Aktivieren der Verstärker ein Offset einschalten. 


## Änderungen an `grad_board.py`

Die Einstellung der DAC-Werte erfolgt in der Datei `grad_board.py` ab Zeile 105. Dabei zeigte sich, dass es vorteilhaft ist, die Reihenfolge der Befehle zu ändern:
- **Vorher:** Verstärker einschalten und danach Outputs auf 0 setzen.  
- **Nachher:** Zuerst Outputs auf 0 setzen, dann Verstärker einschalten.  

Wir haben daher Zeile 110 mit Zeile 109 getauscht.  

Die Befehle adressieren im Hexadezimalsystem die einzelnen Register der DACs. Weitere Details dazu finden sich im Datenblatt der DACs ([Datenblatt](https://www.analog.com/media/en/technical-documentation/data-sheets/AD5781.pdf), ab Seite 19)



Das Offset entsteht erst beim letzten Befehl (`0x07200002`), zuvor bleibt das System perfekt auf 0. Ohne diesen Befehl lassen sich jedoch weder über `examples.py` noch über `MaRGE` Gradienten erzeugen.  

Nachdem wir diesen Offset manuell angepasst haben (z. B. durch Setzen auf 200 statt 0 → `0x04100200`), konnten wir eine Verbesserung feststellen. Allerdings trat das Offset erneut auf, sobald ein Gradienten aktiviert wurde.

## Hardware-Änderung: Spannungsteiler

Um das Offset zu reduzieren, haben wir einen 10:1-Spannungsteiler eingebaut. Gleichzeitig haben wir im Konfigurationsfile von MaRGE (`hw_config.py`) die Gradientenverstärkung (`gFactor`) um den Faktor 10 angepasst. Dadurch wurden die bisherigen Ergebnisse beibehalten.  
- Beispiel:  
  - **Vorher:** `gFactor` = 0.05  
  - **Nachher:** `gFactor` = 0.005  
  - Ähnliche Anpassung für andere Werte (z. B. 0.035 → 0.0035).

## Finales Konfigurationsfile

Das Konfigurationsfile (`hw_config.py`) sieht nun wie folgt aus:  
[hw_config.py](./hw_config.py)

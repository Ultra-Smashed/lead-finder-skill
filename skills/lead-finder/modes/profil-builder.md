# Baustein 2: Profil-Builder

Ziel: Aus jedem Fund wird ein Lead-Profil, mit dem man eine Nachricht schreiben kann, die klingt, als hätte man der Person zugehört.

## Pro Lead

1. **Profil öffnen** (Profil-URL, Bio, Link in der Bio, die letzten Beiträge). Ergänzen: echter Name, Firma, Rolle, Website, Ort, Follower.
2. **Drei Felder füllen, jeweils wörtlich aus Beiträgen, Kommentaren oder Bio:**
   - `problem`: was nervt, kostet, nicht klappt. Beispiel: „Catering-Anfragen gehen bei mir ständig in den DMs unter“
   - `wunsch`: Ziel, Traum, was sie erreichen wollen. Beispiel: „Ziel dieses Jahr: jedes Wochenende ausgebucht“
   - `einwand`: schlechte Erfahrung, Bedenken, Grund, warum sie bisher nicht gekauft haben. Beispiel: „Jede Agentur, die wir probiert haben, hat unser Essen nie verstanden“
   Fehlt eines, bleibt das Feld leer. Nicht aus dem Problem einen Wunsch ableiten und als Zitat ausgeben.
3. **Kaufsignal:** `ja`, wenn die Person aktiv nach einer Lösung sucht, gerade wächst, einstellt oder eine Lösung vergleicht. Sonst `nein`.
4. **Entscheider?** In `rolle` festhalten. Bei Firmenseiten die Person dahinter suchen (Impressum, Team-Seite, LinkedIn).

Hat ein Lead mehrere passende Zitate, das stärkste nach `problem`, ein zweites nach `wunsch` oder `einwand`.

## Viele Leads

Ab 30 Leads in Paketen zu 20 arbeiten und nach jedem Paket die Datei speichern. In Claude Code dürfen Unteragenten parallel je ein Paket bearbeiten, wenn das Werkzeug dafür da ist.

Danach: `python3 scripts/leads.py score leads.csv` und eine Zeile mit der Verteilung (über 70, 40–70, unter 40).

## Ausgabe im Chat

Die besten fünf als Karten:

```
Marco Ruiz · Marco's Kitchen · Instagram · Score 90
PROBLEM   „Catering-Anfragen gehen bei mir ständig in den DMs unter“
WUNSCH    „jedes Wochenende ausgebucht“
EINWAND   „jede Agentur, die wir probiert haben, hat unser Essen nie verstanden“
KONTAKT   marco@marcoskitchen.de (Impressum)
```

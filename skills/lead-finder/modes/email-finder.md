# Baustein 3: E-Mail-Finder

Ziel: zu jedem Lead die Adresse, unter der die Person wirklich erreichbar ist. Persönliche Adresse vor Sammeladresse.

## Reihenfolge der Quellen

1. **Profil und Bio:** E-Mail-Knopf, Adresse in der Bio, Link-in-Bio-Seite (Linktree und Co.).
2. **Website aus dem Profil:** Startseite, `/impressum`, `/kontakt`, `/contact`, `/about`, `/ueber-uns`, `/team`, `/imprint`, `/legal`. In Deutschland, Österreich und der Schweiz steht im Impressum fast immer eine Adresse.
3. **Muster:** Ist nur eine Sammeladresse (`info@`, `hallo@`, `kontakt@`) da, aber der Name der Person bekannt, die üblichen Muster bilden (`vorname@`, `vorname.nachname@`, `v.nachname@`) und als `geraten` markieren. Die Sammeladresse bleibt als Ersatz in der Zeile.
4. **Nichts gefunden:** `email_status = keine`, `kanal = dm`. Der Sender schreibt dann eine Direktnachricht statt einer Mail.

## Mit Skript (Claude Code oder Code-Ausführung mit Netz)

```bash
python3 scripts/find_email.py --csv leads.csv            # alle Zeilen mit Website, ohne E-Mail
python3 scripts/find_email.py --domain marcoskitchen.de --name "Marco Ruiz"
```

Das Skript ruft die Seiten oben ab, entschleiert Schreibweisen wie `name [at] firma [punkt] de`, bevorzugt persönliche Adressen, prüft per DNS, ob die Domain Mails annimmt (MX-Eintrag), und schreibt `email`, `email_quelle`, `email_status` in die CSV.

## Ohne Skript (Claude-App)

Dieselben Seiten mit dem Seitenabruf öffnen und die Adresse herausziehen. Bis zu 10 Abrufe parallel.

## Danach

Eine Zeile: „E-Mail gefunden: 96 · geraten: 21 · keine: 31 (gehen als DM)“. Dann `leads.py score` neu laufen lassen, weil der Kontakt in den Score eingeht.

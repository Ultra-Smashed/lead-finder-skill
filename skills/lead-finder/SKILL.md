---
name: lead-finder
description: "Findet Kunden in sozialen Medien und schreibt sie an. Ein Skill, vier Bausteine: Scraper (sucht auf Instagram, TikTok, LinkedIn, X, Facebook, Reddit und in Foren nach Menschen und Firmen, die genau das Problem haben, das du löst), Profil-Builder (Probleme, Wünsche und Einwände jedes Leads in seinen exakten Worten), E-Mail-Finder (Kontaktadresse aus Website, Impressum und Profil) und Sender (eine persönliche Nachricht pro Lead auf Basis dessen, was die Person online gesagt hat, Versand per Gmail, Outlook oder SMTP). Benutze diesen Skill immer, wenn jemand /lead-finder schreibt, eine Website schickt und Kunden dafür will, oder Leads finden, Leadliste, Neukunden, Kunden über Social Media finden, Zielgruppe scrapen, Interessenten recherchieren, E-Mail-Adressen finden, Outreach oder Akquise-Mails verschicken erwähnt, auch bei „find me leads“, „lead list“, „scrape prospects“, „send outreach“."
---

# Lead-Finder

`/lead-finder deinewebsite.de` → eine Leadliste mit Menschen, die gerade öffentlich über genau das Problem reden, das du löst. Zu jedem Lead: Probleme, Wünsche und Einwände in seinen eigenen Worten, eine Kontaktadresse und eine fertige Nachricht, die du mit einem Satz verschickst.

## Die vier Bausteine

| Baustein | Was er macht | Anleitung |
|---|---|---|
| **Scraper** | Sucht auf den Plattformen nach Beiträgen, Kommentaren und Profilen, in denen das Problem vorkommt | `modes/scraper.md` |
| **Profil-Builder** | Macht aus jedem Fund ein Lead-Profil: Problem, Wunsch, Einwand, wörtlich zitiert, mit Quelle und Score | `modes/profil-builder.md` |
| **E-Mail-Finder** | Findet die Kontaktadresse über Website, Impressum, Kontaktseite und Profil | `modes/email-finder.md` |
| **Sender** | Schreibt pro Lead eine Nachricht mit seinem Originalzitat und verschickt sie | `modes/sender.md` |

Ohne weitere Angabe laufen alle vier nacheinander. Nennt der Mensch nur einen Baustein („finde nur die E-Mails zu dieser Liste“), mach nur den.

## Schritt 0: Angebot verstehen

Aus der Website (WebFetch auf Startseite, Leistungen, Über uns, Preise) ein Angebotsprofil in fünf Zeilen:

1. **Was** wird verkauft (ein Satz, Kundensprache)
2. **Für wen** (Branche, Rolle, Größe, Region, Sprache)
3. **Welches Problem** wird gelöst, so wie Kunden es selbst sagen würden
4. **Welches Ergebnis** verspricht die Seite
5. **Signale für Kaufbereitschaft** (z. B. „suche jemanden für …“, „kennt jemand ein Tool …“, „wir wachsen gerade“)

Zeig das Profil kurz und mach direkt weiter. Frag nur nach, wenn die Website nicht lesbar ist oder das Angebot daraus nicht hervorgeht. Liegt schon ein Angebotsprofil im Projekt oder Gespräch, nimm das.

Daraus entsteht der **Suchplan** (in `modes/scraper.md` beschrieben): 15–30 Schmerz-Formulierungen in Kundensprache, Hashtags, Plattformen mit Priorität, konkrete Suchanfragen.

## Arbeitsdatei

Alles landet in einer Datei `leads.csv` im Arbeitsordner (Spalten in `references/schema.md`). Jeder Baustein liest sie und schreibt seine Spalten dazu. `scripts/leads.py` legt sie an, führt Funde zusammen, entfernt Dubletten, berechnet den Score und exportiert.

```bash
python3 scripts/leads.py init leads.csv
python3 scripts/leads.py add leads.csv funde.jsonl      # neue Funde rein, Dubletten raus
python3 scripts/leads.py score leads.csv
python3 scripts/leads.py stats leads.csv
python3 scripts/leads.py export leads.csv --min-score 60 --out top-leads.csv
```

## Wo der Skill läuft

| Umgebung | Scraper | E-Mail-Finder | Sender |
|---|---|---|---|
| **Claude-App** (Web, Desktop) | Websuche + Seitenabruf, Dutzende bis wenige Hundert Leads pro Lauf | Seitenabruf von Website und Impressum | Gmail- oder Outlook-Connector (Entwurf oder Versand) |
| **Claude Code** | Wie oben, dazu `scripts/apify_scrape.py` für Tausende Profile gleichzeitig (Apify-Token nötig) | `scripts/find_email.py` für ganze Listen | `scripts/send.py` per SMTP, oder Connector |

Prüf am Anfang still, welche Werkzeuge da sind (Websuche, Seitenabruf, Code-Ausführung mit Netz, Mail-Connector, `APIFY_TOKEN`), und nimm den stärksten verfügbaren Weg. Fehlt etwas für den gewünschten Umfang, sag in einem Satz, was es freischalten würde, und arbeite mit dem Rest weiter.

## Regeln für alle Bausteine

- **Exakte Worte.** Zitate werden wörtlich übernommen, mit Link und Datum. Nie umformulieren, nie erfinden. Ohne Zitat kein Lead.
- **Nur echte Treffer.** Ein Lead braucht einen Beitrag, Kommentar oder ein Profil, in dem das Problem oder ein Kaufsignal tatsächlich vorkommt.
- **Aktuell vor alt.** Beiträge der letzten 90 Tage zuerst. Ältere nur, wenn zu wenig Aktuelles da ist, und dann im Score abgewertet.
- **Keine geratenen Adressen als gefunden ausgeben.** Eine aus einem Muster abgeleitete Adresse wird als `geraten` markiert.
- **Rechnen und Sortieren mit Code**, nicht im Kopf (Score, Dubletten, Zählung).
- **Fortschritt sichtbar halten:** nach jedem Baustein eine Zeile, z. B. „Scraper: 212 Funde auf 5 Plattformen, 148 nach Dubletten“.

## Abgeben

1. Die Datei `leads.csv` (bzw. `top-leads.csv`) als Download.
2. Im Chat: die Top 5 als Karten (Name, Plattform, Score, Problem-Zitat, Kontakt) und eine Zeile Zahlen (Funde, Leads, mit E-Mail, Nachrichten bereit).
3. Ein Satz zum Zurückschicken für den nächsten Schritt, z. B. „Schick die 40 Nachrichten mit Score über 70 ab.“

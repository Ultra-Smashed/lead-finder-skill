# Arbeitsdatei leads.csv

Eine Zeile pro Lead. Trennzeichen Komma, UTF-8, erste Zeile Spaltennamen. `scripts/leads.py init` legt die Datei mit diesen Spalten an.

| Spalte | Baustein | Inhalt |
|---|---|---|
| `id` | Scraper | Fortlaufend, vergibt `leads.py` |
| `plattform` | Scraper | instagram, tiktok, linkedin, x, facebook, reddit, forum, web |
| `handle` | Scraper | Benutzername ohne @ |
| `name` | Scraper / Profil | Anzeigename oder echter Name |
| `firma` | Profil | Firma oder Projekt, falls erkennbar |
| `rolle` | Profil | Inhaberin, Geschäftsführer, Marketing … |
| `profil_url` | Scraper | Link zum Profil |
| `website` | Profil | Website aus Bio oder Profil |
| `beitrag_url` | Scraper | Link zum Beitrag oder Kommentar mit dem Zitat |
| `datum` | Scraper | Datum des Beitrags, JJJJ-MM-TT |
| `zitat` | Scraper | Der Satz, um den es geht, wörtlich |
| `problem` | Profil | Problem in seinen exakten Worten |
| `wunsch` | Profil | Wunsch oder Ziel in seinen exakten Worten |
| `einwand` | Profil | Einwand, schlechte Erfahrung oder Bedenken, wörtlich |
| `kaufsignal` | Profil | ja / nein, mit Satz („suche jemanden für …“) |
| `follower` | Scraper | Zahl, falls bekannt |
| `score` | `leads.py score` | 0–100 |
| `email` | E-Mail-Finder | Adresse |
| `email_quelle` | E-Mail-Finder | impressum, kontakt, profil, website, muster |
| `email_status` | E-Mail-Finder | gefunden, geraten, keine |
| `betreff` | Sender | Betreff der Nachricht |
| `nachricht` | Sender | Text der Nachricht |
| `kanal` | Sender | email, dm |
| `status` | Sender | neu, entwurf, gesendet, fehler, antwort |
| `gesendet_am` | Sender | Zeitstempel |

## Score (rechnet `leads.py score`)

| Teil | Punkte |
|---|---|
| Problem-Zitat vorhanden | 30 |
| Kaufsignal | 20 |
| Wunsch oder Einwand vorhanden | 10 |
| Beitrag jünger als 30 Tage / 90 Tage / älter | 20 / 10 / 0 |
| Kontakt: E-Mail gefunden / geraten / keine | 20 / 8 / 0 |

## Fundformat für `leads.py add`

Eine JSON-Zeile pro Fund (JSONL). Nur `plattform` und `zitat` sind Pflicht, alle anderen Spalten von oben dürfen mit:

```json
{"plattform": "instagram", "handle": "marcos.kitchen", "name": "Marco Ruiz", "profil_url": "https://instagram.com/marcos.kitchen", "beitrag_url": "https://instagram.com/p/xyz", "datum": "2026-11-12", "zitat": "Catering-Anfragen gehen bei mir ständig in den DMs unter"}
```

Dubletten erkennt `leads.py` über Plattform + Handle, ersatzweise über die Beitrags-URL. Bei einer Dublette werden leere Felder ergänzt, vorhandene nicht überschrieben.

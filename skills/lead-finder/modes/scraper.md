# Baustein 1: Scraper

Ziel: möglichst viele echte Funde, in denen Menschen das Problem aus dem Angebotsprofil in eigenen Worten beschreiben oder etwas suchen, das der Mensch anbietet.

## 1. Suchplan bauen

Aus dem Angebotsprofil (Schritt 0 in `SKILL.md`):

- **Schmerz-Formulierungen (15–30):** so, wie Kunden reden, nicht wie Anbieter. Nicht „Lead-Management“, sondern „Anfragen gehen in den DMs unter“, „komme nicht hinterher mit Nachrichten“, „verliere ständig Aufträge“. In der Sprache der Zielgruppe (deutsch und, wenn passend, englisch).
- **Kaufsignale (5–10):** „suche jemanden für …“, „kann jemand … empfehlen“, „welches Tool für …“, „hat jemand Erfahrung mit …“, „wir stellen ein: …“.
- **Hashtags (10–20)** für Instagram und TikTok, aus Branche und Problem.
- **Plattform-Priorität:** B2B-Angebote → LinkedIn, X, Reddit, Foren zuerst. Lokale Betriebe, Gastro, Handwerk, Beauty, Coaching → Instagram, TikTok, Facebook-Gruppen zuerst.
- **Konkurrenz-Anker:** Kommentare unter Beiträgen von Wettbewerbern und unter Beschwerden über Wettbewerber („nie wieder Agentur X“) sind die besten Einwand-Quellen.

Zeig den Suchplan in einer kurzen Tabelle und leg los.

## 2. Suchen

### Weg A: Websuche (überall verfügbar)

Suchanfragen pro Plattform mit `site:` kombinieren, jeweils mit einer Schmerz-Formulierung oder einem Kaufsignal:

```
site:instagram.com "Anfragen gehen unter" catering
site:linkedin.com/posts "suche eine Agentur" social media
site:reddit.com "kann jemand empfehlen" buchhaltung selbstständig
site:x.com "komme nicht hinterher" DMs
site:tiktok.com "kunden finden" friseur
site:facebook.com/groups "suche jemanden" website
```

Pro Treffer die Seite abrufen (WebFetch), das Zitat wörtlich herausziehen, Handle, Profil-Link, Datum notieren. Seiten, die sich ohne Anmeldung nicht öffnen, mit dem Text aus dem Suchergebnis aufnehmen und `datum` leer lassen.

Ziel pro Lauf in der Claude-App: so lange suchen, bis 50 brauchbare Funde da sind oder alle Suchanfragen abgearbeitet sind. Suchanfragen parallel schicken, wo es geht.

### Weg B: Apify (Claude Code, Tausende Profile)

Ist `APIFY_TOKEN` gesetzt und Code-Ausführung mit Netz da, nimm `scripts/apify_scrape.py`. Es startet die Scraper für jede Plattform mit den Hashtags und Suchbegriffen aus dem Suchplan und schreibt alle Funde normalisiert als JSONL:

```bash
python3 scripts/apify_scrape.py --plan suchplan.json --out funde.jsonl --limit 500
```

`suchplan.json` sieht so aus:

```json
{
  "instagram_hashtags": ["catering", "eventcatering"],
  "tiktok_suche": ["catering anfragen", "dms chaos"],
  "x_suche": ["\"komme nicht hinterher\" DMs"],
  "linkedin_suche": ["suche Agentur Social Media"],
  "reddit_suche": ["catering anfragen verwalten"],
  "filter": ["anfrage", "dm", "nachricht", "unter"]
}
```

`filter` sind Wortstämme. Nur Funde, deren Text mindestens einen davon enthält, kommen in die Datei. So bleiben aus Tausenden Beiträgen die übrig, in denen das Problem wirklich vorkommt. Danach liest Claude die gefilterten Funde und übernimmt nur die, in denen das Problem tatsächlich gemeint ist.

Ohne Token: Weg A, und einmal sagen, dass ein Apify-Token (apify.com, kostenloses Kontingent) den Umfang auf Tausende Profile erhöht.

## 3. Übernehmen

Funde als JSONL (Format in `references/schema.md`) speichern und mit `python3 scripts/leads.py add leads.csv funde.jsonl` in die Arbeitsdatei holen. Danach eine Zeile: Funde, Plattformen, Leads nach Dubletten.

## Qualität

- Ein Fund ohne wörtliches Zitat wird nicht übernommen.
- Anbieter, die selbst dieselbe Leistung verkaufen, aussortieren (außer der Mensch sucht Partner).
- Bots, Gewinnspiel-Kommentare und reine Emoji-Kommentare aussortieren.

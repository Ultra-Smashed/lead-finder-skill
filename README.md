# Lead-Finder-Skill

Ein Skill für Claude. Du gibst `/lead-finder` und deine Website ein, und Claude sucht auf Instagram, TikTok, LinkedIn, X, Facebook und Reddit nach Menschen, die gerade öffentlich über genau das Problem reden, das du löst. Zu jedem Lead bekommst du Probleme, Wünsche und Einwände in seinen exakten Worten, eine Kontaktadresse und eine fertige Nachricht, die mit seinem eigenen Zitat beginnt. Auf dein Okay verschickt Claude die Nachrichten. Kostenlos, MIT-Lizenz.

| Baustein | Was er macht |
| --- | --- |
| **Scraper** | Baut aus deiner Website einen Suchplan (Schmerz-Formulierungen, Kaufsignale, Hashtags) und sucht damit auf allen Plattformen. Mit Apify-Token in Claude Code: Tausende Beiträge pro Lauf. |
| **Profil-Builder** | Macht aus jedem Fund ein Profil: Problem, Wunsch, Einwand, jeweils wörtlich, mit Link und Datum, plus Score von 0 bis 100. |
| **E-Mail-Finder** | Findet die Adresse über Bio, Website, Impressum und Kontaktseite. Persönliche Adresse vor info@. |
| **Sender** | Schreibt pro Lead eine Nachricht mit seinem Originalzitat und verschickt sie per Gmail, Outlook oder SMTP. DMs kommen als Liste zum Kopieren. |

## Installation

### Claude-App (Web, Desktop)

Am schnellsten: den Link in einen neuen Chat einfügen und Claude bitten, den Skill zu installieren:

```
https://github.com/Ultra-Smashed/lead-finder-skill

Installier diesen Skill für mich.
```

Oder von Hand:

1. [`lead-finder.zip`](https://github.com/Ultra-Smashed/lead-finder-skill/raw/main/lead-finder.zip) herunterladen (nicht entpacken).
2. In Claude unter **Settings → Capabilities** den Schalter **Code execution and file creation** einschalten. In der neueren Ansicht heißt er **Create and edit files**.
3. **Customize → Skills** öffnen, auf **+** klicken, dann **Create skill → Upload a skill** und die ZIP-Datei wählen.

Für den Versand in der App den **Gmail**- oder **Outlook**-Connector verbinden.

### Claude Code

Als Plugin:

```
/plugin marketplace add Ultra-Smashed/lead-finder-skill
/plugin install lead-finder@lead-finder
```

Oder den Ordner kopieren:

```bash
git clone https://github.com/Ultra-Smashed/lead-finder-skill.git
cp -r lead-finder-skill/skills/lead-finder ~/.claude/skills/
```

Optional für mehr Umfang und direkten Versand, als Umgebungsvariablen oder in einer `.env` im Arbeitsordner:

```
APIFY_TOKEN=...            # apify.com, für Tausende Beiträge pro Lauf
SMTP_HOST=smtp.dein-anbieter.de
SMTP_PORT=587
SMTP_USER=du@deinefirma.de
SMTP_PASS=...
FROM_EMAIL=du@deinefirma.de
FROM_NAME=Dein Name
```

## Benutzen

```
/lead-finder deinewebsite.de
```

Oder in eigenen Worten:

> Finde mir 100 Leads für mein Catering in Köln und schreib ihnen.

> Hier ist meine Leadliste. Such nur die E-Mail-Adressen raus.

> Schick alle Nachrichten mit Score über 70 ab.

Alles landet in einer Datei `leads.csv`, die du jederzeit öffnen, filtern und weitergeben kannst.

## Dateien

```
skills/lead-finder/SKILL.md          Ablauf, Bausteine, Regeln
skills/lead-finder/modes/            eine Anleitung pro Baustein
skills/lead-finder/references/       Spalten der leads.csv und Score
skills/lead-finder/scripts/          Hilfsskripte (Python 3, ohne Zusatzpakete)
lead-finder.zip                      derselbe Skill-Ordner als ZIP für die Claude-App
.claude-plugin/                      plugin.json, marketplace.json
```

Nach einer Änderung im Skill-Ordner die ZIP neu bauen: `cd skills && zip -r ../lead-finder.zip lead-finder`.

Anleitung: [thanisch.co/wissen/guides/lead-finder-skill-claude](https://thanisch.co/wissen/guides/lead-finder-skill-claude)

MIT-Lizenz, siehe [LICENSE](LICENSE). Von [Christopher Thanisch](https://thanisch.co).

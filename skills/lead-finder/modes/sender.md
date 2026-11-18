# Baustein 4: Sender

Ziel: Jede Nachricht beginnt mit dem, was die Person selbst gesagt hat. So liest sie sich wie eine Antwort, nicht wie Werbung.

## Absender klären (einmal)

Wenn nicht schon bekannt, in einer Nachricht fragen:
1. Name und Firma, die unterschreiben
2. Du oder Sie
3. Was soll die Person tun (kurzer Call, Antwort, Link anschauen)? Mit Link, falls vorhanden.
4. Ein echtes Ergebnis oder eine Referenz, falls vorhanden (sonst ohne)

## Nachricht pro Lead

Aufbau, 50–90 Wörter:

1. **Anrede** mit Vorname, wenn bekannt.
2. **Ihr Zitat:** „Du hast geschrieben, dass [problem, wörtlich, gekürzt nur am Rand].“
3. **Die Brücke:** ein Satz, was der Absender genau dagegen tut, in ihren Worten. Gibt es einen Einwand, ihn direkt aufnehmen („Und ja, wir kommen nicht mit Standardvorlagen, …“).
4. **Kleine Frage:** „Lohnt sich ein kurzer Blick?“ oder „Soll ich dir zeigen, wie das bei dir aussähe?“
5. **Unterschrift.**

**Betreff:** höchstens sechs Wörter, aus ihrem Thema, z. B. „Deine Catering-Anfragen“ oder „Zu deinem Beitrag über DMs“.

**DM statt Mail** (kein Kontakt gefunden oder Plattform passt besser): dieselbe Nachricht, höchstens 300 Zeichen, ohne Betreff.

Beispiel:

> Betreff: Deine Catering-Anfragen
>
> Hi Marco,
> du hast geschrieben, dass Catering-Anfragen bei dir ständig in den DMs untergehen. Genau das lösen wir: Jede Anfrage landet automatisch in einer Liste mit Datum, Personenzahl und Budget, und du antwortest mit einem Klick. Kein Template-Kram, wir bauen das auf eure Abläufe. Lohnt sich ein kurzer Blick?
>
> Viele Grüße
> Lena

## Freigabe und Versand

1. Alle Nachrichten in die CSV schreiben (`betreff`, `nachricht`, `kanal`, `status = entwurf`) und die ersten fünf im Chat zeigen.
2. Der Mensch gibt frei, z. B. „Schick alle mit Score über 70“ oder „Schick alle“. Ohne diese Freigabe nichts versenden.
3. Versand über den stärksten verfügbaren Weg:
   - **Gmail- oder Outlook-Connector:** pro Lead eine Mail senden. Kann der Connector nur Entwürfe anlegen, Entwürfe anlegen und sagen, dass sie im Postfach bereitliegen.
   - **Claude Code / Code-Ausführung mit Netz:** `scripts/send.py` per SMTP:
     ```bash
     python3 scripts/send.py leads.csv --min-score 70 --send
     ```
     Zugangsdaten aus den Umgebungsvariablen `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `FROM_NAME`, `FROM_EMAIL`. Ohne `--send` zeigt das Skript nur, was rausgehen würde.
   - **DMs:** Claude kann keine DMs auf Instagram, TikTok oder LinkedIn absetzen. Die DM-Texte als Liste mit Profil-Link ausgeben, zum Kopieren.
4. Nach dem Versand `status = gesendet` und `gesendet_am` setzen, Fehler mit `status = fehler`.

## Tempo

Damit das Postfach nicht als Spam eingestuft wird: `send.py` schickt standardmäßig höchstens 50 Mails am Tag mit 45–120 Sekunden Abstand (`--per-day`, `--min-wait`, `--max-wait` ändern das). Bei neuen Postfächern mit 20 am Tag anfangen.

## Nachfassen

Auf Wunsch nach 3 und 7 Tagen je eine kurze Nachfass-Mail an alle mit `status = gesendet` ohne Antwort, jeweils mit einem neuen Bezug zu ihrem Zitat statt „wollte nur nachhaken“.

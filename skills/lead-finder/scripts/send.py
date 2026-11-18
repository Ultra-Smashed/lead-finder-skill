#!/usr/bin/env python3
"""Nachrichten aus leads.csv per SMTP verschicken. Python 3, ohne Zusatzpakete.

  python3 send.py leads.csv                       # Vorschau, nichts wird verschickt
  python3 send.py leads.csv --min-score 70 --send # verschicken

Zugangsdaten aus Umgebungsvariablen (oder einer Datei .env im Arbeitsordner):
  SMTP_HOST, SMTP_PORT (587 = STARTTLS, 465 = SSL), SMTP_USER, SMTP_PASS, FROM_EMAIL, FROM_NAME

Verschickt nur Zeilen mit kanal = email (oder leer), einer E-Mail, Betreff, Nachricht
und status entwurf oder neu. Setzt danach status = gesendet bzw. fehler.
"""
import argparse
import csv
import os
import random
import smtplib
import ssl
import sys
import time
from datetime import datetime
from email.message import EmailMessage
from email.utils import formataddr, make_msgid


def lade_env(pfad=".env"):
    if not os.path.exists(pfad):
        return
    for zeile in open(pfad, encoding="utf-8"):
        zeile = zeile.strip()
        if zeile and not zeile.startswith("#") and "=" in zeile:
            k, v = zeile.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def speichern(pfad, rows, felder):
    tmp = pfad + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=felder)
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, pfad)


def verbinden():
    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT", "587"))
    ctx = ssl.create_default_context()
    s = smtplib.SMTP_SSL(host, port, context=ctx, timeout=30) if port == 465 else smtplib.SMTP(host, port, timeout=30)
    if port != 465:
        s.starttls(context=ctx)
    s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
    return s


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--send", action="store_true", help="wirklich verschicken (sonst nur Vorschau)")
    p.add_argument("--min-score", type=int, default=0)
    p.add_argument("--per-day", type=int, default=50, help="höchstens so viele in diesem Lauf")
    p.add_argument("--min-wait", type=int, default=45, help="Sekunden zwischen zwei Mails, mindestens")
    p.add_argument("--max-wait", type=int, default=120, help="Sekunden zwischen zwei Mails, höchstens")
    a = p.parse_args()
    lade_env()

    with open(a.csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    felder = list(rows[0].keys()) if rows else []
    for extra in ("status", "gesendet_am"):
        if extra not in felder:
            felder.append(extra)

    offen = [r for r in rows
             if (r.get("kanal") or "email") == "email"
             and r.get("email") and r.get("betreff") and r.get("nachricht")
             and (r.get("status") or "neu") in ("neu", "entwurf")
             and int(r.get("score") or 0) >= a.min_score][: a.per_day]

    if not a.send:
        for r in offen[:5]:
            print(f"An: {r['email']}\nBetreff: {r['betreff']}\n\n{r['nachricht']}\n{'-' * 60}")
        print(f"Vorschau: {len(offen)} Mails würden verschickt. Zum Senden --send anhängen.")
        return

    fehlend = [k for k in ("SMTP_HOST", "SMTP_USER", "SMTP_PASS", "FROM_EMAIL") if not os.environ.get(k)]
    if fehlend:
        sys.exit("Es fehlen Zugangsdaten: " + ", ".join(fehlend))

    absender = formataddr((os.environ.get("FROM_NAME", ""), os.environ["FROM_EMAIL"]))
    server = verbinden()
    ok = fehler = 0
    for i, r in enumerate(offen):
        msg = EmailMessage()
        msg["From"] = absender
        msg["To"] = r["email"]
        msg["Subject"] = r["betreff"]
        msg["Message-ID"] = make_msgid(domain=os.environ["FROM_EMAIL"].split("@")[1])
        msg.set_content(r["nachricht"])
        try:
            server.send_message(msg)
            r["status"], r["gesendet_am"] = "gesendet", datetime.now().isoformat(timespec="seconds")
            ok += 1
            print(f"[{i + 1}/{len(offen)}] gesendet an {r['email']}", flush=True)
        except smtplib.SMTPServerDisconnected:
            server = verbinden()
            r["status"] = "fehler"
            fehler += 1
        except Exception as e:  # noqa: BLE001
            r["status"] = "fehler"
            fehler += 1
            print(f"[{i + 1}/{len(offen)}] Fehler bei {r['email']}: {e}", flush=True)
        speichern(a.csv, rows, felder)
        if i < len(offen) - 1:
            time.sleep(random.randint(a.min_wait, a.max_wait))
    server.quit()
    print(f"Gesendet: {ok} · Fehler: {fehler}")


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Arbeitsdatei leads.csv verwalten: anlegen, Funde zusammenführen, Score, Export.

Python 3, ohne Zusatzpakete.

  python3 leads.py init leads.csv
  python3 leads.py add leads.csv funde.jsonl
  python3 leads.py score leads.csv
  python3 leads.py stats leads.csv
  python3 leads.py export leads.csv --min-score 60 --out top-leads.csv
"""
import argparse
import csv
import json
import os
import sys
from datetime import date, datetime

COLUMNS = [
    "id", "plattform", "handle", "name", "firma", "rolle", "profil_url", "website",
    "beitrag_url", "datum", "zitat", "problem", "wunsch", "einwand", "kaufsignal",
    "follower", "score", "email", "email_quelle", "email_status", "betreff",
    "nachricht", "kanal", "status", "gesendet_am",
]


def read(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(path, rows):
    tmp = path + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLUMNS})
    os.replace(tmp, path)


def key(r):
    plattform = (r.get("plattform") or "").strip().lower()
    handle = (r.get("handle") or "").strip().lower().lstrip("@")
    if plattform and handle:
        return ("h", plattform, handle)
    url = (r.get("beitrag_url") or r.get("profil_url") or "").strip().lower().rstrip("/")
    return ("u", url) if url else ("z", (r.get("zitat") or "").strip().lower()[:120])


def cmd_init(a):
    if os.path.exists(a.csv) and read(a.csv):
        print(f"{a.csv} existiert schon, nichts geändert.")
        return
    write(a.csv, [])
    print(f"{a.csv} angelegt.")


def cmd_add(a):
    rows = read(a.csv)
    index = {key(r): r for r in rows}
    next_id = max([int(r["id"]) for r in rows if (r.get("id") or "").isdigit()] or [0]) + 1
    neu = dupl = ohne_zitat = 0
    with open(a.jsonl, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fund = json.loads(line)
            if not (fund.get("zitat") or "").strip():
                ohne_zitat += 1
                continue
            fund = {k: str(v) if v is not None else "" for k, v in fund.items()}
            if fund.get("handle"):
                fund["handle"] = fund["handle"].lstrip("@")
            k = key(fund)
            if k in index:
                vorhanden = index[k]
                for c in COLUMNS:
                    if not vorhanden.get(c) and fund.get(c):
                        vorhanden[c] = fund[c]
                dupl += 1
                continue
            fund["id"] = str(next_id)
            fund.setdefault("status", "neu")
            next_id += 1
            rows.append(fund)
            index[k] = fund
            neu += 1
    write(a.csv, rows)
    print(f"Neu: {neu} · Dubletten zusammengeführt: {dupl} · ohne Zitat verworfen: {ohne_zitat} · gesamt: {len(rows)}")


def alter_tage(d):
    try:
        return (date.today() - datetime.strptime(d[:10], "%Y-%m-%d").date()).days
    except (ValueError, TypeError):
        return None


def score(r):
    s = 0
    if (r.get("problem") or r.get("zitat") or "").strip():
        s += 30
    if (r.get("kaufsignal") or "").strip().lower().startswith("ja"):
        s += 20
    if (r.get("wunsch") or "").strip() or (r.get("einwand") or "").strip():
        s += 10
    t = alter_tage(r.get("datum") or "")
    if t is not None:
        s += 20 if t <= 30 else 10 if t <= 90 else 0
    st = (r.get("email_status") or "").strip().lower()
    s += 20 if st == "gefunden" else 8 if st == "geraten" else 0
    return s


def cmd_score(a):
    rows = read(a.csv)
    for r in rows:
        r["score"] = str(score(r))
    rows.sort(key=lambda r: -int(r["score"]))
    write(a.csv, rows)
    hoch = sum(1 for r in rows if int(r["score"]) > 70)
    mittel = sum(1 for r in rows if 40 <= int(r["score"]) <= 70)
    print(f"Score gesetzt für {len(rows)} Leads · über 70: {hoch} · 40–70: {mittel} · unter 40: {len(rows) - hoch - mittel}")


def cmd_stats(a):
    rows = read(a.csv)
    def zaehl(feld):
        out = {}
        for r in rows:
            v = (r.get(feld) or "-").strip() or "-"
            out[v] = out.get(v, 0) + 1
        return ", ".join(f"{k}: {v}" for k, v in sorted(out.items(), key=lambda x: -x[1]))
    print(f"Leads: {len(rows)}")
    print(f"Plattformen: {zaehl('plattform')}")
    print(f"E-Mail: {zaehl('email_status')}")
    print(f"Status: {zaehl('status')}")


def cmd_export(a):
    rows = [r for r in read(a.csv) if int(r.get("score") or 0) >= a.min_score]
    if a.status:
        rows = [r for r in rows if (r.get("status") or "") == a.status]
    write(a.out, rows)
    print(f"{len(rows)} Leads nach {a.out} exportiert.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("init"); s.add_argument("csv"); s.set_defaults(f=cmd_init)
    s = sub.add_parser("add"); s.add_argument("csv"); s.add_argument("jsonl"); s.set_defaults(f=cmd_add)
    s = sub.add_parser("score"); s.add_argument("csv"); s.set_defaults(f=cmd_score)
    s = sub.add_parser("stats"); s.add_argument("csv"); s.set_defaults(f=cmd_stats)
    s = sub.add_parser("export"); s.add_argument("csv"); s.add_argument("--min-score", type=int, default=0)
    s.add_argument("--status"); s.add_argument("--out", required=True); s.set_defaults(f=cmd_export)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    sys.exit(main())

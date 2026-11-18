#!/usr/bin/env python3
"""Kontaktadressen finden: Website, Impressum, Kontaktseite. Python 3, ohne Zusatzpakete.

  python3 find_email.py --domain marcoskitchen.de --name "Marco Ruiz"
  python3 find_email.py --csv leads.csv            # alle Zeilen mit Website und ohne E-Mail

Schreibt bei --csv die Spalten email, email_quelle, email_status zurück.
"""
import argparse
import csv
import html
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.request
from urllib.parse import urljoin, urlparse

PFADE = ["", "/impressum", "/kontakt", "/contact", "/imprint", "/legal", "/about",
         "/ueber-uns", "/uber-uns", "/team", "/impressum.html", "/kontakt.html"]
SAMMEL = {"info", "hallo", "hello", "kontakt", "contact", "office", "mail", "service",
          "support", "team", "buero", "post", "anfrage", "anfragen", "booking", "hi"}
UNSINN = ("example.", "sentry", "wixpress", "@2x", ".png", ".jpg", ".svg", ".webp", "domain.", "email.com")
MAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def hole(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "de,en"})
        with urllib.request.urlopen(req, timeout=12) as r:
            return r.read(800_000).decode(r.headers.get_content_charset() or "utf-8", "ignore")
    except Exception:
        return ""


def entschleiern(t):
    t = html.unescape(t)
    t = re.sub(r"\s*[\[\(\{]\s*(at|ät|@)\s*[\]\)\}]\s*", "@", t, flags=re.I)
    t = re.sub(r"\s+(at)\s+", "@", t)
    t = re.sub(r"\s*[\[\(\{]\s*(dot|punkt|\.)\s*[\]\)\}]\s*", ".", t, flags=re.I)
    return t


def adressen(text):
    out = []
    for m in MAIL_RE.findall(entschleiern(text)):
        m = m.strip(".").lower()
        if any(u in m for u in UNSINN):
            continue
        if m not in out:
            out.append(m)
    return out


def hat_mx(domain):
    tool = shutil.which("nslookup") or shutil.which("dig")
    if not tool:
        return None
    try:
        args = [tool, "-type=mx", domain] if tool.endswith("nslookup") else [tool, "+short", "MX", domain]
        out = subprocess.run(args, capture_output=True, text=True, timeout=8).stdout.lower()
        return ("mail exchanger" in out) or bool(out.strip() and tool.endswith("dig"))
    except Exception:
        return None


def ascii_name(s):
    s = s.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z\-]", "", s)


def muster(name, domain):
    teile = [ascii_name(t) for t in (name or "").split() if ascii_name(t)]
    if not teile:
        return []
    v, n = teile[0], teile[-1] if len(teile) > 1 else ""
    out = [f"{v}@{domain}"]
    if n:
        out += [f"{v}.{n}@{domain}", f"{v[0]}.{n}@{domain}", f"{v}{n}@{domain}"]
    return out


def suche(domain_oder_url, name=""):
    url = domain_oder_url if "://" in domain_oder_url else "https://" + domain_oder_url
    host = urlparse(url).netloc.lower()
    domain = host[4:] if host.startswith("www.") else host
    basis = f"{urlparse(url).scheme}://{host}"
    gefunden = {}
    for pfad in PFADE:
        seite = urljoin(basis, pfad) if pfad else url
        for a in adressen(hole(seite)):
            gefunden.setdefault(a, "impressum" if "impressum" in pfad or "imprint" in pfad or "legal" in pfad
                                else "kontakt" if "kont" in pfad or "contact" in pfad else "website")
        if len(gefunden) >= 6:
            break
    eigene = {a: q for a, q in gefunden.items() if a.split("@")[1].endswith(domain)} or gefunden
    vorname = ascii_name((name or " ").split()[0]) if name else ""
    def rang(a):
        lokal = a.split("@")[0]
        if vorname and vorname in lokal:
            return 0
        return 2 if lokal in SAMMEL else 1
    sortiert = sorted(eigene, key=rang)
    mx = hat_mx(domain)
    ergebnis = {"domain": domain, "mx": mx, "alle": sortiert}
    if sortiert and rang(sortiert[0]) < 2:
        ergebnis.update(email=sortiert[0], email_quelle=eigene[sortiert[0]], email_status="gefunden")
    elif name and mx is not False and muster(name, domain):
        geraten = muster(name, domain)[1 if len(muster(name, domain)) > 1 else 0]
        ergebnis.update(email=geraten, email_quelle="muster", email_status="geraten",
                        ersatz=sortiert[0] if sortiert else "")
    elif sortiert:
        ergebnis.update(email=sortiert[0], email_quelle=eigene[sortiert[0]], email_status="gefunden")
    else:
        ergebnis.update(email="", email_quelle="", email_status="keine")
    return ergebnis


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--domain")
    p.add_argument("--name", default="")
    p.add_argument("--csv")
    a = p.parse_args()
    if a.domain:
        print(json.dumps(suche(a.domain, a.name), ensure_ascii=False, indent=2))
        return
    if not a.csv:
        p.error("--domain oder --csv angeben")
    with open(a.csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        felder = rows[0].keys() if rows else []
    zaehl = {"gefunden": 0, "geraten": 0, "keine": 0}
    for r in rows:
        if r.get("email") or not r.get("website"):
            continue
        e = suche(r["website"], r.get("name", ""))
        r["email"], r["email_quelle"], r["email_status"] = e["email"], e["email_quelle"], e["email_status"]
        if e["email_status"] == "keine" and not r.get("kanal"):
            r["kanal"] = "dm"
        zaehl[e["email_status"]] += 1
        print(f"{r.get('name') or r.get('handle')}: {e['email'] or '-'} ({e['email_status']})", flush=True)
    tmp = a.csv + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(felder))
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, a.csv)
    print(f"E-Mail gefunden: {zaehl['gefunden']} · geraten: {zaehl['geraten']} · keine: {zaehl['keine']}")


if __name__ == "__main__":
    sys.exit(main())

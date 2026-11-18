#!/usr/bin/env python3
"""Tausende Beiträge über Apify holen und als Funde (JSONL) speichern. Python 3, ohne Zusatzpakete.

  export APIFY_TOKEN=...      (apify.com → Settings → Integrations)
  python3 apify_scrape.py --plan suchplan.json --out funde.jsonl --limit 500

suchplan.json: instagram_hashtags, tiktok_suche, x_suche, linkedin_suche, reddit_suche (Listen)
und filter (Wortstämme; nur Funde, deren Text einen davon enthält, werden gespeichert).

Die Actor-IDs unten sind die gängigen Scraper aus dem Apify Store. Wenn einer umbenannt wurde,
im Store suchen und hier ersetzen. Eingaben, die ein Actor nicht kennt, ignoriert er.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ACTORS = {
    "instagram": ("apify/instagram-hashtag-scraper", lambda q, n: {"hashtags": q, "resultsLimit": n}),
    "tiktok": ("clockworks/tiktok-scraper", lambda q, n: {"searchQueries": q, "resultsPerPage": n}),
    "x": ("apidojo/tweet-scraper", lambda q, n: {"searchTerms": q, "maxItems": n}),
    "linkedin": ("harvestapi/linkedin-post-search", lambda q, n: {"searchQueries": q, "maxPosts": n}),
    "reddit": ("trudax/reddit-scraper-lite", lambda q, n: {"searches": q, "maxItems": n}),
}
PLAN_KEYS = {"instagram": "instagram_hashtags", "tiktok": "tiktok_suche", "x": "x_suche",
             "linkedin": "linkedin_suche", "reddit": "reddit_suche"}


def lauf(actor, eingabe, token):
    url = (f"https://api.apify.com/v2/acts/{actor.replace('/', '~')}/run-sync-get-dataset-items?"
           + urllib.parse.urlencode({"token": token, "timeout": 280}))
    req = urllib.request.Request(url, data=json.dumps(eingabe).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read().decode())


def erst(d, *pfade):
    for pfad in pfade:
        v = d
        for teil in pfad.split("."):
            v = v.get(teil) if isinstance(v, dict) else None
        if v not in (None, "", []):
            return v
    return ""


def normal(plattform, it):
    text = erst(it, "caption", "text", "full_text", "fullText", "content", "body", "title", "description")
    handle = erst(it, "ownerUsername", "authorMeta.name", "author.userName", "author.username",
                  "author.publicIdentifier", "username", "user.screen_name")
    name = erst(it, "ownerFullName", "authorMeta.nickName", "author.name", "author.fullName", "user.name")
    datum = str(erst(it, "timestamp", "createTimeISO", "createdAt", "postedAt.date", "postedAt", "created_utc"))[:10]
    return {
        "plattform": plattform,
        "handle": str(handle).lstrip("@"),
        "name": name,
        "profil_url": erst(it, "ownerProfileUrl", "authorMeta.profileUrl", "author.url", "author.linkedinUrl", "authorUrl"),
        "beitrag_url": erst(it, "url", "webVideoUrl", "postUrl", "twitterUrl", "linkedinUrl", "link"),
        "datum": datum,
        "zitat": str(text).strip()[:600],
        "follower": erst(it, "ownerFollowersCount", "authorMeta.fans", "author.followers", "author.followersCount"),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--plan", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--limit", type=int, default=300, help="Ergebnisse pro Plattform")
    a = p.parse_args()
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("APIFY_TOKEN fehlt. Ohne Token den Scraper über die Websuche laufen lassen.")
    plan = json.load(open(a.plan, encoding="utf-8"))
    filt = [f.lower() for f in plan.get("filter", [])]

    jobs = {pl: plan[k] for pl, k in PLAN_KEYS.items() if plan.get(k)}

    def job(pl):
        actor, eingabe = ACTORS[pl]
        try:
            return pl, lauf(actor, eingabe(jobs[pl], a.limit), token), None
        except Exception as e:  # noqa: BLE001
            return pl, [], str(e)

    gesamt = behalten = 0
    with open(a.out, "a", encoding="utf-8") as out, ThreadPoolExecutor(max_workers=5) as ex:
        for pl, items, fehler in ex.map(job, jobs):
            if fehler:
                print(f"{pl}: Fehler ({fehler})", flush=True)
                continue
            n = 0
            for it in items if isinstance(items, list) else []:
                f = normal(pl, it)
                if not f["zitat"]:
                    continue
                if filt and not any(w in f["zitat"].lower() for w in filt):
                    continue
                out.write(json.dumps(f, ensure_ascii=False) + "\n")
                n += 1
            gesamt += len(items) if isinstance(items, list) else 0
            behalten += n
            print(f"{pl}: {len(items)} geholt, {n} passen zum Filter", flush=True)
    print(f"Gesamt: {gesamt} Beiträge geholt, {behalten} Funde nach {a.out}")


if __name__ == "__main__":
    sys.exit(main())

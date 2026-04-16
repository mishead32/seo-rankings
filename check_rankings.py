#!/usr/bin/env python3
"""
SEO Rank Checker — Google Custom Search API
FREE: 100 queries/day, resets every day forever — no credits, no limits
Checks website ranking on Google India for 3 brands
"""
import requests, json, os, time
from datetime import datetime, timezone, timedelta

GOOGLE_API_KEY = os.environ.get("GOOGLE_CSE_API_KEY", "").strip()
GOOGLE_CX      = os.environ.get("GOOGLE_CSE_CX", "").strip()

BRANDS = {
    "Bodyzone": {
        "website": "bodyzonegym.in",
        "color": "#2563eb",
        "keywords": [
            "Bodyzone Gym",
            "Body Zone Gym Chandigarh",
            "Best Gym In Chandigarh",
            "Body Zone Chandigarh",
            "Gym In Chandigarh",
            "Gym Chandigarh",
            "Gyms In Chandigarh",
            "Best Gyms In Chandigarh",
            "Premium Gym In Chandigarh",
            "Best Gym Chandigarh",
            "Chandigarh Gym",
            "Top gym in chandigarh",
            "Chandigarh Best Gym",
            "Chandigarh Gyms",
            "Top Gyms In Chandigarh",
            "Most Expensive Gym In Chandigarh",
            "celebrity gym in chandigarh",
            "gym in sector 9 chandigarh",
            "sector 9 gym chandigarh",
            "gym in sector 9",
            "expensive gym in chandigarh",
            "biggest gym in chandigarh",
            "aerobics classes in chandigarh",
            "Best aerobics classes chandigarh",
            "bhangra classes in chandigarh sector 9",
            "yoga classes in chandigarh",
            "Personal Training in chandigarh",
            "yoga studio chandigarh",
            "fitness club in chandigarh",
            "spinning classes in chandigarh",
            "spinning studio in chandigarh",
            "luxury gym in chandigarh",
            "gym in chandigarh with fees",
            "biggest gym in chandigarh",
            "good gyms in chandigarh",
            "benefits of Bhangra classes",
        ]
    },
    "Spa Kora": {
        "website": "spakora.in",
        "color": "#7c3aed",
        "keywords": [
            "best spa in chandigarh",
            "spa kora",
            "spa kora chandigarh",
            "spa in chandigarh",
            "deep tissue spa in chandigarh",
            "full body massage in chandigarh",
            "spa kora in chandigarh",
            "massage spa in chandigarh",
            "spa services in chandigarh",
            "best couple spa chandigarh",
            "couple spa in chandigarh",
            "Luxury Spa In Chandigarh",
            "full body spa in chandigarh",
            "best luxury massage in chandigarh",
            "deep tissue massage in chandigarh",
            "couple massage in chandigarh",
            "couple massage spa in chandigarh",
            "Female to Male Spa in Chandigarh",
            "deep tissue chandigarh",
            "balinese massage in chandigarh",
            "Best balinese massage in chandigarh",
            "full body massage chandigarh",
            "massage service in chandigarh",
            "massage in chandigarh",
            "spa at chandigarh",
            "Spa Massage Chandigarh",
            "top spa in chandigarh",
            "Best Couple Spa In Chandigarh",
            "couple massage spa chandigarh",
            "spa massage in chandigarh",
            "thai massage in chandigarh",
            "thai spa in chandigarh",
            "deep tissue massage chandigarh",
            "couple Massage in chandigarh",
            "spa service chandigarh",
            "premium massage service in chandigarh",
            "premium spa in chandigarh",
            "Premium spa services in Chandigarh",
            "Family Spa in Chandigarh",
            "Authentic Massage in Chandigarh",
        ]
    },
    "BIPS": {
        "website": "bipspatiala.net",
        "color": "#059669",
        "keywords": [
            "bips patiala",
            "bips school patiala",
            "bips school",
            "cbse schools in patiala",
            "best school in patiala",
            "schools in patiala",
            "best schools in patiala",
            "schools in patiala",
            "patiala best school",
            "top 10 schools in patiala",
            "top 5 schools in patiala",
            "schools patiala",
            "top schools in patiala",
            "patiala schools",
            "best cbse schools in patiala",
            "top 10 cbse schools in patiala",
            "cbse schools in patiala city",
            "best cbse school in patiala",
            "Nursery school in Patiala",
            "famous schools in Patiala",
            "top rated schools in Patiala",
            "Best international schools in Patiala",
            "best schools in Patiala with fees",
            "International Schools in Patiala",
            "lkg admission process in patiala schools",
            "ukg admission process in patiala schools",
            "preschool Admission Process in Patiala",
        ]
    },
}


def get_rank(keyword, domain):
    """Return (rank, error). rank=1-10 if found, None if not in top 10."""
    try:
        r = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": GOOGLE_API_KEY, "cx": GOOGLE_CX,
                "q":   keyword, "num": 10, "gl": "in", "hl": "en"
            },
            timeout=15
        )
        data = r.json()
        if "error" in data:
            msg = str(data["error"]).lower()
            if "quota" in msg or data["error"].get("code") == 429:
                return None, "quota"
            return None, "error"
        for i, item in enumerate(data.get("items", []), 1):
            if domain.lower() in item.get("link", "").lower():
                return i, None
        return None, None
    except Exception as e:
        print(f"    Error: {e}")
        return None, "error"


def main():
    print("=" * 55)
    print("  SEO RANK CHECKER — Google Custom Search API")
    print("  100 free queries/day — resets daily forever")
    print("=" * 55)

    if not GOOGLE_API_KEY:
        print("ERROR: GOOGLE_CSE_API_KEY not set!"); raise SystemExit(1)
    if not GOOGLE_CX:
        print("ERROR: GOOGLE_CSE_CX not set!"); raise SystemExit(1)

    try:
        with open("rankings.json", encoding="utf-8") as f:
            old = json.load(f)
    except Exception:
        old = {"brands": {}}

    result      = {"brands": {}}
    query_count = 0
    LIMIT       = 100
    quota_hit   = False

    for brand, info in BRANDS.items():
        print(f"\n  [{brand}]  {info['website']}")
        prev = {k["keyword"]: k for k in
                old.get("brands", {}).get(brand, {}).get("keywords", [])}
        updated = []

        for kw in info["keywords"]:
            if quota_hit or query_count >= LIMIT:
                entry = dict(prev.get(kw, {"keyword": kw, "rank": None}))
                entry["keyword"] = kw
                updated.append(entry)
                continue

            print(f"    [{query_count+1:03d}] {kw}", end=" ... ", flush=True)
            rank, err = get_rank(kw, info["website"])

            if err == "quota":
                print("QUOTA HIT — keeping previous data for remaining keywords")
                quota_hit = True
                entry = dict(prev.get(kw, {"keyword": kw, "rank": None}))
                entry["keyword"] = kw
                updated.append(entry)
                continue

            print(f"#{rank}" if rank else "not in top 10")
            updated.append({"keyword": kw, "rank": rank})
            query_count += 1
            time.sleep(0.3)

        result["brands"][brand] = {
            "website":  info["website"],
            "color":    info["color"],
            "keywords": updated
        }

    utc = datetime.now(timezone.utc)
    ist = utc + timedelta(hours=5, minutes=30)
    result["last_updated"]     = utc.strftime("%Y-%m-%d %H:%M UTC")
    result["last_updated_ist"] = ist.strftime("%d %b %Y, %I:%M %p IST")

    with open("rankings.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n  Done! {query_count} queries used. Quota resets tomorrow.")


if __name__ == "__main__":
    main()

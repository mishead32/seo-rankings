#!/usr/bin/env python3
"""
SEO Rank Checker — Serper.dev API (Real Google Results)
Free signup at serper.dev gives 2500 credits per account.
Supports 2 API keys (SERPER_API_KEY + SERPER_API_KEY_2) for extended use.
When key 1 runs out, automatically switches to key 2.
"""
import requests, json, os, time
from datetime import datetime, timezone, timedelta

# ── API Keys (add both in GitHub Secrets for longer free use) ─────────────────
KEY_1 = os.environ.get("SERPER_API_KEY",   "").strip()
KEY_2 = os.environ.get("SERPER_API_KEY_2", "").strip()

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
    }
}


def get_rank(keyword, domain, api_key):
    """Search Google via Serper.dev and return (rank, error_type)."""
    try:
        r = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json={"q": keyword, "gl": "in", "hl": "en", "num": 10},
            timeout=15
        )
        if r.status_code == 403 or r.status_code == 429:
            return None, "credits_exhausted"

        data = r.json()

        # Check for credit exhaustion in response
        if "error" in data or data.get("credits", 1) == 0:
            return None, "credits_exhausted"

        for i, item in enumerate(data.get("organic", []), 1):
            if domain.lower() in item.get("link", "").lower():
                return i, None

        return None, None   # not in top 10

    except Exception as e:
        print(f"    Error: {e}")
        return None, "error"


def main():
    print("=" * 55)
    print("  SEO RANK CHECKER — Serper.dev (Real Google Results)")
    print("=" * 55)

    # Determine which API key to use
    active_key  = KEY_1
    active_label = "KEY 1"

    if not KEY_1 and not KEY_2:
        print("ERROR: No SERPER_API_KEY set in GitHub Secrets!")
        print("Sign up FREE at https://serper.dev to get your key.")
        raise SystemExit(1)

    if not KEY_1 and KEY_2:
        active_key   = KEY_2
        active_label = "KEY 2"

    print(f"  Using: {active_label}")

    # Load previous rankings
    try:
        with open("rankings.json", encoding="utf-8") as f:
            old = json.load(f)
    except Exception:
        old = {"brands": {}}

    result       = {"brands": {}}
    query_count  = 0
    credits_done = False

    for brand, info in BRANDS.items():
        print(f"\n  [{brand}]  {info['website']}")

        prev = {k["keyword"]: k for k in
                old.get("brands", {}).get(brand, {}).get("keywords", [])}
        updated = []

        for kw in info["keywords"]:

            # If key 1 ran out, try key 2
            if credits_done and active_key == KEY_1 and KEY_2:
                print(f"\n  KEY 1 credits used up — switching to KEY 2 automatically")
                active_key   = KEY_2
                active_label = "KEY 2"
                credits_done = False

            if credits_done:
                # Both keys exhausted — keep previous data
                entry = dict(prev.get(kw, {"keyword": kw, "rank": None}))
                entry["keyword"] = kw
                updated.append(entry)
                continue

            print(f"    [{query_count+1:03d}] {kw}", end=" ... ", flush=True)
            rank, err = get_rank(kw, info["website"], active_key)

            if err == "credits_exhausted":
                if active_key == KEY_1 and KEY_2:
                    print(f"KEY 1 exhausted — switching to KEY 2")
                    active_key   = KEY_2
                    active_label = "KEY 2"
                    # Retry this keyword with key 2
                    rank, err = get_rank(kw, info["website"], active_key)
                    if err == "credits_exhausted":
                        print("KEY 2 also exhausted — keeping previous data")
                        credits_done = True
                        entry = dict(prev.get(kw, {"keyword": kw, "rank": None}))
                        entry["keyword"] = kw
                        updated.append(entry)
                        continue
                else:
                    print("Credits exhausted — keeping previous data for remaining keywords")
                    credits_done = True
                    entry = dict(prev.get(kw, {"keyword": kw, "rank": None}))
                    entry["keyword"] = kw
                    updated.append(entry)
                    continue

            print(f"#{rank}" if rank else "not in top 10")
            updated.append({"keyword": kw, "rank": rank})
            query_count += 1
            time.sleep(0.2)

        result["brands"][brand] = {
            "website":  info["website"],
            "color":    info["color"],
            "keywords": updated
        }

    # Timestamps
    utc = datetime.now(timezone.utc)
    ist = utc + timedelta(hours=5, minutes=30)
    result["last_updated"]     = utc.strftime("%Y-%m-%d %H:%M UTC")
    result["last_updated_ist"] = ist.strftime("%d %b %Y, %I:%M %p IST")

    with open("rankings.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n  Done! {query_count} keywords checked.")


if __name__ == "__main__":
    main()

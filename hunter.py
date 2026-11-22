
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone

SEARCHES = [
    "free AI credits",
    "AI startup credits",
    "free cloud credits",
    "GPU credits startup",
    "free API credits",
    "developer grants AI",
]

KEYWORDS = [
    "credits", "credit", "free tier", "free trial",
    "startup program", "grant", "funding", "gpu",
    "cloud", "api", "compute", "token",
]

def search_hackernews(query):
    encoded = urllib.parse.quote(query)
    url = (
        "https://hn.algolia.com/api/v1/search"
        f"?query={encoded}&tags=story&hitsPerPage=20"
    )

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "AI-Credits-Hunter/1.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data.get("hits", [])

def main():
    found = {}

    for query in SEARCHES:
        print(f"Searching: {query}")

        try:
            hits = search_hackernews(query)

            for hit in hits:
                title = hit.get("title") or ""
                url = hit.get("url") or ""

                if not url:
                    url = (
                        "https://news.ycombinator.com/item?id="
                        + str(hit.get("objectID", ""))
                    )

                text = title.lower()

                score = sum(
                    1 for keyword in KEYWORDS
                    if keyword in text
                )

                if score >= 1:
                    found[url] = {
                        "title": title,
                        "url": url,
                        "score": score,
                        "source": "Hacker News",
                        "points": hit.get("points", 0),
                        "created_at": hit.get("created_at"),
                    }

        except Exception as error:
            print(f"Search failed: {query} | {error}")

    results = sorted(
        found.values(),
        key=lambda item: (
            item["score"],
            item["points"]
        ),
        reverse=True
    )

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_found": len(results),
        "opportunities": results,
    }

    with open("results.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print(f"\nTotal opportunities found: {len(results)}")

    for item in results[:15]:
        print(f"\n[{item['score']}] {item['title']}")
        print(item["url"])

if __name__ == "__main__":
    main()

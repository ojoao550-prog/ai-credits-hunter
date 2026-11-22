
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone

SEARCH_TERMS = [
    "sales",
    "customer support",
    "virtual assistant",
    "appointment setter",
    "lead generation",
    "marketing",
    "freelance",
]

def get_json(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "AI-Money-Hunter/1.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))

def search_remotive(term):
    url = (
        "https://remotive.com/api/remote-jobs?"
        + urllib.parse.urlencode({"search": term})
    )

    data = get_json(url)
    return data.get("jobs", [])

def main():
    opportunities = {}

    for term in SEARCH_TERMS:
        print("Searching:", term)

        try:
            jobs = search_remotive(term)

            for job in jobs:
                job_id = str(job.get("id", ""))

                if not job_id:
                    continue

                opportunities[job_id] = {
                    "title": job.get("title"),
                    "company": job.get("company_name"),
                    "category": job.get("category"),
                    "location": job.get("candidate_required_location"),
                    "salary": job.get("salary") or "Not informed",
                    "job_type": job.get("job_type"),
                    "publication_date": job.get("publication_date"),
                    "application_url": job.get("url"),
                    "source": "Remotive",
                    "remote": True,
                    "verified_for_brazil": False
                }

        except Exception as error:
            print("Search error:", term, error)

    results = list(opportunities.values())

    results.sort(
        key=lambda item: item.get("publication_date") or "",
        reverse=True
    )

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_found": len(results),
        "notice": (
            "Listings are not guaranteed to accept Brazilian applicants. "
            "Check eligibility, payment terms and legitimacy before applying."
        ),
        "opportunities": results
    }

    with open(
        "money_results.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\nTotal opportunities found:", len(results))
    print("Report saved to money_results.json")

    for item in results[:10]:
        print("\n", item["title"])
        print("Company:", item["company"])
        print("Salary:", item["salary"])
        print("Location:", item["location"])
        print("Apply:", item["application_url"])

if __name__ == "__main__":
    main()

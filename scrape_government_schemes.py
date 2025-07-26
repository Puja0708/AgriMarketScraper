import requests
from bs4 import BeautifulSoup
import json

def scrape_raitamitra():
    url = "https://raitamitra.karnataka.gov.in/info-2/Agriculture+Schemes/en"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    schemes = []
    rows = soup.select(".table.table-bordered tr")[1:]
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            name = cols[0].get_text(strip=True)
            desc = cols[1].get_text(strip=True)
            schemes.append({
                "source": "Raitamitra (Karnataka)",
                "scheme_name": name,
                "description": desc
            })
    return schemes


def scrape_kisansuvidha():
    url = "https://www.kisansuvidha.gov.in/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    schemes = []
    links = soup.select(".text-white a")
    for link in links:
        name = link.get_text(strip=True)
        if name and "Yojana" in name or "Scheme" in name or "Mission" in name:
            schemes.append({
                "source": "Kisan Suvidha (National)",
                "scheme_name": name,
                "description": "No description available"
            })
    return schemes


def scrape_agricoop():
    url = "https://agricoop.gov.in/en/Major#gsc.tab=0"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    schemes = []
    items = soup.select("div.tab-content div.tab-pane ul li")
    for li in items:
        name = li.get_text(strip=True)
        if name:
            schemes.append({
                "source": "Agricoop (Ministry of Agriculture)",
                "scheme_name": name,
                "description": "Scheme listed by Agricoop"
            })
    return schemes


def main():
    all_schemes = []

    try:
        print("🔹 Scraping Raitamitra (Karnataka)...")
        all_schemes += scrape_raitamitra()
    except Exception as e:
        print(f"⚠️ Raitamitra scraping failed: {e}")

    try:
        print("🔹 Scraping Kisan Suvidha (National)...")
        all_schemes += scrape_kisansuvidha()
    except Exception as e:
        print(f"⚠️ Kisan Suvidha scraping failed: {e}")

    try:
        print("🔹 Scraping Agricoop (National)...")
        all_schemes += scrape_agricoop()
    except Exception as e:
        print(f"⚠️ Agricoop scraping failed: {e}")

    # Save as JSON
    with open("consolidated_agriculture_schemes.json", "w", encoding="utf-8") as f:
        json.dump(all_schemes, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Done. {len(all_schemes)} schemes saved to 'consolidated_agriculture_schemes.json'")


if __name__ == "__main__":
    main()

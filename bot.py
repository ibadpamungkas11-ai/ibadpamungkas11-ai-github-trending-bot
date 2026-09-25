import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://github.com/trending?since=daily"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
repos = soup.select("article.Box-row")

today = datetime.now().strftime("%Y-%m-%d")

output = [
    "# GitHub Trending 🔥",
    "",
    f"Update: {today}",
    "",
]

for i, repo in enumerate(repos[:10], 1):
    name = repo.select_one("h2 a")

    if not name:
        continue

    repo_name = name.get_text(" ", strip=True).replace(" ", "")
    repo_url = "https://github.com" + name.get("href", "")

    description = repo.select_one("p")
    description = (
        description.get_text(" ", strip=True)
        if description
        else "Tidak ada deskripsi."
    )

    language = repo.select_one("[itemprop='programmingLanguage']")
    language = (
        language.get_text(" ", strip=True)
        if language
        else "Tidak diketahui"
    )

    output.extend([
        f"## {i}. [{repo_name}]({repo_url})",
        "",
        f"**Bahasa:** {language}",
        "",
        description,
        "",
        "---",
        "",
    ])

with open("TRENDING.md", "w", encoding="utf-8") as file:
    file.write("\n".join(output))

print("GitHub Trending berhasil

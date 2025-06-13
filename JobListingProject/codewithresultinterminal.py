# This code prints the result in the terminal
import requests
from bs4 import BeautifulSoup

def scrape_and_display_jobs():
    keyword = input("Enter a job keyword to search for (e.g. python, data, engineer): ").lower()

    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve the web page.")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    job_elements = soup.find_all("div", class_="card-content")

    matches = []

    for job_elem in job_elements:
        title = job_elem.find("h2", class_="title").text.strip()
        company = job_elem.find("h3", class_="company").text.strip()
        location = job_elem.find("p", class_="location").text.strip()
        link = job_elem.find_all("a")[-1]["href"]

        if keyword in title.lower():
            matches.append((title, company, location, link))

    if matches:
        print(f"\nFound {len(matches)} job(s) with keyword '{keyword}':\n")
        for i, (title, company, location, link) in enumerate(matches, start=1):
            print(f"Job #{i}")
            print(f"Title   : {title}")
            print(f"Company : {company}")
            print(f"Location: {location}")
            print(f"Apply   : {link}\n" + "-"*40)
    else:
        print(f"\nNo jobs found with keyword '{keyword}'.")

# Run the interactive job scraper
scrape_and_display_jobs()

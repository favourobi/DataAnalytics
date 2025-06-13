# New features added to this code
'''
Features:
1. Keyword Highlighting (I needed to install a new module using: pip install tabulate termcolor)
2. Formatted the table using the tabulate command
3. Added filters by location and company
4. It was interactive too
5. 
'''

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from termcolor import colored

def scrape_filtered_jobs():
    # User inputs
    keyword = input("Enter a job keyword to search for (e.g. python, data): ").lower()
    location_filter = input("Filter by location (or leave blank to skip): ").lower()
    company_filter = input("Filter by company (or leave blank to skip): ").lower()

    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve the web page.")
        return

    soup_job = BeautifulSoup(response.text, "html.parser")
    job_elements = soup_job.find_all("div", class_="card-content")

    job_rows = []

    for job_elem in job_elements:
        title = job_elem.find("h2", class_="title").text.strip()
        company = job_elem.find("h3", class_="company").text.strip()
        location = job_elem.find("p", class_="location").text.strip()
        link = job_elem.find_all("a")[-1]["href"]

        # Apply filters
        if keyword not in title.lower():
            continue
        if location_filter and location_filter not in location.lower():
            continue
        if company_filter and company_filter not in company.lower():
            continue

        # Highlight keyword in title
        highlighted_title = title.replace(keyword, colored(keyword, "yellow", attrs=["bold"])) if keyword in title.lower() else title

        job_rows.append([highlighted_title, company, location, link])

    if job_rows:
        print("\n" + tabulate(job_rows, headers=["Job Title", "Company", "Location", "Apply Link"], tablefmt="fancy_grid"))
        print(f"\nTotal matches found: {len(job_rows)}")
    else:
        print("\nNo matching jobs found with the given filters.")

# Run it
scrape_filtered_jobs()

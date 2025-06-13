# This particular evolution will work based on the user input
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_jobs_by_keyword():
    keyword = input("Enter a job keyword to search for (e.g. python, data, engineer): ").lower()

    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve the web page.")
        return

    soup_job = BeautifulSoup(response.text, "html.parser")
    job_elements = soup_job.find_all("div", class_="card-content")

    matching_jobs = []

    for job_elem in job_elements:
        title = job_elem.find("h2", class_="title").text.strip()
        company = job_elem.find("h3", class_="company").text.strip()
        location = job_elem.find("p", class_="location").text.strip()
        link = job_elem.find_all("a")[-1]["href"]

        # Check if keyword is in job title
        if keyword in title.lower():
            matching_jobs.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Apply Link": link
            })

    if matching_jobs:
        filename = f"{keyword}_jobs.csv"
        df = pd.DataFrame(matching_jobs)
        df.to_csv(filename, index=False)
        print(f"{len(matching_jobs)} job(s) found with keyword '{keyword}' and saved to {filename}")
    else:
        print(f"No jobs found with keyword '{keyword}'.")

# Run the scraper with keyword input
scrape_jobs_by_keyword()

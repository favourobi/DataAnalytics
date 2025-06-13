import requests
from bs4 import BeautifulSoup
import pandas as pd
#This code has been modified to search for only python jobs only
def scrape_python_jobs():
    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve the web page.")
        return

    soup_job = BeautifulSoup(response.text, "html.parser")
    job_elements = soup_job.find_all("div", class_="card-content")

    python_jobs = []

    for job_elem in job_elements:
        title = job_elem.find("h2", class_="title").text.strip()
        company = job_elem.find("h3", class_="company").text.strip()
        location = job_elem.find("p", class_="location").text.strip()
        link = job_elem.find_all("a")[-1]["href"]

        # Only add jobs that mention "Python" in the title
        if "python" in title.lower():
            python_jobs.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Apply Link": link
            })

    if python_jobs:
        df = pd.DataFrame(python_jobs)
        df.to_csv("python_jobs.csv", index=False)
        print("Python jobs successfully saved to python_jobs.csv!")
    else:
        print("No Python jobs found.")

# Run the filtered scraper
scrape_python_jobs()

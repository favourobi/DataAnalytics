# Now we can improve on this code by clearing search history
# Making it more interactive

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from termcolor import colored
import os
from datetime import datetime

HISTORY_FILE = "search_history.txt"  # History file name


# Show recent search history
def show_search_history(limit=5):
    if os.path.exists(HISTORY_FILE):
        print("\n Last Searches:\n")
        with open(HISTORY_FILE, "r") as file:
            lines = file.readlines()
            last_lines = lines[-limit:]
            for entry in last_lines:
                print("• " + entry.strip())
        print()
    else:
        print("\n No search history yet.\n")


# Log a new search to the history file
def log_search(keyword, location, company, count):
    with open(HISTORY_FILE, "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"[{timestamp}] keyword='{keyword}', location='{location}', company='{company}', matches={count}\n"
        file.write(entry)


# Clear all saved search history
def clear_search_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        print(" Search history cleared.\n")
    else:
        print(" No history to clear.\n")


# Highlight matched text
def highlight(text, match):
    if match and match in text.lower():
        return text.lower().replace(
            match, colored(match, "cyan", attrs=["bold"])
        )
    return text


# Main job scraping and filtering function
def scrape_filtered_jobs():
    # Ask user for filters
    keyword = input("Enter a job keyword to search for (e.g. python, data): ").lower().strip()
    location_filter = input("Filter by location (or leave blank to skip): ").lower().strip()
    company_filter = input("Filter by company (or leave blank to skip): ").lower().strip()

    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)

    if response.status_code != 200:
        print(" Failed to retrieve the job listings.")
        return

    soup_job = BeautifulSoup(response.text, "html.parser")
    job_elements = soup_job.find_all("div", class_="card-content")
    job_rows = []

    for job_elem in job_elements:
        title = job_elem.find("h2", class_="title").text.strip()
        company = job_elem.find("h3", class_="company").text.strip()
        location = job_elem.find("p", class_="location").text.strip()
        link = job_elem.find_all("a")[-1]["href"]

        # Filtering
        if keyword not in title.lower():
            continue
        if location_filter and location_filter not in location.lower():
            continue
        if company_filter and company_filter not in company.lower():
            continue

        # Highlight matches
        title_disp = highlight(title, keyword)
        location_disp = highlight(location, location_filter)
        company_disp = highlight(company, company_filter)

        job_rows.append([title_disp, company_disp, location_disp, link])

    match_count = len(job_rows)
    log_search(keyword, location_filter or "-", company_filter or "-", match_count)

    if job_rows:
        print("\n" + tabulate(
            job_rows,
            headers=["Job Title", "Company", "Location", "Apply Link"],
            tablefmt="fancy_grid"
        ))
        print(f"\n Total matches found: {match_count}")
    else:
        print(f"\n No matching jobs found.\n")


# Menu loop to interact with the user
def main_menu():
    while True:
        print("\n Menu")
        print("1.  Search for jobs")
        print("2.  View last searches")
        print("3.  Clear search history")
        print("4.  Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            scrape_filtered_jobs()
        elif choice == "2":
            show_search_history()
        elif choice == "3":
            clear_search_history()
        elif choice == "4":
            print(" Exiting. Goodbye!\n")
            break
        else:
            print(" Invalid choice. Please enter 1 to 4.\n")


# Run the menu
main_menu()

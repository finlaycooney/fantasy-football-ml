#this is the first script to run to get the data from the website
# it only gets whole season data, not gameweek data

import requests
import pandas as pd



def get_historic_fpl_data():
    """
    Downloads the main history page from Fantasy Nutmeg and returns the HTML.
    """
    print("Requesting data from Fantasy Nutmeg...")

    url = "https://www.fantasynutmeg.com/api/history/season/2024-25"
    try:
        response = requests.get(url)
        response.raise_for_status() # Check for errors
        print("Download successful")
        print(f"Status Code: {response.status_code}")
        html_content = response.text
        return html_content
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None # Return nothing if it fails

downloaded_html = get_historic_fpl_data()

# 2. CHECK if the download worked before continuing
if downloaded_html:
    # At this point, the data is stored in the 'downloaded_html' variable in memory.
    # We can print a small part of it to see it.
    print("\n--- First 500 characters of downloaded data ---")
    print(downloaded_html[:500])
    print("----------------------------------------------\n")

    # 3. SAVE the data from memory into a file on your hard drive
    # This makes the data permanent so you can use it later without re-downloading.
    file_path = 'fpl_history_page.html'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(downloaded_html)

    print(f"Data has been saved to a file named: {file_path}")
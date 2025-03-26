import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_schedule(html, map_name):
    soup = BeautifulSoup(html, 'html.parser')
    sections = soup.find_all('div', style=lambda value: value and 'background' in value)
    # print(f"Found {len(sections)} sections for map {map_name}")  # Debug print
    schedule = []
    for section in sections:
        map_title = section.find('h3').text.strip()
        if map_title == map_name:
            time_info = section.find('p').text.strip()
            if 'From' in time_info and 'to' in time_info and ('starts in' in time_info or 'ends in' in time_info):
                schedule.append(time_info)
    return schedule

def format_schedule(schedule, mode, url):
    output = [f"Fetching schedule for {mode} from URL: {url}"]
    for entry in schedule:
        output.append(f"{MAP_NAME} {entry}")
    return "\n".join(output)

load_dotenv()

BASE_URL = os.getenv('BASE_URL', "https://apexlegendsstatus.com/current-map/battle_royale")
PUBS_URL = f"{BASE_URL}/pubs"
RANKED_URL = f"{BASE_URL}/ranked"
MAP_NAME = os.getenv('MAP_NAME', "Kings Canyon")

def main():
    print("All times are in UTC")

    pubs_html = fetch_html(PUBS_URL)
    pubs_schedule = parse_schedule(pubs_html, MAP_NAME)
    pubs_output = format_schedule(pubs_schedule, "PUBS", PUBS_URL)
    print(pubs_output)

    ranked_html = fetch_html(RANKED_URL)
    ranked_schedule = parse_schedule(ranked_html, MAP_NAME)
    ranked_output = format_schedule(ranked_schedule, "RANKED", RANKED_URL)
    print(ranked_output)

if __name__ == "__main__":
    main()
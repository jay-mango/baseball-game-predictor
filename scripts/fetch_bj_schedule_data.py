from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

print("🚀 Starting Selenium script...")

# Set up Selenium driver
print("🛠️ Setting up Chrome WebDriver...")
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Visit FanGraphs schedule page
url = "https://www.fangraphs.com/teams/blue-jays/schedule"
print(f"🌐 Navigating to {url} ...")
driver.get(url)

# Wait for the page to fully load
print("⏳ Waiting for page to load...")
time.sleep(3)

# Locate the schedule table
print("🔍 Finding the schedule table...")
table = driver.find_element(By.CLASS_NAME, "team-schedule-table")
rows = table.find_elements(By.TAG_NAME, "tr")
print(f"📄 Found {len(rows)} table rows.")

# Prepare data for DataFrame
tor_games_comp = []

print("📥 Starting to scrape completed games only...")
for index, row in enumerate(rows):
    cols = row.find_elements(By.TAG_NAME, "td")
    if cols:
        try:
            tor_runs = cols[5].text
            opp_runs = cols[6].text

            # Skip games with no score (not yet played)
            if tor_runs == "" or opp_runs == "":
                continue

            date = cols[0].text
            opponent = cols[2].text
            result = cols[4].text
            tor_starter = cols[7].text
            opp_starter = cols[8].text

            tor_games_comp.append({
                "Date": date,
                "Opponent": opponent,
                "Result": result,
                "TOR Starter": tor_starter,
                "OPP Starter": opp_starter
            })
        except Exception as e:
            print(f"⚠️ Error reading row {index + 1}: {e}")

# Create DataFrame
df = pd.DataFrame(tor_games_comp, columns=[
    "Date", "Opponent", "Result", "TOR Starter", "OPP Starter"
])
print("\n🧾 DataFrame with completed games created successfully!\n")
print(df)

# Clean up
driver.quit()
print("✅ Done! Browser closed.")

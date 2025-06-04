from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Functions

def get_game_date(stat_name, index, row_dict, table_id):

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, table_id))
    )
    table_hit = driver.find_element(By.ID, table_id)
    rows_hit = table_hit.find_elements(By.TAG_NAME, "tr")

    last_row = rows_hit[-1]  # Get the last row which contains the totals
    cols = last_row.find_elements(By.TAG_NAME, "td")
    if cols:
        row_dict[stat_name] = cols[index].text.strip()  # OPS column
    return row_dict

def extract_stats(driver, row_dict):
    try:
        # Part 1: OPS from Blue Jays - Advanced
        stat_name = "OPS"
        index = 7  # OPS column index in the last row
        bj_hit_table_id = "WinsBox1_dg3hb_ctl00"
        row_dict = get_game_date(stat_name, index, row_dict, bj_hit_table_id)
        
        # Part 2: OPS from Opponent - Advanced
        stat_name = "opp_OPS"
        opp_hit_table_id = "WinsBox1_dg3ab_ctl00"
        row_dict = get_game_date(stat_name, index, row_dict, opp_hit_table_id)

        # Part 3: WHIP from Pitching table - Blue Jays
        stat_name = "WHIP"
        index = 9  # WHIP column index in the last row
        bj_pitch_table_id = "WinsBox1_dg3hp_ctl00"
        row_dict = get_game_date(stat_name, index, row_dict, bj_pitch_table_id)

        # Part 4: WHIP from Pitching table - Opponent
        stat_name = "opp_WHIP"
        bj_pitch_table_id = "WinsBox1_dg3ap_ctl00"
        row_dict = get_game_date(stat_name, index, row_dict, bj_pitch_table_id)


    except Exception as e:
        print(f"❌ Error during stat extraction: {e}")


def click_on_box_score(driver, url, row_dict):

    driver.execute_script("window.open('');")  # Open new tab
    driver.switch_to.window(driver.window_handles[1])  # Switch to new tab
    driver.get(url)

    try:
        driver.find_element(By.LINK_TEXT, "Box Score").click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
   
    except Exception as e:
        print(f"❌ Failed to load box score page: {e}")

    # 👉 Do scraping here...
    extract_stats(driver, row_dict)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def visit_schedule_page(driver):

    # Visit FanGraphs schedule page
    url = "https://www.fangraphs.com/teams/blue-jays/schedule"
    driver.get(url)

    # Wait for the page to fully load
    time.sleep(3)

    # Locate the schedule table
    table = driver.find_element(By.CLASS_NAME, "team-schedule-table")
    rows = table.find_elements(By.TAG_NAME, "tr")

    return rows

# Main Script
print("📅 Fetching BlueJays schedule data...")
# Set up Selenium driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode for faster execution, but you can comment this out if you want to see the browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

rows = visit_schedule_page(driver)

# Prepare data for DataFrame
tor_games = []

for index, row in enumerate(rows):
    cols = row.find_elements(By.TAG_NAME, "td")
    if cols:
        try:
            tor_runs = cols[5].text
            opp_runs = cols[6].text

            # Skip games with no score (not yet played)
            if tor_runs == "" or opp_runs == "":
                continue

            # Create row dict and add basic info
            row_data = {
                "Date": cols[0].text,
                "Opponent": cols[2].text,
                "Result": cols[4].text,
                "OPS": None,
                "WHIP": None,
                "opp_OPS": None,
                "opp_WHIP": None,
            }
            tor_games.append(row_data)
            
            # Get box score link and scrape additional stats
            link_element = cols[0].find_element(By.TAG_NAME, "a")
            box_score_url = link_element.get_attribute("href")
            click_on_box_score(driver, box_score_url, row_data)
            if index == 5:
                break  # For testing, remove this line to scrape all games
        except Exception as e:
            print(f"⚠️ Error reading row {index + 1}: {e}")

# Create DataFrame
df = pd.DataFrame(tor_games)
print(df)
df.to_csv('blue_jays_games_data.csv', index=False)

# Clean up
driver.quit()
print("✅ Done! Browser closed.")
from playwright.sync_api import sync_playwright
from save_to_db import save_ads_to_db
from datetime import datetime
from config import (
    NUXEO_URL,
    USERNAME,
    PASSWORD
)

import json
import os

# ============================================
# CONFIG
# ============================================

TAB_NAMES = [
    "Materials Review",
    "Menu Typing",
    "PreMedia",
    "Design",
    "In Progress Ads",
    "In House Change",
    "Quality Control"
]

# ============================================
# GLOBAL VARIABLES
# ============================================

all_ads = []
current_tab_name = ""

# ============================================
# SWITCH TAB
# ============================================

def switch_tab(page, tab_name):

    global current_tab_name

    current_tab_name = tab_name

    print("\n===================================")
    print(f"SWITCHING TO TAB: {tab_name}")
    print("===================================")

    page.wait_for_selector(
        f"text='{tab_name}'",
        timeout=30000
    )

    tab = page.locator(
        f"text='{tab_name}'"
    ).first

    tab.click()

    page.wait_for_timeout(3000)

# ============================================
# SCRAPE CURRENT PAGE
# ============================================

def scrape_current_page(page):

    rows = page.locator("table tbody tr")

    count = rows.count()

    print(f"\nAds in Current Page: {count}")

    if count == 0:
        return

    for i in range(count):

        try:

            row = rows.nth(i)

            cells = row.locator("td")

            if cells.count() < 12:
                continue

            ad_data = {
                "Tab": current_tab_name,
                "Ad": cells.nth(1).inner_text().strip(),
                "Due Out Deadline": cells.nth(2).inner_text().strip(),
                "Art Deadline": cells.nth(3).inner_text().strip(),
                "Advertiser": cells.nth(4).inner_text().strip(),
                "DT": cells.nth(5).inner_text().strip(),
                "Material": cells.nth(6).inner_text().strip(),
                "Complexity": cells.nth(7).inner_text().strip(),
                "Effort": cells.nth(8).inner_text().strip(),
                "Claimed By": cells.nth(9).inner_text().strip(),
                "Sales Rep": cells.nth(10).inner_text().strip(),
                "Market": cells.nth(11).inner_text().strip(),
                "Scan Time": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }

            all_ads.append(ad_data)

            print(f"Ad Found: {ad_data['Ad']}")

        except Exception as e:

            print("Row extraction error:", e)

# ============================================
# SCRAPE ALL PAGES
# ============================================

def scrape_all_pages(page):

    page.wait_for_timeout(2000)

    pagination = page.locator(
        "span[id*='_nav_top_status']"
    )

    if pagination.count() == 0:

        scrape_current_page(page)

        return

    while True:

        try:

            current_status = pagination.first.inner_text()

            current_page = int(
                current_status.split("/")[0]
            )

            total_pages = int(
                current_status.split("/")[1]
            )

            print(
                f"\nPAGE {current_page} OF {total_pages}"
            )

        except Exception:

            scrape_current_page(page)

            break

        scrape_current_page(page)

        if current_page >= total_pages:
            break

        next_button = page.locator(
            "input[alt='Next']"
        ).first

        next_button.click()

        page.wait_for_timeout(3000)

# ============================================
# LOAD PREVIOUS ADS
# ============================================

def load_previous_ads():

    if not os.path.exists("previous_ads.json"):
        return []

    with open("previous_ads.json", "r") as file:

        return json.load(file)

# ============================================
# SAVE CURRENT ADS
# ============================================

def save_current_ads():

    with open("previous_ads.json", "w") as file:

        json.dump(all_ads, file, indent=4)

# ============================================
# COMPARE ADS
# ============================================

def compare_ads(previous_ads, current_ads):

    previous_ids = {
        ad["Ad"] for ad in previous_ads
    }

    current_ids = {
        ad["Ad"] for ad in current_ads
    }

    incoming_ids = current_ids - previous_ids

    outgoing_ids = previous_ids - current_ids

    incoming_ads = [
        ad for ad in current_ads
        if ad["Ad"] in incoming_ids
    ]

    outgoing_ads = [
        ad for ad in previous_ads
        if ad["Ad"] in outgoing_ids
    ]

    return incoming_ads, outgoing_ads

# ============================================
# SAVE SUMMARY JSON
# ============================================

def save_summary_json(incoming_ads, outgoing_ads):

    summary = {
        "scan_time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "total_ads": len(all_ads),
        "incoming_ads": len(incoming_ads),
        "outgoing_ads": len(outgoing_ads),
        "ads": all_ads
    }

    with open("results.json", "w") as file:

        json.dump(summary, file, indent=4)

# ============================================
# AUTOMATED LOGIN
# ============================================

def login(page):

    print("\nStarting automated login...")

    page.goto(
        NUXEO_URL,
        timeout=60000
    )

    page.wait_for_selector(
        "input[type='text']",
        timeout=60000
    )

    page.fill(
        "input[type='text']",
        USERNAME
    )

    page.fill(
        "input[type='password']",
        PASSWORD
    )

    print("Credentials entered.")

    page.click(
        "button:has-text('Log In')"
    )

    print("Login button clicked.")

    page.wait_for_selector(
        "text='Materials Review'",
        timeout=120000
    )

    print("Login successful.")

# ============================================
# MAIN EXECUTION
# ============================================

def run_monitor():

    global all_ads

    all_ads.clear()

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--single-process",
                "--disable-setuid-sandbox",
                "--no-zygote"
            ]
        )

        context = browser.new_context()

        page = context.new_page()

        try:

            # LOGIN
            login(page)

            print("\n===================================")
            print("STARTING SCAN")
            print("===================================")

            for tab_name in TAB_NAMES:

                try:

                    switch_tab(page, tab_name)

                    scrape_all_pages(page)

                except Exception as tab_error:

                    print(f"\nTAB ERROR: {tab_name}")

                    print(tab_error)

            print("\n===================================")
            print(f"TOTAL ADS: {len(all_ads)}")
            print("===================================")

            previous_ads = load_previous_ads()

            incoming_ads, outgoing_ads = compare_ads(
                previous_ads,
                all_ads
            )

            print(f"Incoming Ads: {len(incoming_ads)}")
            print(f"Outgoing Ads: {len(outgoing_ads)}")

            save_current_ads()

            save_ads_to_db(all_ads)

            save_summary_json(
                incoming_ads,
                outgoing_ads
            )

            result = {
                "status": "success",
                "total_ads": len(all_ads),
                "incoming_ads": len(incoming_ads),
                "outgoing_ads": len(outgoing_ads)
            }

            browser.close()

            return result

        except Exception as e:

            browser.close()

            return {
                "status": "error",
                "message": str(e)
            }

# ============================================
# DIRECT RUN
# ============================================

if __name__ == "__main__":

    result = run_monitor()

    print(result)
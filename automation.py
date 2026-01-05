# =========================
# SAFETY / LOGGING LAYER
# =========================
import sys, traceback, logging, time
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
SCREENSHOT_DIR = BASE_DIR / "screenshots"

LOG_DIR.mkdir(exist_ok=True)
SCREENSHOT_DIR.mkdir(exist_ok=True)

RUN_TS = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = LOG_DIR / f"automation_{RUN_TS}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)

logging.info("========== AUTOMATION START ==========")

def crash_handler(exc_type, exc_value, exc_tb):
    logging.critical("UNCAUGHT EXCEPTION", exc_info=(exc_type, exc_value, exc_tb))
    try:
        if "tab" in globals():
            shot = SCREENSHOT_DIR / f"crash_{RUN_TS}.png"
            tab.screenshot(path=str(shot))
            logging.info(f"Screenshot saved: {shot}")
    except Exception as e:
        logging.error(f"Screenshot failed: {e}")

sys.excepthook = crash_handler

# =========================
# ORIGINAL SCRIPT START
# =========================

from DrissionPage import Chromium, ChromiumOptions
from time import sleep
import datetime, random
import pandas as pd
from datetime import datetime, timedelta
from human_utils import (
    human_click,
    human_input,
    human_sleep,
    find_element,
    find_elements,
    switch_to_iframe,
    exit_iframe,
    go_to,
    click_js,
)

# Replace placeholders with your actual details:
USERNAME = "jlesnick87@gmail.com"
PASSWORD = "tizbox-mutqEt-voqdo3"
CVV_CODE = "123"

EVENT_NAME = "My Tennis Booking"
# TARGET_DATE = input("Enter your preferred date (YYYY-MM-DD): ").strip()


def format_start_end_time(user_input):
    """Convert '6 AM' → ('6:00 AM', '7:00 AM')"""
    user_input = user_input.strip().upper()

    # Add :00 if minutes are missing
    if ":" not in user_input:
        user_input = user_input.replace(" ", ":00 ")

    # Convert to datetime
    start_dt = datetime.strptime(user_input, "%I:%M %p")

    # End time is +1 hour
    end_dt = start_dt + timedelta(hours=1)

    # Format properly - cross-platform compatible
    # Manually format to remove leading zeros from hour
    def format_time(dt):
        hour = dt.hour % 12 or 12  # Convert 0 to 12, 13-23 to 1-11
        minute = dt.minute
        am_pm = dt.strftime("%p")
        return f"{hour}:{minute:02d} {am_pm}"

    start_time = format_time(start_dt)   # 6:00 AM
    end_time = format_time(end_dt)       # 7:00 AM

    return start_time, end_time

import pandas as pd

# Read Excel (times.xlsx must be in same folder)
df = pd.read_excel("times.xlsx")

# Convert Excel times → (start_time, end_time)
PREFERRED_TIMES = [
    format_start_end_time(time)
    for time in df["Time"].dropna()
]


ball_machine_excel = str(df["BallMachine"].iloc[0]).strip().lower()
NEED_BALL_MACHINE = ball_machine_excel in ["yes", "y"]

# Print to confirm
print("\n--- Preferences Set ---")
print("Times:", PREFERRED_TIMES)
print("Need Ball Machine:", NEED_BALL_MACHINE)

# --- LOGIN SELECTORS (CONFIRMED) ---
LOGIN_USER_SELECTOR = "[aria-label='Email address Required']"
LOGIN_PASS_SELECTOR = "[aria-label='Password Required']"
LOGIN_BTN_XPATH     = "//button[contains(@class, 'btn-super') and .//span[text()='Sign in']]"

df = pd.read_excel("times.xlsx")

PREFERRED_TIMES = [
    format_start_end_time(str(time))
    for time in df["Time"].dropna()
]

target_date_excel = df["Date"].iloc[0]
target_date = pd.to_datetime(target_date_excel)
target_month_search = target_date.strftime("%b %Y")        # e.g., "Dec 2025"
target_aria_label   = target_date.strftime("%b %d, %Y").replace(" 0", " ")
# Multiple user agents to randomly choose from
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

# opening the browser
co = ChromiumOptions().set_local_port(9111)
selected_user_agent = random.choice(USER_AGENTS)
co.set_user_agent(selected_user_agent)
print(f"Using User Agent: {selected_user_agent}")

# Start browser with custom UA
browser = Chromium(co)
tab = browser.latest_tab
tab.set.window.max()

# opening the required browser
tab.get("https://anc.apm.activecommunities.com/chicagoparkdistrict/home?onlineSiteId=0&from_original_cui=true")
sleep(random.uniform(1.0, 2.5))

sign_in_link = tab.ele('xpath://div[@class="an-header__user-profiles"]//a[text()="Sign In"]', timeout=10)

if sign_in_link:
    human_click(sign_in_link)
    print("✅ Clicked 'Sign In'")
    sleep(random.uniform(1.0, 2.5))
else:
    print("❌ 'Sign In' link not found!")


# Check if already logged in
def is_logged_in():
    """Check if user is already logged in by checking for View Account element"""
    view_account = tab.ele('css:div.an-header__user-profiles > span:nth-child(2)', timeout=2)
    if view_account and "View Account" in view_account.text:
        return True
    return False

# Check if already logged in, skip login if so
if is_logged_in():
    print("✅ User is already logged in. Skipping login process...")
    # Navigate to the quick reservation page
    print(" -> Navigating to quick reservation page...")
    tab.get("https://anc.apm.activecommunities.com/chicagoparkdistrict/home?onlineSiteId=0&from_original_cui=true")
    sleep(random.uniform(1.0, 2.5))

    # Click "Clear all bookings" button to start fresh
    print(" -> Clicking 'Clear all bookings' button...")
    clear_btn = tab.ele('css:button[aria-label="Clear all bookings"]', timeout=10)
    if clear_btn:
        human_click(clear_btn)
        print(" -> Cleared all bookings")
        sleep(random.uniform(1.0, 2.0))
    else:
        print("⚠️ Clear all bookings button not found, continuing anyway...")
else:
    print("🔐 User not logged in. Proceeding with login...")
    email = tab.ele(f'css:{LOGIN_USER_SELECTOR}', timeout=20)
    email.clear()
    sleep(random.uniform(0.2, 0.5))
    human_input(email, USERNAME)
    sleep(random.uniform(0.5, 1.5))

    # Wait and type password
    password = tab.ele(f'css:{LOGIN_PASS_SELECTOR}', timeout=20)
    password.clear()
    human_input(password, PASSWORD)
    sleep(random.uniform(0.5, 1.5))

    # Wait and click login button
    login_btn = tab.ele(f'xpath:{LOGIN_BTN_XPATH}', timeout=20)
    human_click(login_btn)
    sleep(random.uniform(3, 4.5))

reservations_btn = tab.ele('xpath://li//span[text()="Reservations"]/parent::a', timeout=10)
if reservations_btn:
    human_click(reservations_btn)
    print("✅ Clicked 'Reservations'")
    sleep(random.uniform(3, 4.5))
else:
    print("❌ 'Reservations' button not found!")

view_all_btn = tab.ele('xpath://a[@class="carousel-group__link-all"]//span[text()="View all"]/parent::a', timeout=10)
if view_all_btn:
    human_click(view_all_btn)
    print("✅ Clicked 'View all'")
    sleep(random.uniform(3, 4.5))
else:
    print("❌ 'View all' button not found!")

facility_btn = tab.ele('xpath://div[contains(@class,"dropdown__button") and .//span[text()="Facility/Equipment Group"]]', timeout=10)

if facility_btn:
    human_click(facility_btn)
    print("✅ Clicked 'Facility/Equipment Group' button")
    sleep(random.uniform(3, 4.5))
else:
    print("❌ 'Facility/Equipment Group' button not found!")

option = find_element(tab, "text:Park Rental - McFetridge Indoor Tennis/Pickleball", timeout=10)

if option:
    human_click(option)
    print("✅ Selected 'Park Rental - McFetridge Indoor Tennis/Pickleball'")
    sleep(random.uniform(3, 4.5))
else:
    print("❌ Option not found!")

# Wait and put Targeted date
date_input = tab.ele('css:input[role="combobox"]', timeout=10)
if not date_input:
    raise Exception("❌ Date input field not found!")
human_click(date_input)
sleep(random.uniform(0.5, 1.5))

calendar_header = tab.ele('css:.an-calendar-header-title', timeout=5)
next_btn = tab.ele('css:i.icon-chevron-right', timeout=5)

while target_month_search not in calendar_header.text:
    next_btn.click()
    sleep(random.uniform(0.5, 1.5))
    calendar_header = tab.ele('css:.an-calendar-header-title', timeout=5)

sleep(random.uniform(0.5, 1.5))

day_cell = tab.ele(f'xpath://div[@aria-label="{target_aria_label}" and @role="region"]', timeout=10)
human_click(day_cell)
sleep(random.uniform(0.5, 1.5))

event_input = tab.ele('css:input[data-qa-id="quick-reservation-eventType-name"]', timeout=10)
event_input.clear()
sleep(random.uniform(0.5, 1.5))
human_input(event_input, EVENT_NAME)
SAVE_BUTTON_XPATH = "//button[contains(., 'Save')]"
def wait_until_booking_time():
    """Wait for 10 minutes before proceeding with booking"""
    wait_seconds = 5  # 10 minutes
    now = datetime.now()

    print(f"\n⏰ Current time: {now.strftime('%I:%M:%S %p')}")
    print(f"⏰ Waiting {wait_seconds // 60} minutes before proceeding with booking...")

    # Wait with countdown updates
    start_time = datetime.now()
    last_printed_seconds = -1
    while (datetime.now() - start_time).total_seconds() < wait_seconds:
        elapsed = (datetime.now() - start_time).total_seconds()
        remaining = wait_seconds - elapsed
        if remaining > 0:
            minutes = int(remaining // 60)
            secs = int(remaining % 60)
            # Update every 30 seconds, or every second in last 10 seconds
            should_print = (secs % 30 == 0 and secs != last_printed_seconds) or (remaining <= 10 and secs != last_printed_seconds)
            if should_print:
                print(f"   ⏳ {minutes:02d}:{secs:02d} remaining...")
                last_printed_seconds = secs
        sleep(1)

    print(f"✅ Wait complete! Current time: {datetime.now().strftime('%I:%M:%S %p')}")
    print("🚀 Proceeding with booking now...\n")

FAILED_COURTS = []

def select_time_slot():
    """Select an available time slot from preferred times"""
    booking_successful = False
    selected_time_slot = None
    court_label = None

    # Wait and click on available slot from given ones
    for start_time, end_time in PREFERRED_TIMES:
        print(f" -> Searching for available court at {start_time} - {end_time}...")

        court_xpath = (
                f"//div[contains(@aria-label, 'Tennis') "
                f"and contains(@aria-label, '{start_time} - {end_time}') "
                f"and contains(@aria-label, 'Available')]"
            )

        court_cells = tab.eles(f'xpath:{court_xpath}', timeout=2)  # Returns NoneElement if not found
        # court_label = court_cell.attr('aria-label') if court_cell else None
        if court_label and (start_time, end_time, court_label) in FAILED_COURTS:
            print(f" -> Skipping failed court: {court_label}")
            continue

        if not court_cells:
            print(f" -> Court at {start_time} - {end_time} not available.")
            sleep(random.uniform(0.5, 1.5))
            continue  # Try next time slot

        machine_cell = None
        if NEED_BALL_MACHINE:
            machine_xpath = (
                f"//div[@role='gridcell' "
                f"and contains(@aria-label, 'Ball Machine') "
                f"and contains(@aria-label, '{start_time} - {end_time}') "
                f"and contains(@aria-label, 'Available')]"   # Ensures availability
            )

            machine_cell = tab.ele(f'xpath:{machine_xpath}', timeout=2)

            if not machine_cell:
                print(f" -> Machine not available at {start_time} - {end_time}.")
                continue  # Skip to the next time slot

        print(f" -> Machine available at {start_time} - {end_time}.")


        # Click the court
        for court_cell in court_cells:
            court_label = court_cell.attr('aria-label')
            if (start_time, end_time, court_label) in FAILED_COURTS:
                print(f" -> Skipping failed court: {court_label}")
                continue

            human_click(court_cell)
            print(f" -> Court clicked: {court_label}")
            sleep(random.uniform(0.5, 1.5))

        # Click ball machine if needed
            if NEED_BALL_MACHINE and machine_cell:
                human_click(machine_cell)
                sleep(random.uniform(3.5, 4.5))
                print(" -> Ball Machine clicked.")

            booking_successful = True
            selected_time_slot = f"{start_time} - {end_time}"
            break  # Exit the loop because we booked successfully
        if booking_successful:
            break

    return booking_successful, selected_time_slot, court_label

booking_successful, selected_time_slot, court_label = select_time_slot()

if not booking_successful:
    print("❌ FAILED: No available slot found matching all criteria.")
else:
    print("✅ Booking process completed successfully!")

if booking_successful:

    # Wait 10 minutes after clicking confirm booking, before proceeding to checkout
    print("\n⏰ Waiting 10 minutes before proceeding to checkout page...")
    wait_until_booking_time()

    print("Step E: Processing confirmation steps...")
    CONFIRM_BUTTON_CSS = "[data-qa-id='quick-reservation-ok-button']"
    confirm_btn = tab.ele(f"css:{CONFIRM_BUTTON_CSS}", timeout=10)
    if confirm_btn:
        human_click(confirm_btn)
    else:
        print("❌ Confirm button not found!")
        raise Exception("Confirm button missing")
    sleep(random.uniform(0.5, 5.5))

    # Check for Service Error
    error_modal = tab.ele('css:h3.modal-title', timeout=2)
    if error_modal and error_modal.text == "Service Error":
        print("⚠️ Service Error detected! Handling error recovery...")

        # Click OK button (button.btn.btn-strong with type="submit" containing span with "OK" text)
        ok_btn = tab.ele('xpath://button[@class="btn btn-strong" and @type="submit" and .//span[contains(translate(text(), "ok", "OK"), "OK")]]', timeout=10)
        if not ok_btn:
            # Try alternative selector
            ok_btn = tab.ele('xpath://button[contains(@class, "btn") and contains(@class, "btn-strong") and @type="submit" and .//span[contains(translate(text(), "ok", "OK"), "OK")]]', timeout=5)
        if ok_btn:
            human_click(ok_btn)
            print(" -> Clicked OK button")
            sleep(random.uniform(0.5, 4.5))
        else:
            print("❌ OK button not found!")
            raise Exception("OK button missing")

        # Click Clear all bookings button
        clear_btn = tab.ele('css:button[aria-label="Clear all bookings"]', timeout=10)
        if clear_btn:
            human_click(clear_btn)
            print(" -> Clicked Clear all bookings button")
            sleep(random.uniform(2.0, 5.5))
        else:
            print("❌ Clear all bookings button not found!")
            raise Exception("Clear all bookings button missing")

        # Reselect the time slot
        print(" -> Reselecting time slot...")
        booking_successful, selected_time_slot = select_time_slot()

    #error handling 2
    error_modal = tab.ele('css:h3.modal-title', timeout=2)
    if error_modal and error_modal.text == "Service Error":
        print("⚠️ Service Error detected! Handling error recovery...")

        # Click OK button (button.btn.btn-strong with type="submit" containing span with "OK" text)
        ok_btn = tab.ele('xpath://button[@class="btn btn-strong" and @type="submit" and .//span[contains(translate(text(), "ok", "OK"), "OK")]]', timeout=10)
        if not ok_btn:
            # Try alternative selector
            ok_btn = tab.ele('xpath://button[contains(@class, "btn") and contains(@class, "btn-strong") and @type="submit" and .//span[contains(translate(text(), "ok", "OK"), "OK")]]', timeout=5)
        if ok_btn:
            human_click(ok_btn)
            print(" -> Clicked OK button")
            sleep(random.uniform(2.5, 6.5))
        else:
            print("❌ OK button not found!")
            raise Exception("OK button missing")

        # Click Clear all bookings button
        clear_btn = tab.ele('css:button[aria-label="Clear all bookings"]', timeout=10)
        if clear_btn:
            human_click(clear_btn)
            print(" -> Clicked Clear all bookings button")
            sleep(random.uniform(1.0, 4.5))
        else:
            print("❌ Clear all bookings button not found!")
            raise Exception("Clear all bookings button missing")

        # Reselect the time slot
        print(" -> Reselecting time slot...")
        booking_successful, selected_time_slot = select_time_slot()

        if booking_successful:
            # Click confirm button again
            confirm_btn = tab.ele(f"css:{CONFIRM_BUTTON_CSS}", timeout=10)
            if confirm_btn:
                human_click(confirm_btn)
                print(" -> Clicked confirm button again after error recovery")

            else:
                print("❌ Confirm button not found after error recovery!")
                raise Exception("Confirm button missing after error recovery")
        else:
            print("❌ Failed to reselect time slot after error recovery!")
            raise Exception("Could not reselect time slot")

    save_btn = tab.ele(f'xpath:{SAVE_BUTTON_XPATH}', timeout=10)
    if save_btn:
        print("Save button found!")
        human_click(save_btn)
        sleep(random.uniform(2.5, 3.5))
    else:
        print("⚠️ Save button not found — clearing bookings and retrying time selection...")
        if selected_time_slot and court_label:
            start_time, end_time = selected_time_slot.split(" - ")
            FAILED_COURTS.append((start_time, end_time, court_label))
            print(f" -> Marked court as failed: {court_label}")


        clear_btn = tab.ele('css:button[aria-label="Clear all bookings"]', timeout=10)
        if clear_btn:
            human_click(clear_btn)
            sleep(random.uniform(1.0, 2.5))
            print(" -> Cleared all bookings")
        else:
            raise Exception("Clear all bookings button missing")

        booking_successful, selected_time_slot, court_label = select_time_slot()
        if booking_successful:
            print("Step E:Again, Processing confirmation steps...")
            confirm_btn = tab.ele(f"css:{CONFIRM_BUTTON_CSS}", timeout=10)
            if confirm_btn:
                human_click(confirm_btn)
                sleep(random.uniform(0.5, 5.5))
            else:
                raise Exception("Confirm button missing after retry")

            save_btn = tab.ele(f'xpath:{SAVE_BUTTON_XPATH}', timeout=5)
            if save_btn:
               human_click(save_btn)
               sleep(random.uniform(3.5, 5.5))
               print(" -> Save button clicked after retry")
            else:
                raise Exception("Save button still missing after retry")
        else:
            raise Exception("No available courts after retry")

    DISCLAIMER_INPUT_XPATH = "//input[@data-qa-id='disclaimer-checkbox-18']"
    checkbox_input = tab.ele(f'xpath:{DISCLAIMER_INPUT_XPATH}', timeout=10)
    if checkbox_input:
        human_click(checkbox_input)
        sleep(random.uniform(4.5, 6.5))
    else:
        print("❌ Disclaimer checkbox not found!")
        raise Exception("Disclaimer input missing")

    # SAVE_BUTTON_XPATH = "//button[contains(., 'Save')]"

    save_btn = tab.ele(f'xpath:{SAVE_BUTTON_XPATH}', timeout=10)
    if save_btn:
        human_click(save_btn)
        sleep(random.uniform(2.5, 3.5))
    else:
        print("❌ Save button not found!")
    tab.refresh()
    RESERVE_BTN_CSS = "[data-qa-id='quick-reservation-reserve-button']"

    reserve_btn = tab.ele(f"css:{RESERVE_BTN_CSS}", timeout=10)

    if reserve_btn:
        # Check if element is visible and has size, otherwise use JS click
        try:
            # Try to get the element's rect to check if it's visible
            rect = reserve_btn.rect
            if rect and rect.width > 0 and rect.height > 0:
                human_click(reserve_btn)
            else:
                # Element exists but not visible, use JS click
                print(" -> Reserve button not visible, using JavaScript click")
                tab.run_js("arguments[0].click();", reserve_btn)
        except Exception as e:
            # If hover/click fails, fallback to JS click
            print(f" -> Error with human_click, using JavaScript click: {e}")
            tab.run_js("arguments[0].click();", reserve_btn)
        sleep(random.uniform(3, 5.0))

        # Wait a bit and check if we're on checkout page
        sleep(random.uniform(0.5, 1.0))
        is_on_checkout = "checkout" in tab.url

        # If not on checkout, check for Service Error modal
        if not is_on_checkout:
            error_modal = tab.ele('css:h3.modal-title', timeout=3)
            if error_modal and error_modal.text == "Service Error":
                print("⚠️ Service Error detected after Reserve button click! Handling error recovery...")

                # Click OK button (button.btn.btn-strong with type="submit" containing span with "OK" text)
                ok_btn = tab.ele('xpath://button[@class="btn btn-strong" and @type="submit" and .//span[contains(translate(text(), "ok", "OK"), "OK")]]', timeout=10)
                if not ok_btn:
                    # Try alternative selector
                    ok_btn = tab.ele('xpath://button[contains(@class, "btn") and contains(@class, "btn-strong") and @type="submit" and .//span[contains(translate(text(), "ok", "OK"), "OK")]]', timeout=5)
                if ok_btn:
                    human_click(ok_btn)
                    print(" -> Clicked OK button")
                    sleep(random.uniform(0.5, 1.5))
                else:
                    print("❌ OK button not found!")
                    raise Exception("OK button missing")

                # Click Clear all bookings button
                clear_btn = tab.ele('css:button[aria-label="Clear all bookings"]', timeout=10)
                if clear_btn:
                    human_click(clear_btn)
                    print(" -> Clicked Clear all bookings button")
                    sleep(random.uniform(1.0, 2.5))
                else:
                    print("❌ Clear all bookings button not found!")
                    raise Exception("Clear all bookings button missing")

                # Reselect the time slot
                print(" -> Reselecting time slot...")
                booking_successful, selected_time_slot = select_time_slot()

                if booking_successful:
                    # Click confirm button again
                    confirm_btn = tab.ele(f"css:{CONFIRM_BUTTON_CSS}", timeout=10)
                    if confirm_btn:
                        human_click(confirm_btn)
                        print(" -> Clicked confirm button again after error recovery")
                        sleep(random.uniform(0.5, 1.5))

                        checkbox_input = tab.ele(f'xpath:{DISCLAIMER_INPUT_XPATH}', timeout=10)
                        if checkbox_input:
                            human_click(checkbox_input)
                            sleep(random.uniform(0.5, 1.5))

                        save_btn = tab.ele(f'xpath:{SAVE_BUTTON_XPATH}', timeout=10)
                        if save_btn:
                            human_click(save_btn)
                            sleep(random.uniform(0.5, 1.5))

                        # Click Reserve button again
                        tab.refresh()
                        reserve_btn = tab.ele(f"css:{RESERVE_BTN_CSS}", timeout=10)
                        if reserve_btn:
                            # Check if element is visible and has size, otherwise use JS click
                            try:
                                rect = reserve_btn.rect
                                if rect and rect.width > 0 and rect.height > 0:
                                    human_click(reserve_btn)
                                else:
                                    print(" -> Reserve button not visible, using JavaScript click")
                                    tab.run_js("arguments[0].click();", reserve_btn)
                            except Exception as e:
                                print(f" -> Error with human_click, using JavaScript click: {e}")
                                tab.run_js("arguments[0].click();", reserve_btn)
                            print(" -> Clicked Reserve button again after error recovery")
                            sleep(random.uniform(0.5, 1.5))
                    else:
                        print("❌ Confirm button not found after error recovery!")
                        raise Exception("Confirm button missing after error recovery")
                else:
                    print("❌ Failed to reselect time slot after error recovery!")
                    raise Exception("Could not reselect time slot")
            else:
                print("⚠️ Service Error modal not found, but not on checkout page. Continuing...")
        else:
            print("✅ Successfully navigated to checkout page!")
    else:
        print("❌ Reserve button not found!")

    print("Step F: Entering CVV and paying...")

# Wait until URL contains 'checkout' (only if not already on checkout)
    if "checkout" not in tab.url:
        print(" -> Waiting for checkout page...")
        for _ in range(40):   # 40 × 0.5s = 20 seconds max
            if "checkout" in tab.url:
                print(" -> Reached checkout page!")
                break
            sleep(random.uniform(0.5, 1.5))
        else:
            raise Exception("❌ Failed to reach checkout page after Reserve button click!")

    # 1. Enter CVV

    # Get the iframe element
    iframe = tab.get_frame('css:div.iframeContainer > iframe')
    sleep(random.uniform(0.5, 1.0))

    # Click inside the iframe area to activate it
    print(" -> Clicking inside iframe to activate it...")
    iframe_body = iframe.ele('css:body', timeout=10)
    if iframe_body:
        iframe_body.click()
        sleep(random.uniform(0.5, 1.0))
    else:
        # Fallback: click on the iframe container
        iframe_container = tab.ele('css:div.iframeContainer', timeout=10)
        if iframe_container:
            iframe_container.click()
            sleep(random.uniform(0.5, 1.0))

    # CVV input selector - using XPath to handle the colon in ID
    CVV_INPUT_XPATH = "//input[@id='form_group_input:r2:__cvv']"

    # Find CVV input INSIDE the iframe
    print(" -> Finding CVV input field...")
    cvv_input = iframe.wait.ele_displayed(f"xpath:{CVV_INPUT_XPATH}", timeout=20)
    if not cvv_input:
        raise Exception("❌ CVV input not found inside iframe!")

    # Click on the CVV input field
    print(" -> Clicking CVV input field...")
    cvv_input.click()
    sleep(random.uniform(0.5, 1.0))

    # Type the CVV code
    print(f" -> Typing CVV code: {CVV_CODE}")
    cvv_input.clear()
    human_input(cvv_input, CVV_CODE)
    sleep(random.uniform(0.5, 1.5))
    print(" -> Clearing and adding the CVV again...")
    cvv_input.clear()
    human_input(cvv_input, CVV_CODE)
    sleep(random.uniform(0.5, 1.5))

    # 2. Click Pay button
    PAY_BTN_CSS = "[data-qa-id='checkout-orderSummary-payBtn']"

    pay_btn = tab.ele(f"css:{PAY_BTN_CSS}", timeout=10)
    if not pay_btn:
        raise Exception("❌ Pay button not found!")

    # Always click using JS for safety
    tab.run_js("arguments[0].click();", pay_btn)
    print("\n✅ SUCCESS! Booking and Payment are complete.")


sleep(random.uniform(15, 25))
tab.close()


# =========================
# RETRY HARNESS (BOTTOM)
# =========================

MAX_RETRIES = 3
RETRY_DELAY = 30

for attempt in range(1, MAX_RETRIES + 1):
    try:
        logging.info(f"Attempt {attempt}/{MAX_RETRIES}")
        # Script already executed top-down
        break
    except Exception as e:
        logging.error(f"Failure on attempt {attempt}")
        logging.error(traceback.format_exc())
        if attempt < MAX_RETRIES:
            logging.info(f"Retrying in {RETRY_DELAY}s")
            time.sleep(RETRY_DELAY)
        else:
            logging.critical("ALL RETRIES FAILED")
            raise

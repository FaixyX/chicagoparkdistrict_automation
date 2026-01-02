import time
import random
from DrissionPage import Chromium

# ---------- Human-like helper functions ----------
def human_sleep(a=0.5, b=1.5):
    """Random sleep to mimic human delays"""
    time.sleep(random.uniform(a, b))

def human_click(element):
    """Scroll, hover, and click element like a human"""
    element.scroll()
    human_sleep(0.3, 0.6)
    element.hover()
    human_sleep(0.3, 0.6)
    element.click()
    human_sleep(0.1, 0.4)

def human_input(element, text):
    """Click and type text with human-like delays"""
    element.scroll()
    human_sleep(0.1, 0.3)
    element.click()
    human_sleep(0.1, 0.3)
    for ch in text:
        element.input(ch)  # DrissionPage input is per char fast
        time.sleep(random.uniform(0.05, 0.2))
    human_sleep(0.2, 0.5)

def human_select_dropdown(tab, dropdown_locator, option_text):
    """Select option from dropdown by visible text"""
    dropdown = tab.wait.ele_displayed(dropdown_locator, timeout=10)
    human_click(dropdown)
    human_sleep(0.2, 0.5)
    option = tab.wait.ele_displayed(f"text:{option_text}", timeout=5)
    human_click(option)

def human_scroll_to(tab, element):
    """Scroll to element smoothly"""
    element.scroll_to()
    human_sleep(0.2, 0.5)

# ---------- Element finders ----------
def find_element(tab, locator, timeout=10):
    """Wait for element to exist and return it"""
    return tab.wait.ele_displayed(locator, timeout=timeout)

def find_elements(tab, locator, timeout=10):
    """Wait for multiple elements to be visible"""
    return tab.wait.eles_displayed(locator, timeout=timeout)

# ---------- JS helpers ----------
def click_js(tab, element):
    """Click using JS"""
    tab.run_js("arguments[0].click();", element)
    human_sleep(0.2, 0.5)

# ---------- Tab helpers ----------
def go_to(tab, url):
    """Open URL and wait a little"""
    tab.get(url)
    human_sleep(1, 2)

def scroll_bottom(tab):
    """Scroll to bottom of page"""
    tab.run_js("window.scrollTo(0, document.body.scrollHeight);")
    human_sleep(0.5, 1.0)

def scroll_top(tab):
    """Scroll to top"""
    tab.run_js("window.scrollTo(0,0);")
    human_sleep(0.5, 1.0)

# ---------- Iframe helpers ----------
def switch_to_iframe(tab, iframe_locator):
    """Return a child tab pointing to iframe"""
    iframe = find_element(tab, iframe_locator)
    return tab.frame_tab(iframe)

def exit_iframe(tab):
    """Go back to main page from iframe"""
    tab.frame_tab(None)  # In newer DrissionPage versions
    human_sleep(0.5, 1.0)

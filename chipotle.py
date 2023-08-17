import time
import sys
import re
import logging
import subprocess
import pyautogui
import pytesseract
import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

FOUND_CODES_FILE = "foundCodes.txt"
FOUND_IMAGES_FILE = "foundImages.txt"
TWITTER_PAGE = "https://twitter.com/ChipotleTweets"
# TWITTER_PAGE = "https://twitter.com/0b11100001"

logging.getLogger().setLevel(logging.INFO)

def setClipboard(message):
    """Set clipboard (Mac only)"""
    subprocess.run("pbcopy", text=True, input=message)

def guiPaste():
    """Paste shortcut (Mac only)"""
    pyautogui.hotkey('command', 'v')

def sendSMSFirstRecipient(message):
    """Send an SMS to the first message in IMessage.
    Assumes the targeted address is the first one in
    message recipeints list.
    We hard code in icon positions.
    """

    # Desktop app coordinates hardcoded for simplicity.
    SMS_APP_ICON = (243, 909)
    PINNED_MESSAGE = (154, 188) #click this as fallback
    TEXT_BOX = (429, 848)

    logging.info(f"Attempting to send SMS: `{message}`...")
    start = time.perf_counter()
    setClipboard(message)
    pyautogui.click(*SMS_APP_ICON)
    # time.sleep(0.01)
    pyautogui.click(*PINNED_MESSAGE)
    # time.sleep(0.01)
    pyautogui.click(*TEXT_BOX)
    # time.sleep(0.05)
    guiPaste()
    # time.sleep(0.05)
    pyautogui.press("enter")
    end = time.perf_counter()
    seconds = end - start
    logging.info(f"Done. Took {seconds:0.4f} seconds to send.")
    time.sleep(0.05) # Needed to make sure enter is pressed

def runBot():
    regexp = r"[Tt][oe]xt (\S*) to" # Sometimes the image to text reads "Text" as "Toxt" lol

    #todo: find area to click based on average over some window
    with open(FOUND_CODES_FILE, "r") as f:
        foundCodes = set([code.strip() for code in f.readlines()])
    with open(FOUND_IMAGES_FILE, "r") as f:
        foundImages = set([src.strip() for src in f.readlines()])

    try:
        logging.info("Opening headless Firefox browser...")
        driver = webdriver.Firefox()
        logging.info(f"Navigating to {TWITTER_PAGE}...")
        driver.get(TWITTER_PAGE)
        while True:
            logging.info("----------Refreshing...----------")
            logging.info("Waiting for content to load...")
            start = time.perf_counter()
            driver.get(TWITTER_PAGE)
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '[aria-labelledby="accessible-list-1"]')
                    )
                )
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                driver.close()
                driver = webdriver.Firefox()
                logging.info("Restarting due to timeout")
                continue
            seconds = time.perf_counter() - start
            logging.info(f"Wait over. Took {seconds:0.4f}s to load tweets. Parsing and extracting...")
            time.sleep(.4) # do we need this?
            start = time.perf_counter()
            text = ""
            foundImagesCount = 0
            for img in driver.find_elements(By.TAG_NAME, "img"):
                foundImagesCount += 1
                src = img.get_attribute("src")
                if src not in foundImages:
                    if "media" in src and ("small" in src or "medium" in src):
                        logging.info(f"Found non-thumbnail media image src: {src}")
                        foundImages.add(src)
                        try:
                            response = requests.get(src)
                            image = Image.open(BytesIO(response.content))
                            extracted_text = pytesseract.image_to_string(image)
                        except Exception as e:
                            logging.info(f"Error in image text extraction: {e}")
                            continue
                        extracted_text = extracted_text.replace("\n", " ")
                        text += extracted_text
                        logging.info(f"Found image text: {extracted_text}")
            text += driver.page_source 
            foundCount = 0
            for m in re.findall(regexp, text):
                foundCount += 1
                if m not in foundCodes:
                    logging.info(f"Sending {m}")
                    sendSMSFirstRecipient(m)
                    foundCodes.add(m)
            seconds = time.perf_counter() - start
            logging.info(f"Took {seconds:0.4f}s to parse {foundCount} codes and {foundImagesCount} images")
    except KeyboardInterrupt:
        logging.info("Saving...")
        with open(FOUND_CODES_FILE, "w") as f:
            f.writelines("\n".join(foundCodes))
        with open(FOUND_IMAGES_FILE, "w") as f:
            f.writelines("\n".join(foundImages))
        sys.exit()

if __name__ == "__main__":
    runBot()


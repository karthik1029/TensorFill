import time
import yaml
import re
import numpy as np
import tensorflow_hub as hub
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Load config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 2)

# Load TensorFlow embedding model
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
used_labels = set()

# Minimum similarity threshold for matching
SIMILARITY_THRESHOLD = 0.75

# --- Normalize label text for matching ---
def normalize(text):
    return re.sub(r"[^a-zA-Z0-9 ]", "", text.strip().lower())

# --- Fill text input field based on semantic label match ---
def semantic_fill(concept, value):
    try:
        labels = [lbl for lbl in driver.find_elements(By.TAG_NAME, "label")
                  if lbl.get_attribute("for") and normalize(lbl.text) not in used_labels]
        label_texts = [lbl.text.strip() for lbl in labels]
        norm_texts = [normalize(txt) for txt in label_texts]

        embeddings = embed(norm_texts + [normalize(concept)])
        sims = np.inner(embeddings[:-1], embeddings[-1])
        best_idx = np.argmax(sims)

        if sims[best_idx] < SIMILARITY_THRESHOLD:
            print(f"⚠️ Weak match for '{concept}': Closest label is '{norm_texts[best_idx]}' with score {sims[best_idx]:.2f}")
            return

        best_label = labels[best_idx]
        input_id = best_label.get_attribute("for")
        input_elem = driver.find_element(By.ID, input_id)

        if input_elem.get_attribute("value").strip():
            print(f"⏩ Skipped '{norm_texts[best_idx]}' (already filled)")
            return

        input_elem.clear()
        time.sleep(0.5)
        input_elem.send_keys(value)

        used_labels.add(normalize(label_texts[best_idx]))
        print(f"✅ Filled '{norm_texts[best_idx]}' (web label) for concept '{concept}' (yaml key)")

    except Exception as e:
        print(f"⚠️ Semantic fill failed for '{concept}': {e}")

# --- Fill dropdowns that allow typing then ENTER ---
def semantic_type_dropdown(concept, value):
    try:
        labels = [lbl for lbl in driver.find_elements(By.TAG_NAME, "label")
                  if lbl.get_attribute("for") and normalize(lbl.text) not in used_labels]
        label_texts = [lbl.text.strip() for lbl in labels]
        norm_texts = [normalize(txt) for txt in label_texts]

        embeddings = embed(norm_texts + [normalize(concept)])
        sims = np.inner(embeddings[:-1], embeddings[-1])
        best_idx = np.argmax(sims)

        if sims[best_idx] < SIMILARITY_THRESHOLD:
            print(f"⚠️ Weak match for '{concept}': Closest label is '{norm_texts[best_idx]}' with score {sims[best_idx]:.2f}")
            return

        best_label = labels[best_idx]
        input_id = best_label.get_attribute("for")
        input_elem = driver.find_element(By.ID, input_id)

        if input_elem.get_attribute("value").strip():
            print(f"⏩ Skipped '{norm_texts[best_idx]}' (already filled)")
            return

        input_elem.clear()
        time.sleep(0.5)
        input_elem.send_keys(value)
        time.sleep(0.5)
        input_elem.send_keys(Keys.ENTER)
        time.sleep(0.5)

        used_labels.add(normalize(label_texts[best_idx]))
        print(f"✅ Filled '{norm_texts[best_idx]}' (web label) for concept '{concept}' (yaml key) (typed + ENTER)")

        if "visa sponsorship" in concept.lower() or "authorized to work" in concept.lower():
            time.sleep(1)

    except Exception as e:
        print(f"⚠️ Failed semantic dropdown fill for '{concept}': {e}")

# --- Main flow ---
try:
    driver.get(config["url"])
    time.sleep(2)

    try:
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#grnhse_iframe")))
        driver.switch_to.frame(iframe)
    except:
        pass

    field_map = {
        "first name": config["first_name"],
        "last name": config["last_name"],
        "email": config["email"],
        "phone": config["phone"],
        "LinkedIn": config["linkedin"],
        "pronouns": config["pronouns"],
        "desired salary": config["Desired Salary"],
        "availability": config["availability"],
        "relatives working in company": config["relatives"],
        "website": config["portfolio"]
    }
    for concept, value in field_map.items():
        semantic_fill(concept, value)

    dropdown_map = {
        "authorized to work in the United States": config["work_authorized"],
        "require visa sponsorship": config["need_sponsorship"],
        "school": config["school"],
        "degree": config["degree"],
        "discipline": config["discipline"],
        "are you a U.S. citizen": config["us_citizen"],
        "gender": config["gender"],
        "veteran status": config["veteran_status"],
        "disability status": config["disability_status"],
        "are you hispaniclatino": config["are you hispaniclatino"],
        "please identify your race": config["race"]
    }
    for concept, value in dropdown_map.items():
        semantic_type_dropdown(concept, value)

    driver.find_element(By.ID, "resume").send_keys(config["resume_path"])
    driver.find_element(By.ID, "cover_letter").send_keys(config["cover_letter_path"])

    print("✅ All fields filled. Please verify and submit manually.")
    time.sleep(250)

finally:
    driver.quit()

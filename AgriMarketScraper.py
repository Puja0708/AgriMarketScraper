from selenium import webdriver
from bs4 import BeautifulSoup
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inside your loop or function:



driver = webdriver.Chrome()

karnataka_major_crops = [
    "Tomato",
    "Onion",
    "Potato",
    "Maize",
    "Paddy(Dhan)(Common)",
    "Ragi (Finger Millet)",
    "Green Gram (Moong)",
    "Red Gram (Arhar/Tur)",
    "Groundnut",
    "Sunflower",
    "Cotton",
    "Chillies",
    "Turmeric",
    "Coriander",
    "Beans",
    "Brinjal",
    "Cabbage",
    "Carrot",
    "Cauliflower",
    "Coconut",
    "Ginger",
    "Garlic",
    "Sweet Potato",
    "Bajra (Pearl Millet)",
    "Wheat",
    "Sugarcane",
    "Mango",
    "Banana",
    "Grapes",
    "Sapota (Chikoo)",
    "Papaya",
    "Guava",
    "Coffee"
]

karnataka_districts = [
    "Bagalkot",
    "Ballari",
    "Belagavi",
    "Bengaluru Rural",
    "Bengaluru Urban",
    "Bidar",
    "Chamarajanagar",
    "Chikkaballapur",
    "Chikkamagaluru",
    "Chitradurga",
    "Dakshina Kannada",
    "Davanagere",
    "Dharwad",
    "Gadag",
    "Hassan",
    "Haveri",
    "Kalaburagi",
    "Kodagu",
    "Kolar",
    "Koppal",
    "Mandya",
    "Mysuru",
    "Raichur",
    "Ramanagara",
    "Shivamogga",
    "Tumakuru",
    "Udupi",
    "Uttara Kannada",
    "Vijayapura",
    "Yadgir",
    "Vijayanagara"
]


def fetch_data(state="Karnataka"):
    url = "https://agmarknet.gov.in/PriceAndArrivals/DatewiseCommodityReport.aspx"
    driver.get(url)

    # Select from dropdowns: state, commodity, date range etc
    # Loop through commodities of interest
    results = []
    for crop in karnataka_major_crops:  # e.g. ["Tomato","Onion","Ragi",...]


        # wait = WebDriverWait(driver, 15)
        state_dropdown = Select(driver.find_element(By.ID, "ddlState"))
        # state_dropdown.select_by_visible_text("Karnataka")

        # state_dropdown = Select(driver.find_element(By.ID, "cphBody_State"))

        # state_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "cphBody_State"))))

        # state_dropdown = Select(driver.find_element(By.ID, "cphBody_State"))
        state_dropdown.select_by_visible_text(state)

        market_dropdown = Select(driver.find_element(By.ID, "ddlMarket"))
        # market_dropdown.select_by_visible_text("Your Market Name Here")
        #
        # commodity_dropdown = Select(driver.find_element(By.ID, "cphBody_Commodity"))
        market_dropdown.select_by_visible_text(crop)

        # select_state(state)
        # select_commodity(crop)
        # apply_filters()
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", {"id":"ContentPlaceHolder1_gvData"})
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            results.append({
                "crop_name": crop,
                "district_name": cols[1].text.strip(),
                "market_selling_price": float(cols[7].text.strip())
            })
    driver.quit()
    print(json.dumps(results, indent=2))
    with open("karnataka_crop_market_prices.json", "w") as f:
        json.dumps(results, indent=2)

fetch_data()
from selenium import webdriver
from bs4 import BeautifulSoup
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inside your loop or function:



driver = webdriver.Chrome()

# karnataka_major_crops = [
#     "Tomato",
#     "Onion",
#     "Potato",
#     "Maize",
#     "Paddy(Dhan)(Common)",
#     "Ragi (Finger Millet)",
#     "Green Gram (Moong)",
#     "Red Gram (Arhar/Tur)",
#     "Groundnut",
#     "Sunflower",
#     "Cotton",
#     "Chillies",
#     "Turmeric",
#     "Coriander",
#     "Beans",
#     "Brinjal",
#     "Cabbage",
#     "Carrot",
#     "Cauliflower",
#     "Coconut",
#     "Ginger",
#     "Garlic",
#     "Sweet Potato",
#     "Bajra (Pearl Millet)",
#     "Wheat",
#     "Sugarcane",
#     "Mango",
#     "Banana",
#     "Grapes",
#     "Sapota (Chikoo)",
#     "Papaya",
#     "Guava",
#     "Coffee"
# ]
#
# karnataka_districts = [
#     "Bagalkot",
#     "Ballari",
#     "Belagavi",
#     "Bengaluru Rural",
#     "Bengaluru Urban",
#     "Bidar",
#     "Chamarajanagar",
#     "Chikkaballapur",
#     "Chikkamagaluru",
#     "Chitradurga",
#     "Dakshina Kannada",
#     "Davanagere",
#     "Dharwad",
#     "Gadag",
#     "Hassan",
#     "Haveri",
#     "Kalaburagi",
#     "Kodagu",
#     "Kolar",
#     "Koppal",
#     "Mandya",
#     "Mysuru",
#     "Raichur",
#     "Ramanagara",
#     "Shivamogga",
#     "Tumakuru",
#     "Udupi",
#     "Uttara Kannada",
#     "Vijayapura",
#     "Yadgir",
#     "Vijayanagara"
# ]

karnataka_districts = [
    "Bagalkot", "Ballari", "Belagavi", "Bengaluru", "Bengaluru Rural", "Bidar", "Chamarajanagar",
    "Chikkaballapur", "Chikkamagaluru", "Chitradurga", "Dakshina Kannada", "Davanagere", "Dharwad",
    "Gadag", "Hassan", "Haveri", "Kalaburagi", "Kodagu", "Kolar", "Koppal", "Mandya", "Mysuru",
    "Raichur", "Ramanagara", "Shivamogga", "Tumakuru", "Udupi", "Uttara Kannada", "Vijayapura",
    "Yadgir", "Vijayanagara"
]

karnataka_crops = [
     "Avare Dal", "Avare Whole", "Banana", "Beans", "Beetroot", "Bitter gourd",
    "Bottlegourd", "Brinjal", "Cabbage", "Capsicum", "Carrot", "Cauliflower", "Chayote", "Chillies Dry",
    "Chow Chow", "Cluster beans", "Coconut", "Coriander (Dhania)", "Cucumber", "Field Pea (Dry)",
    "Field Pea (Green)", "French Beans (Frasbean)", "Garlic", "Ginger(Dry)", "Green Chilli", "Green Gram (Moong)",
    "Guar", "Guava", "Knool Khol", "Ladies Finger", "Lemon", "Little gourd (Kundru)", "Maize", "Mango", "Onion",
    "Papaya", "Peas cod", "Potato", "Pumpkin", "Radish", "Ridgeguard(Tori)", "Snakeguard", "Sweet Potato",
    "Tamarind Fruit", "Tomato", "Water Melon", "Yam"
]



def fetch_data(state="Karnataka"):
    url = "https://agmarknet.gov.in/PriceAndArrivals/DatewiseCommodityReport.aspx"
    driver.get(url)

    # Select from dropdowns: state, commodity, date range etc
    # Loop through commodities of interest
    results = []
    for crop in karnataka_crops:  # e.g. ["Tomato","Onion","Ragi",...]

        state_dropdown = Select(driver.find_element(By.ID, "ddlState"))
        state_dropdown.select_by_visible_text(state)
        # market_dropdown = Select(driver.find_element(By.ID, "ddlMarket"))
        crop_dropdown_element = driver.find_element(By.ID, "ddlCommodity")
        crop_dropdown = Select(crop_dropdown_element)
        crop_dropdown.select_by_visible_text(crop)
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
    # print(json.dumps(results, indent=2))
    with open("karnataka_crop_market_prices.json", "w") as f:
        json.dumps(results, indent=2)

fetch_data()
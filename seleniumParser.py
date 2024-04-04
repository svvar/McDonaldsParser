from selenium import webdriver
from selenium.webdriver.common.by import By
import json

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options)

driver.get("https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html")
product_links = [e.get_attribute('href') for e in driver.find_elements(By.CLASS_NAME, 'cmp-category__item-link')]
products = []

for link in product_links:
    driver.get(link)

    driver.implicitly_wait(0.6)
    name = driver.find_element(By.CLASS_NAME, 'cmp-product-details-main__heading').text
    desc = driver.find_element(By.CLASS_NAME, 'cmp-product-details-main__description').text

    try:
        nutri_info = [e.get_attribute('innerText').strip().split()[0]
                      for e in driver.find_elements(By.CLASS_NAME, 'cmp-nutrition-summary__heading-primary-item')]

        calories = nutri_info[0]
        fat = nutri_info[1]
        carbs = nutri_info[2]
        protein = nutri_info[3]

        extra_info = (driver.find_element(By.CLASS_NAME, 'cmp-nutrition-summary__details-column-view-desktop')
                      .find_elements(By.CSS_SELECTOR, 'li > span.value > span.sr-only'))
        extra_info_values = [e.get_attribute('innerText').strip().split()[0] for e in extra_info]

        saturated_fat = extra_info_values[0]
        sugar = extra_info_values[1]
        salt = extra_info_values[2]
        portion = extra_info_values[3]

        product = {'name': name, 'desc': desc, 'calories': calories, 'fat': fat, 'carbs': carbs, 'protein': protein,
                   'saturated_fat': saturated_fat, 'sugar': sugar, 'salt': salt, 'portion': portion}
        products.append(product)
        print(f'{name} parsed successfully')

    except Exception as e:
        print(f'Error adding {name}. Message: {e}')
        continue

driver.quit()
json.dump(products, open('products.json', 'w'), ensure_ascii=False, indent=4)

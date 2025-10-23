# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Number of rows
n_rows = 15000

# Helper functions
def random_timestamp(start, end):
    delta = end - start
    random_days = random.randrange(delta.days)
    random_seconds = random.randrange(24 * 3600)
    ts = start + timedelta(days=random_days, seconds=random_seconds)
    return ts.strftime("%Y-%m-%d %H:%M:%S")

def random_category():
    categories = [
        "Clothing", "Footwear", "Electronics", "Jewelry", "Furniture",
        "Mobiles", "Home Decor", "Automotive", "Beauty", "Toys"
    ]
    main_cat = random.choice(categories)
    sub_cat = random.choice(["Men's", "Women's", "Kids'", "Unisex", "Smart", "Casual"])
    return f'["{main_cat} >> {sub_cat} Products"]'

def random_brand():
    brands = [
        "Alisha", "Samsung", "Nike", "Adidas", "Voylla", "FabHomeDecor",
        "Carrel", "Ladela", "Sicons", "Regular", "Apple", "Vivo"
    ]
    return random.choice(brands) if random.random() > 0.1 else ""

def random_price():
    retail = random.randint(500, 50000)
    discount = random.uniform(0.1, 0.8)
    discounted = int(retail * (1 - discount))
    # Ensure discounted <= retail
    discounted = min(discounted, retail)
    return retail, discounted, round(discount * 100, 2)

# Generate data
data = {
    "uniq_id": [str(uuid.uuid4()) for _ in range(n_rows)],
    "crawl_timestamp": [random_timestamp(
        datetime(2015, 12, 1), datetime(2016, 3, 31)
    ) for _ in range(n_rows)],
    "product_url": [f"https://flipkart.com/product/{i}" for i in range(n_rows)],
    "product_name": [f"{random.choice(['Solid', 'Printed', 'Smart', 'Casual'])} "
                     f"{random.choice(['Top', 'Shoes', 'Phone', 'Necklace', 'Sofa'])} "
                     f"{random.choice(['Men’s', 'Women’s', 'Kids'])}" for _ in range(n_rows)],
    "product_category_tree": [random_category() for _ in range(n_rows)],
    "pid": [f"{random.choice(['TOP', 'SHO', 'MOB', 'JWL', 'FUR'])}{random.randint(100000, 999999)}"
            for _ in range(n_rows)],
    "retail_price": [0] * n_rows,
    "discounted_price": [0] * n_rows,
    "image": [f"['https://flipkart.com/img/{i}.jpg']" if random.random() > 0.2 else ""
              for i in range(n_rows)],
    "is_FK_Advantage_product": [random.choice([True, False]) for _ in range(n_rows)],
    "description": [f"{random.choice(['Comfortable', 'Stylish', 'Durable'])} "
                    f"{random.choice(['cotton top', 'leather shoes', 'smartphone', 'gold necklace', 'wooden sofa'])} "
                    f"for {random.choice(['daily wear', 'party', 'office'])}." for _ in range(n_rows)],
    "product_rating": [random.choice([str(random.randint(1, 5)), "No rating available"])
                      for _ in range(n_rows)],
    "overall_rating": [random.choice([str(random.randint(1, 5)), "No rating available"])
                      for _ in range(n_rows)],
    "brand": [random_brand() for _ in range(n_rows)],
    "product_specifications": [f'{{"material": "{random.choice(["cotton", "leather", "plastic", "gold", "wood"])}"}}'
                              for _ in range(n_rows)],
    "discount_percentage": [0.0] * n_rows,
    "has_image": [False] * n_rows,
    "rating_available": [False] * n_rows,
    "is_clothing": [False] * n_rows,
    "brand_length": [0] * n_rows
}

# Create DataFrame
df = pd.DataFrame(data)

# Fill price-related columns
for i in range(n_rows):
    retail, discounted, discount_pct = random_price()
    df.loc[i, "retail_price"] = retail
    df.loc[i, "discounted_price"] = discounted
    df.loc[i, "discount_percentage"] = discount_pct

# Set derived columns
df["has_image"] = df["image"] != ""
df["rating_available"] = df["product_rating"] != "No rating available"
df["is_clothing"] = df["product_category_tree"].str.contains("Clothing", case=False)
df["brand_length"] = df["brand"].str.len().replace("", 0).astype(int)

# Introduce missing values
for col in ["retail_price", "discounted_price", "discount_percentage"]:
    mask = np.random.random(n_rows) < 0.05
    df.loc[mask, col] = np.nan

for col in ["brand", "description"]:
    mask = np.random.random(n_rows) < 0.03
    df.loc[mask, col] = "Unknown"

# Validate no negative price_diff
df['price_diff'] = df['retail_price'] - df['discounted_price']
if (df['price_diff'] < 0).any():
    raise ValueError("Negative price_diff detected!")
df = df.drop(columns=['price_diff'])  # Remove temp column

# Save to CSV
df.to_csv("/content/flipkart_sales_data.csv", index=False)
print("Dataset generated: flipkart_sales_data.csv with shape", df.shape)
import uvicorn
from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

@app.get("/all_products")
async def get_all():
    with open('products.json') as f:
        data = json.load(f)
    return data

@app.get("/products/{product_name}")
async def get_product(product_name: str):
    with open('products.json') as f:
        data = json.load(f)
    for product in data:
        if product['name'] == product_name.capitalize():
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/{product_name}/{field}")
async def get_product_field(product_name: str, field: str):
    with open('products.json') as f:
        data = json.load(f)
    for product in data:
        if product['name'] == product_name.capitalize():
            try:
                return product[field.lower()]
            except KeyError:
                raise HTTPException(status_code=404, detail="Field not found")
    raise HTTPException(status_code=404, detail="Product not found")


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
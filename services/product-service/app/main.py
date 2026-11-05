import os

from database import engine, init_db
from flask import Flask, jsonify, request
from models import Product
from sqlalchemy.orm import Session

app = Flask(__name__)

init_db()


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/products", methods=["GET"])
def get_products():
    category = request.args.get("category")
    with Session(engine) as session:
        query = session.query(Product).filter(
            Product.is_active == True  # noqa: E712, RUF100
        )
        if category:
            query = query.filter(Product.category == category)
        products = query.all()
        return (
            jsonify(
                [
                    {
                        "id": p.id,
                        "name": p.name,
                        "description": p.description,
                        "price": p.price,
                        "stock": p.stock,
                        "category": p.category,
                    }
                    for p in products
                ]
            ),
            200,
        )


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product or not product.is_active:
            return jsonify({"error": "Product not found"}), 404
        return (
            jsonify(
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "stock": product.stock,
                    "category": product.category,
                }
            ),
            200,
        )


@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")

    if not all([name, price]):
        return jsonify({"error": "Name and price are required"}), 400

    with Session(engine) as session:
        product = Product(
            name=name,
            description=data.get("description"),
            price=price,
            stock=data.get("stock", 0),
            category=data.get("category"),
        )
        session.add(product)
        session.commit()
        session.refresh(product)
        return (
            jsonify({"id": product.id, "message": "Product created successfully"}),
            201,
        )


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        product.is_active = False
        session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8002")))

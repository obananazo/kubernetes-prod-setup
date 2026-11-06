import os

import requests
from database import engine, init_db
from flask import Flask, jsonify, request
from models import Order, OrderItem
from sqlalchemy.orm import Session, joinedload

app = Flask(__name__)

PRODUCT_SERVICE_URL = os.environ.get("PRODUCT_SERVICE_URL", "http://product-service")

init_db()


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    user_id = data.get("user_id")
    items = data.get("items")  # [{"product_id": 1, "quantity": 2}]

    if not all([user_id, items]):
        return jsonify({"error": "user_id and items are required"}), 400

    total_price = 0.0
    order_items = []

    for item in items:
        product_id = item.get("product_id")
        quantity = item.get("quantity")

        response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
        if response.status_code != 200:
            return jsonify({"error": f"Product {product_id} not found"}), 404

        product = response.json()
        unit_price = product.get("price")
        total_price += unit_price * quantity
        order_items.append(
            {"product_id": product_id, "quantity": quantity, "unit_price": unit_price}
        )

    with Session(engine) as session:
        order = Order(user_id=user_id, total_price=total_price)
        session.add(order)
        session.flush()  # important to get the order.id before committing

        for item in order_items:
            session.add(OrderItem(order_id=order.id, **item))
        session.commit()
        return jsonify({"order_id": order.id, "total_price": total_price}), 201


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    with Session(engine) as session:
        orders = (
            session.query(Order)
            .options(joinedload(Order.items))
            .filter(Order.id == order_id)
            .all()
        )
        return (
            jsonify(
                [
                    {
                        "id": order.id,
                        "status": order.status,
                        "total_price": order.total_price,
                        "created_at": order.created_at.isoformat(),
                        "items": [
                            {
                                "product_id": item.product_id,
                                "quantity": item.quantity,
                                "unit_price": item.unit_price,
                            }
                            for item in order.items
                        ],
                    }
                    for order in orders
                ]
            ),
            200,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8003")))

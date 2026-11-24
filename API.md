# API Reference

All services are accessible via the Ingress Controller.

## Local development

Ingress is accessible via `http://localhost`.

> [!NOTE]
> Start the tunnel first: `minikube tunnel`

---

## User Service `/api/users`

### Register
```http
POST /api/users/register
```
```json
{
  "email": "john@example.com",
  "username": "johndoe",
  "password": "secret123",
  "full_name": "John Doe"
}
```
Response `201`:
```json
{ "message": "User registered successfully" }
```

---

### Login
```http
POST /api/users/login
```
```json
{
  "email": "john@example.com",
  "password": "secret123"
}
```
Response `200`:
```json
{ "access_token": "<JWT token>" }
```

---

### Get current user
```http
GET /api/users/me
Authorization: Bearer <token>
```
Response `200`:
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe"
}
```

---

## Product Service `/api/products`

### List products
```http
GET /api/products
GET /api/products?category=electronics
```
Response `200`:
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "A fast laptop",
    "price": 999.99,
    "stock": 10,
    "category": "electronics"
  }
]
```

---

### Get product
```http
GET /api/products/{id}
```
Response `200`:
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "A fast laptop",
  "price": 999.99,
  "stock": 10,
  "category": "electronics"
}
```

---

### Create product
```http
POST /api/products
```
```json
{
  "name": "Laptop",
  "price": 999.99,
  "stock": 10,
  "category": "electronics",
  "description": "A fast laptop"
}
```
Response `201`:
```json
{ "id": 1, "message": "Product created" }
```

---

### Delete product (soft delete)
```http
DELETE /api/products/{id}
```
Response `200`:
```json
{ "message": "Product deleted" }
```

---

## Order Service `/api/orders`

### Create order
```http
POST /api/orders
```
```json
{
  "user_id": 1,
  "items": [
    { "product_id": 1, "quantity": 2 }
  ]
}
```
Response `201`:
```json
{ "order_id": 1, "total_price": 1999.98 }
```

---

### Get orders by user
```http
GET /api/orders/{user_id}
```
Response `200`:
```json
[
  {
    "id": 1,
    "status": "pending",
    "total_price": 1999.98,
    "created_at": "2026-11-24T12:00:00",
    "items": [
      {
        "product_id": 1,
        "quantity": 2,
        "unit_price": 999.99
      }
    ]
  }
]
```

---

## Health & Metrics

| Endpoint | Description |
| -------- | ----------- |
| `/api/users/health` | User Service health check |
| `/api/products/health` | Product Service health check |
| `/api/orders/health` | Order Service health check |
| `/api/users/metrics` | Prometheus metrics |
| `/api/products/metrics` | Prometheus metrics |
| `/api/orders/metrics` | Prometheus metrics |

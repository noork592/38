#!/usr/bin/env python3
"""
Backend API smoke test for JK Products Factory Order Management ERP
Tests all core endpoints with real data as per the review request.
"""
import requests
import json
import sys
from typing import Dict, Any, Optional

# Backend URL from frontend/.env
BASE_URL = "https://clone-code-easy.preview.emergentagent.com/api"

# Test credentials from problem statement
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"
USER_USER = "user"
USER_PASS = "user123"

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, test_name: str):
        self.passed += 1
        print(f"{GREEN}✓{RESET} {test_name}")
    
    def add_fail(self, test_name: str, error: str):
        self.failed += 1
        self.errors.append(f"{test_name}: {error}")
        print(f"{RED}✗{RESET} {test_name}: {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}Test Summary{RESET}")
        print(f"{BLUE}{'='*60}{RESET}")
        print(f"Total: {total} | {GREEN}Passed: {self.passed}{RESET} | {RED}Failed: {self.failed}{RESET}")
        if self.errors:
            print(f"\n{RED}Failed Tests:{RESET}")
            for error in self.errors:
                print(f"  - {error}")
        return self.failed == 0

results = TestResults()

def test_auth_login_admin():
    """Test admin login with correct credentials"""
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": ADMIN_USER,
            "password": ADMIN_PASS
        })
        if response.status_code == 200:
            data = response.json()
            if "token" in data and "user" in data:
                results.add_pass("Admin login with correct credentials")
                return data["token"]
            else:
                results.add_fail("Admin login with correct credentials", "Missing token or user in response")
                return None
        else:
            results.add_fail("Admin login with correct credentials", f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        results.add_fail("Admin login with correct credentials", str(e))
        return None

def test_auth_login_wrong_password():
    """Test login with wrong password returns 401"""
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": ADMIN_USER,
            "password": "wrongpassword"
        })
        if response.status_code == 401:
            results.add_pass("Login with wrong password returns 401")
        else:
            results.add_fail("Login with wrong password returns 401", f"Expected 401, got {response.status_code}")
    except Exception as e:
        results.add_fail("Login with wrong password returns 401", str(e))

def test_auth_login_user():
    """Test user login with correct credentials"""
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": USER_USER,
            "password": USER_PASS
        })
        if response.status_code == 200:
            data = response.json()
            if "token" in data and "user" in data:
                results.add_pass("User login with correct credentials")
                return data["token"]
            else:
                results.add_fail("User login with correct credentials", "Missing token or user in response")
                return None
        else:
            results.add_fail("User login with correct credentials", f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        results.add_fail("User login with correct credentials", str(e))
        return None

def test_get_customers(token: str):
    """Test GET /api/customers - should have many seeded rows from customers.xlsx"""
    try:
        response = requests.get(f"{BASE_URL}/customers", headers={
            "Authorization": f"Bearer {token}"
        })
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                count = len(data)
                if count > 0:
                    results.add_pass(f"GET /customers returns {count} customers")
                    return data
                else:
                    results.add_fail("GET /customers", "Expected seeded customers, got empty list")
                    return []
            else:
                results.add_fail("GET /customers", f"Expected list, got {type(data)}")
                return []
        else:
            results.add_fail("GET /customers", f"Status {response.status_code}: {response.text}")
            return []
    except Exception as e:
        results.add_fail("GET /customers", str(e))
        return []

def test_get_products(token: str):
    """Test GET /api/products - should have 15 seeded products"""
    try:
        response = requests.get(f"{BASE_URL}/products", headers={
            "Authorization": f"Bearer {token}"
        })
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                count = len(data)
                if count == 15:
                    results.add_pass(f"GET /products returns 15 products")
                    return data
                else:
                    results.add_fail("GET /products", f"Expected 15 products, got {count}")
                    return data
            else:
                results.add_fail("GET /products", f"Expected list, got {type(data)}")
                return []
        else:
            results.add_fail("GET /products", f"Status {response.status_code}: {response.text}")
            return []
    except Exception as e:
        results.add_fail("GET /products", str(e))
        return []

def test_get_items(token: str):
    """Test GET /api/items - should have 388 seeded SKUs"""
    try:
        response = requests.get(f"{BASE_URL}/items", headers={
            "Authorization": f"Bearer {token}"
        })
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                count = len(data)
                if count == 388:
                    results.add_pass(f"GET /items returns 388 SKUs")
                    return data
                else:
                    results.add_fail("GET /items", f"Expected 388 SKUs, got {count}")
                    return data
            else:
                results.add_fail("GET /items", f"Expected list, got {type(data)}")
                return []
        else:
            results.add_fail("GET /items", f"Status {response.status_code}: {response.text}")
            return []
    except Exception as e:
        results.add_fail("GET /items", str(e))
        return []

def test_get_orders(token: str):
    """Test GET /api/orders - empty is fine"""
    try:
        response = requests.get(f"{BASE_URL}/orders", headers={
            "Authorization": f"Bearer {token}"
        })
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                count = len(data)
                results.add_pass(f"GET /orders returns {count} orders")
                return data
            else:
                results.add_fail("GET /orders", f"Expected list, got {type(data)}")
                return []
        else:
            results.add_fail("GET /orders", f"Status {response.status_code}: {response.text}")
            return []
    except Exception as e:
        results.add_fail("GET /orders", str(e))
        return []

def test_get_dashboard_stats(token: str):
    """Test GET /api/dashboard/summary or equivalent"""
    try:
        response = requests.get(f"{BASE_URL}/dashboard/summary", headers={
            "Authorization": f"Bearer {token}"
        })
        if response.status_code == 200:
            data = response.json()
            if "stats" in data:
                results.add_pass(f"GET /dashboard/summary returns stats")
                return data
            else:
                results.add_fail("GET /dashboard/summary", "Missing 'stats' in response")
                return None
        else:
            results.add_fail("GET /dashboard/summary", f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        results.add_fail("GET /dashboard/summary", str(e))
        return None

def test_get_settings(token: str):
    """Test GET /api/settings - should have overdue_days=15, edit_window_days=3"""
    try:
        response = requests.get(f"{BASE_URL}/settings", headers={
            "Authorization": f"Bearer {token}"
        })
        if response.status_code == 200:
            data = response.json()
            if "overdue_days" in data and "edit_window_days" in data:
                overdue = data.get("overdue_days")
                edit_window = data.get("edit_window_days")
                if overdue == 15 and edit_window == 3:
                    results.add_pass(f"GET /settings returns overdue_days=15, edit_window_days=3")
                else:
                    results.add_fail("GET /settings", f"Expected overdue_days=15, edit_window_days=3, got {overdue}, {edit_window}")
                return data
            else:
                results.add_fail("GET /settings", "Missing overdue_days or edit_window_days")
                return None
        else:
            results.add_fail("GET /settings", f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        results.add_fail("GET /settings", str(e))
        return None

def test_get_price_lists(token: str):
    """Test GET /api/price-lists - should have 3 seeded"""
    try:
        response = requests.get(f"{BASE_URL}/price-lists", headers={
            "Authorization": f"Bearer {token}"
        })
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                count = len(data)
                if count == 3:
                    results.add_pass(f"GET /price-lists returns 3 price lists")
                    return data
                else:
                    results.add_fail("GET /price-lists", f"Expected 3 price lists, got {count}")
                    return data
            else:
                results.add_fail("GET /price-lists", f"Expected list, got {type(data)}")
                return []
        else:
            results.add_fail("GET /price-lists", f"Status {response.status_code}: {response.text}")
            return []
    except Exception as e:
        results.add_fail("GET /price-lists", str(e))
        return []

def test_get_users(token: str):
    """Test GET /api/users - admin list"""
    try:
        response = requests.get(f"{BASE_URL}/users", headers={
            "Authorization": f"Bearer {token}"
        })
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                count = len(data)
                results.add_pass(f"GET /users returns {count} users")
                return data
            else:
                results.add_fail("GET /users", f"Expected list, got {type(data)}")
                return []
        else:
            results.add_fail("GET /users", f"Status {response.status_code}: {response.text}")
            return []
    except Exception as e:
        results.add_fail("GET /users", str(e))
        return []

def test_create_customer(token: str):
    """Test POST /api/customers - create a customer"""
    try:
        response = requests.post(f"{BASE_URL}/customers", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "name": "Test Customer ABC Ltd",
            "phone": "9876543210",
            "address": "123 Test Street",
            "city": "Mumbai",
            "location": "Andheri"
        })
        if response.status_code == 200:
            data = response.json()
            if "id" in data and data.get("name") == "Test Customer ABC Ltd":
                results.add_pass("POST /customers creates customer")
                return data
            else:
                results.add_fail("POST /customers", "Missing id or name mismatch in response")
                return None
        else:
            results.add_fail("POST /customers", f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        results.add_fail("POST /customers", str(e))
        return None

def test_create_order(token: str, customer_id: str, items: list):
    """Test POST /api/orders - create an order"""
    try:
        # Pick first item from items list
        if not items:
            results.add_fail("POST /orders", "No items available to create order")
            return None
        
        item = items[0]
        response = requests.post(f"{BASE_URL}/orders", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "customer_id": customer_id,
            "items": [{
                "product_name": item.get("product_name", "Side Stand"),
                "quantity": 100,
                "item_id": item.get("id"),
                "item_name": item.get("name")
            }],
            "notes": "Test order from smoke test"
        })
        if response.status_code == 200:
            data = response.json()
            if "id" in data and data.get("customer_id") == customer_id:
                results.add_pass("POST /orders creates order")
                return data
            else:
                results.add_fail("POST /orders", "Missing id or customer_id mismatch in response")
                return None
        else:
            results.add_fail("POST /orders", f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        results.add_fail("POST /orders", str(e))
        return None

def test_get_order(token: str, order_id: str):
    """Test GET /api/orders/{oid} - get order back"""
    try:
        response = requests.get(f"{BASE_URL}/orders/{order_id}", headers={
            "Authorization": f"Bearer {token}"
        })
        if response.status_code == 200:
            data = response.json()
            if data.get("id") == order_id:
                results.add_pass(f"GET /orders/{order_id} returns order")
                return data
            else:
                results.add_fail(f"GET /orders/{order_id}", "Order id mismatch")
                return None
        else:
            results.add_fail(f"GET /orders/{order_id}", f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        results.add_fail(f"GET /orders/{order_id}", str(e))
        return None

def test_delete_order(token: str, order_id: str):
    """Test DELETE /api/orders/{oid} - delete order"""
    try:
        response = requests.delete(f"{BASE_URL}/orders/{order_id}", headers={
            "Authorization": f"Bearer {token}"
        })
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                results.add_pass(f"DELETE /orders/{order_id} deletes order")
                return True
            else:
                results.add_fail(f"DELETE /orders/{order_id}", "Response not ok")
                return False
        else:
            results.add_fail(f"DELETE /orders/{order_id}", f"Status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        results.add_fail(f"DELETE /orders/{order_id}", str(e))
        return False

def test_delete_customer(token: str, customer_id: str):
    """Test DELETE /api/customers/{cid} - delete customer"""
    try:
        response = requests.delete(f"{BASE_URL}/customers/{customer_id}", headers={
            "Authorization": f"Bearer {token}"
        })
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                results.add_pass(f"DELETE /customers/{customer_id} deletes customer")
                return True
            else:
                results.add_fail(f"DELETE /customers/{customer_id}", "Response not ok")
                return False
        else:
            results.add_fail(f"DELETE /customers/{customer_id}", f"Status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        results.add_fail(f"DELETE /customers/{customer_id}", str(e))
        return False

def main():
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}JK Products Factory Order Management ERP - Backend Smoke Test{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    print(f"Backend URL: {BASE_URL}\n")
    
    # 1. Auth tests
    print(f"{YELLOW}=== Authentication Tests ==={RESET}")
    admin_token = test_auth_login_admin()
    test_auth_login_wrong_password()
    user_token = test_auth_login_user()
    
    if not admin_token:
        print(f"\n{RED}CRITICAL: Admin login failed. Cannot continue tests.{RESET}")
        sys.exit(1)
    
    print(f"\n{YELLOW}=== Core List Endpoints ==={RESET}")
    # 2. Core list endpoints
    customers = test_get_customers(admin_token)
    products = test_get_products(admin_token)
    items = test_get_items(admin_token)
    orders = test_get_orders(admin_token)
    test_get_dashboard_stats(admin_token)
    test_get_settings(admin_token)
    price_lists = test_get_price_lists(admin_token)
    users = test_get_users(admin_token)
    
    print(f"\n{YELLOW}=== CRUD Operations ==={RESET}")
    # 3. Create customer and order
    customer = test_create_customer(admin_token)
    if customer and items:
        order = test_create_order(admin_token, customer["id"], items)
        if order:
            # Note: GET /orders/{oid} endpoint doesn't exist in the API
            # But we can verify the order was created by listing all orders
            all_orders = test_get_orders(admin_token)
            if any(o.get("id") == order["id"] for o in all_orders):
                results.add_pass(f"Order {order['id']} found in orders list")
            else:
                results.add_fail(f"Order {order['id']} verification", "Order not found in orders list")
            # Delete order
            test_delete_order(admin_token, order["id"])
        # Delete customer
        test_delete_customer(admin_token, customer["id"])
    
    # Summary
    print()
    success = results.summary()
    
    if success:
        print(f"\n{GREEN}All tests passed!{RESET}")
        sys.exit(0)
    else:
        print(f"\n{RED}Some tests failed. Check errors above.{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()

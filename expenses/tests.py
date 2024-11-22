from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Expense
from datetime import date, datetime


class UserListCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {"username": "testuser", "email": "test@example.com"}

    def test_create_user(self):
        response = self.client.post("/api/v1/users/", self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], self.user_data["username"])

    def test_list_users(self):
        User.objects.create(username="testuser1", email="test1@example.com")
        User.objects.create(username="testuser2", email="test2@example.com")
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class ExpenseListCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", email="test@example.com")
        self.expense_data = {
            "user": self.user.id,
            "title": "Groceries",
            "amount": "50.00",
            "category": 1,
        }

    def test_create_expense(self):
        response = self.client.post("/api/v1/expenses/", self.expense_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.expense_data["title"])

    def test_list_expenses(self):
        Expense.objects.create(user=self.user, title="Groceries", amount=50.00, category=1)
        Expense.objects.create(user=self.user, title="Transport", amount=20.00, category=2)
        response = self.client.get("/api/v1/expenses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class ExpenseDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", email="test@example.com")
        self.expense = Expense.objects.create(user=self.user, title="Groceries", amount=50.00, category=1)

    def test_retrieve_expense(self):
        response = self.client.get(f"/api/v1/expenses/{self.expense.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Groceries")

    def test_update_expense(self):
        update_data = {"title": "Updated Groceries", "amount": "75.00"}
        response = self.client.patch(f"/api/v1/expenses/{self.expense.id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Groceries")
        self.assertEqual(response.data["amount"], "75.00")

    def test_delete_expense(self):
        response = self.client.delete(f"/api/v1/expenses/{self.expense.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expense.objects.filter(id=self.expense.id).exists())

class ExpenseByDateRangeViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", email="test@example.com")
        
        self.expense_first = Expense.objects.create(
            user=self.user,
            title="Groceries",
            amount=50.00,
            category=1,
        )
        self.expense_first.date = datetime(2024, 1, 15, 12, 0, 0)
        self.expense_first.save(update_fields=["date",])
        
        self.expense_second = Expense.objects.create(
            user=self.user,
            title="Transport",
            amount=20.00,
            category=2,
        )
        self.expense_second.date = datetime(2024, 1, 20, 18, 0, 0)
        self.expense_second.save(update_fields=["date",])
        
        self.expense_third = Expense.objects.create(
            user=self.user,
            title="Transport",
            amount=20.00,
            category=2,
        )
        self.expense_third.date = datetime(2024, 2, 20, 18, 0, 0)
        self.expense_third.save(update_fields=["date",])

    def test_get_expenses_by_date_range(self):
        response = self.client.get(f"/api/v1/expenses/{self.user.id}/2024-01-01/2024-01-31/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class CategorySummaryViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", email="test@example.com")
        
        self.expense_first = Expense.objects.create(
            user=self.user, 
            title="Groceries", 
            amount=50.00, 
            category=1,
        )
        self.expense_first.date = datetime(2024, 1, 15, 18, 0, 0)
        self.expense_first.save(update_fields=["date",])
        
        self.expense_second = Expense.objects.create(
            user=self.user, 
            title="Transport", 
            amount=20.00, 
            category=2, 
        )
        self.expense_second.date = datetime(2024, 1, 20, 18, 0, 0)
        self.expense_second.save(update_fields=["date",])
        
        self.expense_third = Expense.objects.create(
            user=self.user, 
            title="Dinner", 
            amount=30.00, 
            category=1,
        )
        self.expense_third.date = datetime(2024, 1, 25, 18, 0, 0)
        self.expense_third.save(update_fields=["date",])

    def test_category_summary(self):
        response = self.client.get(f"/api/v1/expenses/{self.user.id}/summary/2024/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["category"], "Food")
        self.assertEqual(response.data[0]["total"], "80.00")

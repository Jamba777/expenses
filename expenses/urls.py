from django.urls import path, register_converter

from .converters import DateConverter
from .views import (
    UserListCreateView, 
    ExpenseListCreateView, 
    ExpenseDetailView, 
    ExpenseByDateRangeView, 
    CategorySummaryView
)

register_converter(DateConverter, 'date')

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('expenses/<int:user_id>/<date:start_date>/<date:end_date>/', ExpenseByDateRangeView.as_view(), name='expense-by-date'),
    path('expenses/<int:user_id>/summary/<int:year>/<int:month>/', CategorySummaryView.as_view(), name='category-summary'),
]

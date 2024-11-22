from django.db import transaction
from django.db.models import Sum

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import User, Expense
from .serializers import (
    UserSerializer, 
    ExpenseSerializer, 
    ExpenseSummarySerializer,
    ExpenseByDateRangeSerializer
)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExpenseListCreateView(generics.ListCreateAPIView):
    queryset = Expense.objects.all().order_by("-date")
    serializer_class = ExpenseSerializer

class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)

        try:
            with transaction.atomic():
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
        except Exception as e:
            # Place for log exception str(e)
            raise APIException("An error occurred during the update")

        return Response(serializer.data)

class ExpenseByDateRangeView(generics.GenericAPIView):
    serializer_class = ExpenseByDateRangeSerializer
    
    @extend_schema(
        operation_id="retrieve_expenses_by_date_range",
        description="Retrieve all expenses for a user within a specific date range.",
        parameters=[
            OpenApiParameter(
                name="user_id", 
                description="User ID", 
                required=True, 
                type=int, 
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="end_date", 
                description="Date (YYYY-MM-DD format)", 
                required=True, 
                type=str, 
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="start_date", 
                description="Date (YYYY-MM-DD format)", 
                required=True, 
                type=str, 
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: ExpenseSerializer(many=True),
        },
    )
    def get(self, request, user_id, start_date, end_date):
        expenses = Expense.objects.filter(
            user_id=user_id, 
            date__date__range=[start_date, end_date]
        ).order_by("-date")
        
        serializer = self.get_serializer(expenses, many=True)
        return Response(serializer.data)


class CategorySummaryView(generics.GenericAPIView):
    serializer_class = ExpenseSummarySerializer
    
    @extend_schema(
        description="Retrieve total expenses per category for a given month for a user.",
        parameters=[
            OpenApiParameter(
                name="user_id", 
                description="User ID", 
                required=True, 
                type=int,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="year", 
                description="Year (YYYY format)", 
                required=True, 
                type=int,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="month", 
                description="Month (1-12)", 
                required=True, 
                type=int,
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: ExpenseSummarySerializer(many=True),
        },
    )
    def get(self, request, user_id, year, month):
        expenses = Expense.objects.filter(
            user_id=user_id, 
            date__year=year,
            date__month=month
        ).values('category').annotate(total=Sum('amount'))
        
        serializer = self.get_serializer(expenses, many=True)
        return Response(serializer.data)

from rest_framework import serializers

from .models import User, Expense

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ExpenseSerializer(serializers.ModelSerializer):
    readable_category = serializers.SerializerMethodField()
    
    class Meta:
        model = Expense
        fields = ['id', 'user', 'title', 'amount', 'date', 'category', 'readable_category']
        
    def get_readable_category(self, obj) -> str:
        return obj.get_category_display()

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Expense amount must be positive.")
        return value
    
class ExpenseByDateRangeSerializer(ExpenseSerializer):
    class Meta(ExpenseSerializer.Meta):
        fields = ['id', 'title', 'amount', 'date', 'category', 'readable_category']
    
class ExpenseSummarySerializer(serializers.Serializer):
    category = serializers.SerializerMethodField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)

    def get_category(self, obj) -> str:
        return Expense.CategoryChoices(obj['category']).label

from rest_framework import serializers


class Category(serializers.Serializer):
    slug = serializers.SlugField()
    title = serializers.CharField(max_length=255, db_index=True)

class MenuItem(serializers.Serializer):
    title = serializers.CharField(max_length=255, db_index=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = serializers.BooleanField(db_index=True)
    category = serializers.ForeignKey(Category)
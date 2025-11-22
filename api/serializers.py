from rest_framework import serializers
from mongo.models import Food, Recipe, RecipeIngredient

class FoodSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    unit = serializers.CharField(required=False)
    
    class Meta:
        model = Food
        fields = '__all__'

class RecipeIngredientSerializer(serializers.ModelSerializer):
    # This serializer will handle the food and quantity fields from the incoming JSON.
    # The 'food' field is a nested serializer.
    food = FoodSerializer()
    quantity = serializers.FloatField()
    
    class Meta:
        model = RecipeIngredient
        fields = ['food', 'quantity']
        
class RecipeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    servingsize = serializers.IntegerField(required=True, allow_null=False)
    description = serializers.CharField(required=False, allow_null=True)
    
    # This indicates that 'ingredients' is a list of RecipeIngredientSerializer objects.
    ingredients = RecipeIngredientSerializer(many=True, read_only=False)
    
    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        # Pop the ingredients data from the validated_data dictionary
        ingredients_data = validated_data.pop('ingredients')
        
        # Create the Recipe instance first using the remaining validated data
        recipe = Recipe.objects.create(**validated_data)
        
        # Now, iterate through the ingredients data to create RecipeIngredient instances
        for ingredient_data in ingredients_data:
            food_data = ingredient_data.pop('food')
            
            # Retrieve the Food instance using its ID
            try:
                food = Food.objects.get(id=food_data['id'])
            except Food.DoesNotExist:
                # Handle the case where the Food item doesn't exist
                raise serializers.ValidationError("Food item with ID {} not found.".format(food_data['id']))
            
            # Create the RecipeIngredient instance, linking it to the new recipe and found food
            RecipeIngredient.objects.create(
                food=food,
                recipe=recipe,  # Link the ingredient to the new recipe
                quantity=ingredient_data['quantity']
            )
        
        return recipe
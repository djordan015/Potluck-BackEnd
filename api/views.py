from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from mongo.models import Recipe, Sample, Food
from .serializers import FoodSerializer, RecipeSerializer

@api_view(['GET'])
def getFoods(request):
    foods = Food.objects.all()
    serializer = FoodSerializer(foods, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getFood(request):
    print("Request made from ")
    foods = Food.objects.first()
    serializer = FoodSerializer(foods, many=False)
    
    return Response(serializer.data)

@api_view(['POST'])
def addFood(request):
    serializer = FoodSerializer(data=request.data)
    print(f"attempting to post food {request.data}")
    
    if serializer.is_valid():
        name = serializer.validated_data.get('name')
        unit = serializer.validated_data.get('unit')
        
        if Food.objects.filter(name=name, unit=unit).exists():
            return Response(
                {"error": "This food item with the same unit already exists."}, 
                status=status.HTTP_409_CONFLICT
            )
        
        food_instace = serializer.save()
        
        print()
        return Response(serializer.data, status=status.HTTP_201_CREATED)    
    
    print()
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def addRecipe(request):
    serializer = RecipeSerializer(data=request.data)
    print("attempting to post recipe")
    print(request.data)
    
    if serializer.is_valid():
        name = serializer.validated_data.get('name')
        
        # CORRECTED: Check for existing Recipe, not Food
        if Recipe.objects.filter(name=name).exists(): 
            return Response(
                {"error": "This recipe already exists."}, 
                status=status.HTTP_409_CONFLICT
            )
        
        # You need to handle the creation of nested objects manually
        # The default .create() method of ModelSerializer does not handle nested writes
        name = serializer.validated_data['name']
        servingsize = serializer.validated_data['servingsize']
        description = serializer.validated_data.get('description', '')
        ingredients_data = serializer.validated_data.pop('ingredients')

        recipe = Recipe.objects.create(
            name=name,
            servingsize=servingsize,
            description=description
        )

        for ingredient_data in ingredients_data:
            food_data = ingredient_data.pop('food')
            # You must retrieve the Food object using its ID
            food = Food.objects.get(id=food_data['id'])
            RecipeIngredient.objects.create(
                food=food,
                recipe=recipe, # Link the ingredient to the new recipe
                quantity=ingredient_data['quantity']
            )

        # Now serialize the created recipe instance to return it
        created_recipe_serializer = RecipeSerializer(recipe)
        print("Recipe and its ingredients successfully created.")
        return Response(created_recipe_serializer.data, status=status.HTTP_201_CREATED)
    
    print("Serializer errors:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getRecipes(request):
    print("Attempting to fetch recipes\n")
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes, many = True)
    return Response(serializer.data)

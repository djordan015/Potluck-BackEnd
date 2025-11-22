from django.db import models
from django_mongodb_backend.fields import EmbeddedModelField, ArrayField
from django_mongodb_backend.models import EmbeddedModel


class Sample(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = "sample"
        managed = False

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'foods'
        managed = False


class RecipeIngredient(EmbeddedModel):
    """
    Embedded bridge between a Recipe and a Food.

    - Stored inside the Recipe document (no separate collection).
    - Holds the referenced Food primary key and recipe-specific fields
      such as quantity.
    """

    # store the referenced Food PK as a string (ObjectId or other PKs)
    food_pk = models.CharField(max_length=255)
    quantity = models.FloatField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.food_name or self.food_pk}"

    @property
    def food(self):
        """Resolve the Food object referenced by food_pk, or return None."""
        try:
            from .models import Food as FoodModel

            return FoodModel.objects.get(pk=self.food_pk)
        except Exception:
            return None

    @property
    def food_name(self):
        f = self.food
        return f.name if f else None
    
    class Meta:
        managed = False


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    servingsize = models.FloatField(default=1)
    description = models.CharField(max_length=400, blank=True)

    # embedded list of RecipeIngredient instances (stored inside Recipe doc)
    ingredients = ArrayField(EmbeddedModelField(RecipeIngredient), default=list)

    def __str__(self):
        return self.name

    def add_ingredient(self, food, quantity=0):
        """Helper to append an ingredient to this recipe.

        `food` can be a Food instance or a PK value.
        Call save() on the Recipe afterwards to persist changes.
        """
        pk = getattr(food, 'pk', food)
        ri = RecipeIngredient(food_pk=str(pk), quantity=quantity)
        self.ingredients.append(ri)
        return ri

    class Meta:
        db_table = 'recipes'
        managed = False

    


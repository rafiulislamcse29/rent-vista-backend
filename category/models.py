from django.db import models

# Create your models here.

class Category(models.Model):
  name=models.CharField(max_length=100)
  slug=models.SlugField(max_length=100)

  def __str__(self) -> str:
    return f"{self.name}"
  
  class Meta:
    verbose_name_plural = "categories"

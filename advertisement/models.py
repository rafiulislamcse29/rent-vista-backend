from django.db import models
from category.models import Category
from account.models import User
# Create your models here.



class RentAdvertisement(models.Model):
  title=models.CharField(max_length=100)
  description=models.TextField()
  price=models.DecimalField(max_digits=10,decimal_places=2)
  category=models.ForeignKey(Category,related_name='advertisements',on_delete=models.CASCADE)
  owner=models.ForeignKey(User,related_name='advertisements',on_delete=models.CASCADE)
  location=models.CharField(max_length=100,null=True)
  bedrooms=models.IntegerField(null=True)
  amenities=models.CharField(max_length=100,null=True)
  is_approved=models.BooleanField(default=False)
  request_accepted = models.BooleanField(default=False)
  created_at=models.DateTimeField(auto_now_add=True)
  image=models.ImageField(upload_to='advertisement/images/')

  def __str__(self) -> str:
    return self.title
  
class RentRequest(models.Model):
  advertisement=models.ForeignKey(RentAdvertisement,related_name='rent_requests', on_delete=models.CASCADE)
  requester=models.ForeignKey(User,related_name='rent_requests', on_delete=models.CASCADE)
  is_accepted = models.BooleanField(default=False)
  created_at=models.DateTimeField(auto_now_add=True)
  
  def __str__(self) -> str:
    return self.advertisement.title
  
  
class Favourite(models.Model):
  user=models.ForeignKey(User,related_name='favorites',on_delete=models.CASCADE)
  advertisement=models.ForeignKey(RentAdvertisement,related_name='favourites',on_delete=models.CASCADE)
  created_at=models.DateTimeField(auto_now_add=True)

  def __str__(self) -> str:
    return self.user.first_name
  
STAR_CHOICES=[
  ('⭐','⭐'),
  ('⭐⭐','⭐⭐'), 
  ('⭐⭐⭐','⭐⭐⭐'),
  ('⭐⭐⭐⭐','⭐⭐⭐⭐'),
  ('⭐⭐⭐⭐⭐','⭐⭐⭐⭐⭐'),
]

class Review(models.Model):
  advertisement=models.ForeignKey(RentAdvertisement,related_name='reviews',on_delete=models.CASCADE)
  reviewer=models.ForeignKey(User,related_name="reviews",on_delete=models.CASCADE)
  comment=models.TextField()
  rating=models.CharField(choices=STAR_CHOICES,max_length=20)
  created_at=models.DateTimeField(auto_now_add=True)
  
  def __str__(self) -> str:
    return self.advertisement.title
    
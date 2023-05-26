from django.db import models

# Create your models here.
class books:
    
    title : str
    author : str
    cap : str
    stars : str
    price : float
    img : str
    
    def __init__(self):
        
        books.img = "No-Image-.png"
        books.price = 10
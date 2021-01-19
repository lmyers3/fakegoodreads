from django.db import models

# Create your models here.
class Book:
    def __init__(self, bookInfo):

        self.title = bookInfo["title"]
        self.authors = bookInfo["authors"]
        self.imgUrl = bookInfo["imgUrl"]
        self.summary = bookInfo["summary"]
        self.id = bookInfo["id"]

def authorsToString(s):
    authorString = ', '.join(s)
    return authorString

class Review(models.Model):
    book_id = models.CharField(max_length=20)
    username = models.ForeignKey('login.User', on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)


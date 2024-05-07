from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
class Book(models.Model):
    book_name = models.CharField(max_length=120)
    author_name = models.CharField(max_length=60)
    quantity = models.IntegerField()
    objects = models.Manager()


    def __str__(self):
        return self.book_name + '-' + self.author_name


# IssuedItem model to store issued book details
class IssuedItem(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateField(default=date.today(), blank=False)
    return_date = models.DateField(blank=True, null=True)

    # property to get book name
    @property
    def book_name(self):
        return self.book_id.book_name

    # property to get author name
    @property
    def username(self):
        return self.user_id.username

    def __str__(self):
        return self.book_id.book_name + ' issued by ' + self.user_id.first_name + ' on ' + str(self.issue_date)
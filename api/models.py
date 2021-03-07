from django.db import models

class Todo(models.Model): 
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    is_complete = models.BooleanField(default=False)
    # auto_now updates TS with each update 
    time_created = models.DateTimeField(auto_now=True)
    # auto_now_add TS when object created - all other auto_*
    # are mutually exclusive.
    last_modified = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['time_created']


    def __str__(self): 
        return self.title
    
    
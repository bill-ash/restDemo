from django.db import models
# from django.contrib.auth.models import User

class Todo(models.Model): 
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    is_complete = models.BooleanField(default=False)
    # auto_now updates TS with each update 
    time_created = models.DateTimeField(auto_now=True)
    # auto_now_add TS when object created - all other auto_*
    # are mutually exclusive.
    last_modified = models.DateTimeField(auto_now_add=True)
    
    # Not sure why you wouldn't import the User model class...
    owner = models.ForeignKey('auth.user', related_name='todo', on_delete=models.CASCADE)

    class Meta: 
        ordering = ['last_modified']

    def save(self, *args, **kwargs):
        # Overide default save to preform additional functions.
        return super(Todo, self).save(*args, **kwargs)

    def __str__(self): 
        return self.title
    
    
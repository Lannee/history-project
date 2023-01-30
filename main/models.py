from django.db import models

class Article(models.Model):
    title = models.CharField(max_length = 255)
    isBigFormat = models.BooleanField(default=False)
    author = models.ForeignKey('Author', on_delete=models.PROTECT)
    description = models.TextField()
    text = models.TextField()
    likes = models.IntegerField()
    date = models.DateField(auto_now_add = True)
    images = models.ManyToManyField('Images')

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return "article_" + str(self.id)   

class Images(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='articles')

    def __str__(self):
        return self.name

class Author(models.Model):
    fullName = models.CharField(max_length = 255)
    photo = models.ImageField(upload_to='authors')

    def __str__(self):
        return self.fullName        
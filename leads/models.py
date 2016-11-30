from django.db import models


class Skills(models.Model):
    skill = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.skill


class Lead(models.Model):
    # project_id, title, description, skills, url
    project_id = models.IntegerField(blank=True, null=True)  # add unique=True
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    # skills = models.OneToOneField(Skills)
    url = models.URLField(blank=True)

    # owner = models.ForeignKey('auth.User', related_name='leads', on_delete=models.CASCADE, blank=True)

    class Meta:
        ordering = ('project_id',)

    def __str__(self):
        return str(self.project_id)

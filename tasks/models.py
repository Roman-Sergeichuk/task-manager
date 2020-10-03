from django.conf import settings
from django.db import models
from django.utils import timezone


class Task(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'new'),
        ('PLANNED', 'planned'),
        ('IN_PROGRESS', 'in progress'),
        ('COMPLETED', 'completed'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    completion_date = models.DateField(null=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='NEW')

    # def save(self):
    #     TaskHistory.objects.create(task_id=self.pk,
    #                                title=self.title,
    #                                description=self.description,
    #                                author=self.author,
    #                                status=self.status,
    #                                completion_date=self.completion_date)
    #     super(Task, self).save()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class TaskHistory(models.Model):
    task_id = models.IntegerField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    completion_date = models.DateField(null=True)
    status = models.CharField(max_length=11)

    class Meta:
        ordering = ['-pk']







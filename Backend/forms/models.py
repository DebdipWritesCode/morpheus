from django.db import models
from django.db.models import JSONField
from django.utils.timezone import now

# Create your models here.
class UserRole(models.TextChoices):
  ADMIN = "Admin", "admin"
  USER = "User", "user"
  
class QuestionType(models.TextChoices):
  TEXT = 'text', 'Text'
  CHECKBOX = 'checkbox', 'Checkbox'
  DROPDOWN = 'dropdown', 'Dropdown'
  RANKING = 'ranking', 'Ranking'
  LINEAR_SCALE = 'linear_scale', 'Linear Scale'
  DATE_PICKER = 'date_picker', 'Date Picker'
  TIME_PICKER = 'time_picker', 'Time Picker'
  FILE_UPLOAD = 'file_upload', 'File Upload'
  MATRIX = 'matrix', 'Matrix'
  IMAGE = 'image', 'Image'
  SLIDER = 'slider', 'Slider'
  SIGNATURE = 'signature', 'Signature'
  COLOR_PICKER = 'color_picker', 'Color Picker'
  LOCATION = 'location', 'Location'
  PERCENTAGE_ALLOCATION = 'percentage_allocation', 'Percentage Allocation'
    
class User(models.Model):
  id = models.AutoField(primary_key=True)
  username = models.CharField(max_length=100)
  email = models.EmailField(max_length=100)
  password = models.CharField(max_length=100)
  role = models.CharField(
    max_length=5,
    choices=UserRole.choices,
    default=UserRole.USER
  )
  created_at = models.DateTimeField(default=now)
  
class Form(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=255)
  description = models.TextField()
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forms')
  created_at = models.DateTimeField(default=now)
  
class Question(models.Model):
  id = models.AutoField(primary_key=True)
  form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='questions')
  type = models.CharField(
    max_length=25,
    choices=QuestionType.choices,
    default=QuestionType.TEXT
  )
  question_text = models.TextField()
  options = JSONField(
    null = True,
    blank = True
  )
  created_at = models.DateTimeField(default=now)
  
class Response(models.Model):
  id = models.AutoField(primary_key=True)
  form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='responses')
  submitted_at = models.DateTimeField(default=now)
  
class Answer(models.Model):
  id = models.AutoField(primary_key=True)
  response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='answers')
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
  answer = models.JSONField()
from rest_framework import serializers
from .models import User, Form, Question, Response, Answer

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "username", "email", "role", "created_at"]
    
class FormSerializer(serializers.ModelSerializer):
  created_by = UserSerializer(read_only=True)
  
  class Meta:
    model = Form
    fields = ["id", "title", "description", "created_by", "created_at"]
    
class QuestionSerializer(serializers.ModelSerializer):
  form = serializers.PrimaryKeyRelatedField(queryset=Form.objects.all())
  
  class Meta:
    model = Question
    fields = ["id", "form", "type", "question_text", "options", "created_at"]
    
class ResponseSerializer(serializers.ModelSerializer):
  form = serializers.PrimaryKeyRelatedField(queryset=Form.objects.all())
  
  class Meta:
    model = Response
    fields = ["id", "form", "submitted_at"]    
    
class AnswerSerializer(serializers.ModelSerializer):
  response = serializers.PrimaryKeyRelatedField(queryset=Response.objects.all())
  question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
  
  class Meta:
    model = Answer
    fields = ["id", "response", "question", "answer"]
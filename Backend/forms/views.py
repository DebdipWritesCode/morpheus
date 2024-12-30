from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .utils.question_validator import validate_questions
from .utils.answer_validator import validate_answers
from .utils.analytics import aggregate_text_answers, aggregate_dropdown_answers, aggregate_checkbox_answers
from .serializers import FormSerializer

from django.contrib.auth.models import User as AuthUser
from .models import User, UserRole, Question, QuestionType, Form, Response as ResponseModel, Answer
from rest_framework_simplejwt.tokens import RefreshToken

class SignupView(APIView):
  def post(self, request):
    data = request.data
    try:
      auth_user = AuthUser.objects.create_user(
        username = data['username'],
        email = data['email'],
        password = data['password']
      )
      
      user = User.objects.create(
        username=data['username'],
        email=data['email'],
        password=auth_user.password,
        role=data.get('role', 'user')
      )
      return Response({
        "message": "User created successfully",
      }, status=status.HTTP_201_CREATED)
    except Exception as e:
      return Response({
        "error": str(e)
      }, status=status.HTTP_400_BAD_REQUEST)
      
class LoginView(APIView):
  def post(self, request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    
    user = authenticate(username=username, password=password)
    if not user:
      return Response({
        "error": "Invalid credentials"
      }, status=status.HTTP_401_UNAUTHORIZED)
      
    try:
      custom_user = User.objects.get(email=user.email)
    except User.DoesNotExist:
      return Response({
        "error": "User not found"
      }, status=status.HTTP_404_NOT_FOUND)
      
    refresh = RefreshToken.for_user(user)
    
    access_token = refresh.access_token
    access_token["id"] = custom_user.id
    access_token["role"] = custom_user.role
    access_token["username"] = custom_user.username
    access_token["email"] = custom_user.email
    
    return Response({
      "message": "Login successful",
      "access_token": str(access_token),
    }, status=status.HTTP_200_OK)
    
class CreateFormView(APIView):
  def post(self, request):
    data = request.data
    user_id = data.get('user_id')
    title = data.get('title')
    description = data.get('description')
    questions = data.get('questions')
    
    user = User.objects.get(id=user_id)
    if user.role != UserRole.ADMIN:
      return Response({
        "error": "You are not authorized to create forms"
      }, status=status.HTTP_403_FORBIDDEN)
    
    if not title:
      return Response({
        "error": "Title is required"
      }, status=status.HTTP_400_BAD_REQUEST)
      
    if not questions:
      return Response({
        "error": "At least one question is required"
      }, status=status.HTTP_400_BAD_REQUEST)
      
    try:
      validate_questions(questions)
    except Exception as e:
      return Response({
        "error": str(e)
      }, status=status.HTTP_400_BAD_REQUEST)
    
    form_data = {
      "title": title,
      "description": description,
      "created_by": user.id
    }
    
    form_serializer = FormSerializer(data=form_data)
    if form_serializer.is_valid():
      form = form_serializer.save()
      
      for question in questions:
        Question.objects.create(
          form = form.id,
          question_text = question.get('question_text'),
          type = question.get('type'),
          options = question.get('options', [])
        )
      
      return Response({
        "message": "Form and questions created successfully"
      }, status=status.HTTP_201_CREATED)
    else:
      return Response({
        "error": form_serializer.errors
      }, status=status.HTTP_400_BAD_REQUEST)
      
class GetFormsView(APIView):
  def get(self, request):
    user_id = request.query_params.get("user_id")
    
    try:
      user = User.objects.get(id=user_id)
      
      if not user:
        return Response({
          "error": "User not found"
        }, status=status.HTTP_404_NOT_FOUND)
      
      if user.role != UserRole.ADMIN:
        return Response({
          "error": "You are not authorized to view forms"
        }, status=status.HTTP_403_FORBIDDEN)

      forms = Form.objects.filter(created_by=user_id)
      
      form_data = FormSerializer(forms, many=True).data
      
      return Response({
        "message": "Forms retrieved successfully",
        "forms": form_data
      }, status=status.HTTP_200_OK)
    
    except User.DoesNotExist:
      return Response({
        "error": "User not found"
      }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
      return Response({
        "error": str(e)
      }, status=status.HTTP_400_BAD_REQUEST)

class SubmitResponseView(APIView):
  def post(self, request):
    data = request.data
    form_id = data.get('form_id')
    answers = data.get('answers')
    
    if not form_id:
      return Response({
        "error": "Form ID is required"
      }, status=status.HTTP_400_BAD_REQUEST)
      
    if not answers:
      return Response({
        "error": "Answers are required"
      }, status=status.HTTP_400_BAD_REQUEST)
      
    try:
      form = Form.objects.get(id=form_id)
    except Form.DoesNotExist:
      return Response({
        "error": "Form not found"
      }, status=status.HTTP_404_NOT_FOUND)
      
    try:
      validate_answers(answers, form_id)
    except Exception as e:
      return Response({
        "error": str(e)
      }, status=status.HTTP_400_BAD_REQUEST)
      
    response = ResponseModel.objects.create(form=form.id)
    
    for answer in answers:
      Answer.objects.create(
        response = response.id,
        question = answer.get('question_id'),
        answer = answer.get('answer')
      )
    
    return Response({
      "message": "Response submitted successfully"
    }, status=status.HTTP_201_CREATED)
    
class ShowAnalyticsView(APIView):
  def get(self, request, form_id):
    try:
      form = Form.objects.get(id=form_id)
    except Form.DoesNotExist:
      return Response({
        "error": "Form not found"
      }, status=status.HTTP_404_NOT_FOUND)
    
    total_responses = ResponseModel.objects.filter(form=form_id).count()
    
    if total_responses == 0:
      return Response({
        "message": "No responses found for the form",
        "total_responses": total_responses,
        "text_aggregate": {},
        "dropdown_aggregate": {},
        "checkbox_aggregate": {}
      }, status=status.HTTP_200_OK)
      
    text_questions = Question.objects.filter(form=form_id, type=QuestionType.TEXT).values_list('id', flat=True)
    dropdown_questions = Question.objects.filter(form=form_id, type=QuestionType.DROPDOWN).values_list('id', flat=True)
    checkbox_questions = Question.objects.filter(form=form_id, type=QuestionType.CHECKBOX).values_list('id', flat=True)
    
    text_aggregate = {}
    dropdown_aggregate = {}
    checkbox_aggregate = {}
    
    if text_questions:
        text_answers = Answer.objects.filter(question_id__in=text_questions).values_list("answer", flat=True)
        text_aggregate = aggregate_text_answers(text_answers)

    if checkbox_questions:
        checkbox_answers = Answer.objects.filter(question_id__in=checkbox_questions).values_list("answer", flat=True)
        checkbox_aggregate = aggregate_checkbox_answers(checkbox_answers)

    if dropdown_questions:
        dropdown_answers = Answer.objects.filter(question_id__in=dropdown_questions).values_list("answer", flat=True)
        dropdown_aggregate = aggregate_dropdown_answers(dropdown_answers)

    return Response({
        "message": "Analytics retrieved successfully.",
        "total_responses": total_responses,
        "text_aggregate": text_aggregate,
        "checkbox_aggregate": checkbox_aggregate,
        "dropdown_aggregate": dropdown_aggregate
    }, status=status.HTTP_200_OK)
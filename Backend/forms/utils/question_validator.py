from rest_framework.exceptions import ValidationError
from ..models import QuestionType

def validate_question_data(question):
  """ Validate each question based on its type and structure """
  question_text = question.get("question_text")
  question_type = question.get("type")
  options = question.get("options")
  
  if not question_text:
    raise ValidationError("Question text is required")
  if question_type not in QuestionType.values:
    raise ValidationError("Invalid question type")
  
  if question_type in [QuestionType.CHECKBOX, QuestionType.DROPDOWN, QuestionType.RANKING, QuestionType.MATRIX, QuestionType.PERCENTAGE_ALLOCATION]:
    if not options:
      raise ValidationError(f"Options are required for {question_type} question")
    if not isinstance(options, list) or len(options) < 2:
      raise ValidationError(f"Options should be a list with at least 2 items")
  elif question_type in [QuestionType.LINEAR_SCALE, QuestionType.SLIDER]:
    if not options or len(options) != 2:
      raise ValidationError(f"Options should be a list with exactly 2 items for {question_type} question")
    min_value, max_value = options
    if not isinstance(min_value, (int, float)) or not isinstance(max_value, (int, float)):
      raise ValidationError("Options should be numbers")
    if min_value >= max_value:
      raise ValidationError("Minimum value should be less than maximum value")
  else:
    if options:
      raise ValidationError(f"Options are not allowed for {question_type} question")
    
def validate_questions(questions):
  """ Validate the questions list """
  if not isinstance(questions, list):
    raise ValidationError("Questions should be a list")
  if len(questions) < 1 or len(questions) > 100:
    raise ValidationError("Questions should be between 1 and 100")
  
  for question in questions:
    validate_question_data(question)
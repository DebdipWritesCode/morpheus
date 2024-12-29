from rest_framework.exceptions import ValidationError
from ..models import QuestionType, Question

def validate_answers(answers, form_id):
  """ Validates each answer based on the question type """
  for answer in answers:
    question_id = answer.get("question_id")
    answer_data = answer.get("answer")
    
    if not question_id:
      raise ValidationError("Question ID is required")
    if answer_data is None:
      raise ValidationError("Answer is required")
    
    try:
      question = Question.objects.get(id=question_id, form_id=form_id)
    except Question.DoesNotExist:
      raise ValidationError(f"Question with ID {question_id} does not exist in the form")
    
    if question.type in [
      QuestionType.TEXT,
      QuestionType.DROPDOWN,
      QuestionType.DATE_PICKER,
      QuestionType.TIME_PICKER,
      QuestionType.LINEAR_SCALE,
      QuestionType.SLIDER,
      QuestionType.COLOR_PICKER,
      QuestionType.LOCATION,
    ]:
      if not isinstance(answer_data, str):
        raise ValidationError("Answer should be a string")
    else:
      if not isinstance(answer_data, dict):
        raise ValidationError(f"Answer should be an object for {question.type} question")
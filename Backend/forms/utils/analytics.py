from collections import Counter
import json

def aggregate_text_answers(answers):
  """
  Aggregates text answers to find the top 5 most common words (>=5 characters).
  """
  word_counter = Counter()
  for answer in answers:
    words = str(answer).split()
    filtered_words = [word for word in words if len(word) >= 5]
    word_counter.update(filtered_words)
    
  most_common_words = word_counter.most_common(5)
  aggregate = {word: count for word, count in most_common_words}
  others_count = sum(word_counter.values()) - sum(aggregate.values())
  
  if others_count > 0:
    aggregate["Others"] = others_count
  return aggregate

def aggregate_dropdown_answers(answers):
  """
  Aggregates dropdown answers to find the top 5 most selected options.
  """
  options_counter = Counter(answers)
  most_common_options = options_counter.most_common(5)
  aggregate = {option: count for option, count in most_common_options}
  others_count = sum(options_counter.values()) - sum(aggregate.values())
  
  if others_count > 0:
    aggregate["Others"] = others_count
  return aggregate

def aggregate_checkbox_answers(answers):
  """
  Aggregates checkbox answers to find the top 5 most common option combinations.
  """
  combination_counter = Counter()
  for answer in answers:
    try:
        options = json.dumps(answer, sort_keys=True)  # Ensure consistent order for comparison
        combination_counter.update([options])
    except:
        continue
  
  most_common = combination_counter.most_common(5)
  aggregate = {json.loads(option): count for option, count in most_common}
  others_count = sum(combination_counter.values()) - sum(aggregate.values())
  
  if others_count > 0:
      aggregate["Others"] = others_count
  return aggregate
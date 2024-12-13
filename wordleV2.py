import requests
import random
from tqdm import tqdm
from math import log
from english_words import get_english_words_set
import numpy as np
from itertools import product
import time

LETTER_FREQUENCY_ORDER = "etaonrishdlfcmugypwbvkjxzq"
CORRECT, PRESENT, ABSENT = "correct", "present", "absent"
GUESS_COUNT = 0

def try_guess(guess: str, text_size: int) -> list:
  # Add counter
  global GUESS_COUNT
  GUESS_COUNT += 1
  
  # get the pattern return from the API
  query = f"https://wordle.votee.dev:8000/random?guess={guess}&seed={SEED}&size={text_size}"
  r = requests.get(query)
  result = [check["result"] for check in r.json()]
  return result

def filter_allowed_guesses(guess: str, pattern: list, allowed_guesses: list) -> list:
  # filter all the words that match the pattern
  remain_allowed_guesses = []
  allowed_guesses = set(allowed_guesses)
  for word in allowed_guesses:
    should_remain = True
    for i, result in enumerate(pattern):
      if (result == ABSENT and guess[i] in word) or \
      (result == PRESENT and guess[i] not in word) or \
      (result == CORRECT and guess[i] != word[i]):
        should_remain = False
    if should_remain:
      remain_allowed_guesses.append(word)
  return remain_allowed_guesses
    

def calculate_entropy(word, all_pattern: list, allowed_guesses: list)-> float:
  # Calculate the entropy of distribution across all pattern for a particular word with 
  # the formular of information theory E = sum(px*log(1/px))
  # px is the probability of the pattern
  entropy = 0
  for pattern in all_pattern:
    # get all the words that match the pattern
    word_basket = filter_allowed_guesses(word, pattern, allowed_guesses)
    if len(word_basket) > 0:
      px = len(word_basket)/len(allowed_guesses)
      entropy += px * log(1/px,2)

  return entropy

# get the best guess from the allowed guesses list, the best guess is the word that give the highest entropy.
# higher entropy means that the word will help narrow down the possible solutions more effectively.
def get_best_guess(allowed_guesses: list, all_pattern: list)-> int:
  highest_entropy = 0
  result_index = 0
  for i, word in enumerate(tqdm(allowed_guesses)):
    entropy = calculate_entropy(word, all_pattern, allowed_guesses)
    if entropy > highest_entropy:
      highest_entropy = entropy
      result_index = i

  return result_index

def find_correct_word(guess: str, allowed_guesses: list, all_pattern: list) -> str:
  if len(allowed_guesses) == 1:
    return allowed_guesses[0]
  
  if len(allowed_guesses) == 0:
    return "NO_SOLUTION_FOUND"  # Return special value when no solution is found

  guess_pattern = try_guess(guess, len(guess))
  if is_correct_word(guess_pattern):
    return guess
  else:
    remain_words = filter_allowed_guesses(guess, guess_pattern, allowed_guesses)
    best_guess_index = get_best_guess(remain_words, all_pattern)
    if len(remain_words) == 0:
      return "NO_SOLUTION_FOUND"
    best_guess = remain_words.pop(best_guess_index)
    return find_correct_word(best_guess, remain_words, all_pattern)

def is_correct_word(pattern: list) -> bool:
  return set(pattern) == set(["correct"])

def solve_wordle(text_size: int) -> tuple[str, int]:
  # Reset counter at start of each solve
  global GUESS_COUNT
  GUESS_COUNT = 0
  
  all_pattern = list(product(*[[ABSENT ,PRESENT ,CORRECT]]*text_size)) # "absent": 0, "present": 1, "correct": 2,
  allowed_guesses = []

  for word in WORD_LIST:
    if len(word) == text_size and word not in allowed_guesses:
      allowed_guesses.append(word)

  first_guess = LETTER_FREQUENCY_ORDER[:text_size]
  answer = find_correct_word(guess = first_guess, allowed_guesses = allowed_guesses, all_pattern = all_pattern)

  return answer, GUESS_COUNT

if __name__ == "__main__":
    total_guesses = 0
    num_rounds = 10 # Set number of rounds to test
    text_size = 5     # Set word length
    not_found = 0
    print(f"Testing Wordle solver for {num_rounds} rounds with {text_size}-letter words...")
    
    results = []
    start_time = time.time()
    for round in tqdm(range(num_rounds)):
        # Generate new random seed for each round
        global SEED
        global WORD_LIST
        SEED = random.randint(0, 1000000)
        WORD_LIST = list(get_english_words_set(['web2'], lower=True, alpha =False))

        word_ans, guesses = solve_wordle(text_size)
        print(f"Round {round+1} result: {word_ans}, guesses: {guesses}")
        if word_ans == "NO_SOLUTION_FOUND": 
          not_found += 1
          continue
        total_guesses += guesses
        results.append(guesses)
        
    # Calculate total execution time
    total_time = time.time() - start_time
    
    # Calculate statistics
    num_rounds = num_rounds - not_found
    avg_guesses = total_guesses / num_rounds
    min_guesses = min(results)
    max_guesses = max(results)
    
    print(f"\nPerformance Statistics:")
    print(f"Total rounds: {num_rounds}")
    print(f"Average guesses per game: {avg_guesses:.2f}")
    print(f"Minimum guesses: {min_guesses}")
    print(f"Maximum guesses: {max_guesses}")
    print(f"Total API requests: {total_guesses}")
    print(f"Total execution time: {total_time:.2f} seconds")
    print(f"Average time per game: {(total_time/num_rounds):.2f} seconds")

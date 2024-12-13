import requests
import random
from tqdm import tqdm
from math import log
from english_words import get_english_words_set
import numpy as np
import time 
from itertools import product


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


def solve_wordle(text_size: int) -> str:
  # Reset counter at start of each solve
  global GUESS_COUNT
  GUESS_COUNT = 0
  correct_letter_list = []
  for letter in tqdm(LETTER_FREQUENCY_ORDER):
    if len(correct_letter_list) == text_size:
      break
    guess = letter * text_size
    pattern = try_guess(guess, text_size)

    for i, result in enumerate(pattern):
        if result == CORRECT:
          correct_letter_list.append({i: letter})

  # Sort by index i and build string
  sorted_letters = sorted(correct_letter_list, key=lambda x: list(x.keys())[0])
  result = ''.join(list(d.values())[0] for d in sorted_letters)
  print(result)
  return result, GUESS_COUNT

def is_correct_word(pattern: list) -> bool:
  return set(pattern) == set(["correct"])    


if __name__ == "__main__":
    total_guesses = 0
    num_rounds = 10 # Set number of rounds to test
    text_size = 5     # Set word length
    not_found = 0
    print(f"Testing Wordle solver for {num_rounds} rounds with {text_size}-letter words...")
    
    results = []
    start_time = time.time()
    for round in range(num_rounds):
        # Generate new random seed for each round
        global SEED
        SEED = random.randint(0, 1000000)

        word_ans, guesses = solve_wordle(text_size)
        pattern = try_guess(word_ans, text_size)
        if is_correct_word(pattern):
          print(f"Round {round+1} result: {word_ans}, guesses: {guesses}")
        else:
          print(f"Round {round+1} wrong guess, guesses: {guesses}")
        
        if word_ans == "NO_SOLUTION_FOUND": 
          not_found += 1
          continue
        total_guesses += guesses
        results.append(guesses)

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

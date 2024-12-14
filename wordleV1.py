import requests
import random
from tqdm import tqdm
from math import log
from english_words import get_english_words_set
import time 
from itertools import product
from constants import num_rounds, text_size, seeds


LETTER_FREQUENCY_ORDER = "etaonrishdlfcmugypwbvkjxzq"
CORRECT, PRESENT, ABSENT = "correct", "present", "absent"
GUESS_COUNT = 0

def try_guess(guess: str, text_size: int, seed: int) -> list:
  # Add counter
  global GUESS_COUNT
  GUESS_COUNT += 1
  # get the pattern return from the API
  query = f"https://wordle.votee.dev:8000/random?guess={guess}&seed={seed}&size={text_size}"
  r = requests.get(query)
  result = [check["result"] for check in r.json()]
  return result


def solve_wordle(text_size: int, seed: int) -> tuple[str, int]:
  # Reset counter at start of each solve
  global GUESS_COUNT
  GUESS_COUNT = 0
  correct_letter_list = []
  for letter in tqdm(LETTER_FREQUENCY_ORDER):
    if len(correct_letter_list) == text_size:
      break
    guess = letter * text_size
    pattern = try_guess(guess, text_size, seed)

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
    not_found = 0
    print(f"Testing Wordle solver for {num_rounds} rounds with {text_size}-letter words...")
    
    results = []
    times = []
    current_round = 0
    while current_round < num_rounds:
        # Generate new random seed for each round
        seed = seeds[current_round]
        start_time = time.time()
        word_ans, guesses = solve_wordle(text_size,seed)
        end_time = time.time()

        print(f"Round {current_round} result: {word_ans}, guesses: {guesses}, seed: {seed}")
        total_guesses += guesses
        results.append(guesses)
        times.append(end_time - start_time)
        current_round += 1

    # Calculate total execution time
    total_time = sum(times)
    
    # Calculate statistics
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
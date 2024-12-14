## Versions

### V1 (wordleV1.py)

- Solve with a naive strategy
- Main idea:
  - Try each letter from most frequent to least frequent (e.g., 'e', 't', 'a', etc.)
  - For each letter, create a guess by repeating it (e.g., "eeeee")
  - Track correct letter positions found
  - Stop when all letters are found
  - Build final answer by combining correct letters in order
- Simple but inefficient approach with high guess count
  - In term of guess count, it is the worst strategy
  - Time complexity is `O(26*text_size)`

### V2 (wordleV2.py)

- Solve with information theory strategy
- Main idea:
  - Calculate entropy for each possible guess
  - Choose word with highest entropy as best guess
  - Filter remaining words based on guess pattern
  - Repeat until correct word found
- More efficient approach using information theory
  - Significantly reduces number of guesses needed
  - Time complexity is `O(g*n^2*3^text_size)` where `g` is the number of guesses, `n` is the number of words in the word list, `3^text_size` is the number of possible patterns for a word of length `text_size`

### V3 (wordlev3.py)

- The same as V2 but change the way to calculate entropy for faster entropy calculation
- Time complexity is `O(g*n^2*text_size^2)` where `g` is the number of guesses, `n` is the number of words in the word list, `text_size` is the length of the word

Notice:

- V1 always find the correct word
- V2 and V3 are not 100% accurate because word list is not always contain the word need to be solved

## How to Run

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the solver: `python wordleV1.py` or `python wordleV2.py` or `python wordlev3.py`

By default, the solver will:

- Run 10 rounds
- Use 5-letter words
- Show progress for each round
- Display final statistics including:
  - Average guesses per game
  - Minimum guesses
  - Maximum guesses
  - Total API requests
  - Total execution time
  - Average time per game

## Configuration

You can modify these parameters in `constants.py`:

- `num_rounds`: Number of test rounds (default: 10)
- `text_size`: Word length to solve (default: 5, max: 22)

## Performance

For accuracy, I run 20 rounds for each version with the same seed to make sure the word need to be solved is the same.
| Version | Total Execution Time | Average Time per Game | Average Guesses | Min Guesses | Max Guesses | Total API Requests |
| ------- | -------------------- | --------------------- | --------------- | ----------- | ----------- | ------------------ |
| V1 | 50.44 seconds | 2.52 seconds | 17.50 | 8 | 26 | 350 |
| V2 | 971.86 seconds | 48.59 seconds | 4.90 | 3 | 8 | 98 |
| V3 | 29.41 seconds | 1.47 seconds | 4.65 | 2 | 9 | 93 |

## References

- Strategy based on [3Blue1Brown's Wordle video](https://www.youtube.com/watch?v=v68zYyaEmEA)
- Implementation inspired by [3Blue1Brown's GitHub repository](https://github.com/3b1b/videos/tree/master/_2022/wordle)
- Information Theory explanation: [Computerphile's Video](https://www.youtube.com/watch?v=b6VdGHSV6qg)

## Improvement

- Add Pattern Caching to improve performance
- Optimize Entropy Calculation
- Using Word Frequency Weighting

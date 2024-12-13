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
  - Time complexity is `O(n^2*pattern_count)` where `n` is the number of words in the word list, `pattern_count` is the number of possible patterns for a word of length `text_size` could be `3^text_size`

## How to Run

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the solver: `python wordleV1.py` or `python wordleV2.py`

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

You can modify these parameters in the main section of `wordleV1.py` and `wordleV2.py`:

- `num_rounds`: Number of test rounds (default: 10)
- `text_size`: Word length to solve (default: 5, max: 22)

## Performance

| Version | Total Execution Time | Average Time per Game | Average Guesses | Min Guesses | Max Guesses | Total API Requests |
| ------- | -------------------- | --------------------- | --------------- | ----------- | ----------- | ------------------ |
| V1      | 34.49 seconds        | 3.45 seconds          | 17.00           | 10          | 24          | 170                |
| V2      | 444.53 seconds       | 63.50 seconds         | 4.29            | 3           | 5           | 30                 |

## References

- Strategy based on [3Blue1Brown's Wordle video](https://www.youtube.com/watch?v=v68zYyaEmEA)
- Implementation inspired by [3Blue1Brown's GitHub repository](https://github.com/3b1b/videos/tree/master/_2022/wordle)
- Information Theory explanation: [Computerphile's Video](https://www.youtube.com/watch?v=b6VdGHSV6qg)

## Improvement

- Add Pattern Caching to improve performance
- Optimize Entropy Calculation using numpy
- Using Word Frequency Weighting

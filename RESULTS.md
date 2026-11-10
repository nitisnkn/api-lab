# API lab results
## Part 0
Step 0.1, the number of pizza names: 18
Step 0.3, status code of the request without a token: 404
Step 0.4, the name of your pizza: Margherita
Step 0.12, results of the three runs without a session (optional): The Red Napoletana, A Bright Siciliana, The Scary Fungi e Olive
Step 0.16, blocks of "how many of the three tools are excluded": 0, 1, 2, 3

## Defect report
Title: Excluding all tools returns 500 instead of 400
Request: POST /api/pizza with body {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
Expected result: Status 400 and a JSON error message explaining no pizza can be made
Actual result: Status 500 Internal Server Error with an empty body
Severity: High

## Part A: Input space partitioning for ratings

| Characteristic | Blocks | Values in the tests |
| --- | --- | --- |
| C1 Value of stars | below 1, 1 to 5 (base), above 5 | 0, 3, 6 |
| C2 Type of stars | whole number (base), decimal, text, missing | 3, 3.5, "3", no field |
| C3 Pizza | exists (base), does not exist | a new pizza, 999999999 |
| C4 Token | the user's own (base), none, wrong length | from auth, no header, token short |

## Part B
1.
2.
3.
4.
5.
6.
7.
8.
```[cite: 16]
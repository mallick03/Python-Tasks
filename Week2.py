# ==========================================
# Task 1. Write a Python program to get a list, sorted in increasing order by the last element in each tuple from a given list of non-empty tuples.
# ==========================================
sample_tuples = [(2, 5), (1, 2), (4, 4), (2, 3), (2, 1)]
sorted_tuples = sorted(sample_tuples, key=lambda x: x[-1])
print("Task 1:", sorted_tuples)

# ==========================================
# Task 2: Given a string s1, write a program to return the sum and average of the digits that appear in the string, ignoring all other characters.
# ==========================================
s1 = "Python Task 2 Winter Semester 2026"
digits = [int(c) for c in s1 if c.isdigit()]
digit_sum = sum(digits)
digit_avg = digit_sum / len(digits) if digits else 0
print(f"Task 2: Sum = {digit_sum}, Average = {digit_avg}")

# ==========================================
# Task 3: Write a Python program to sort a list of dictionaries using Lambda.
# ==========================================
dict_list = [
    {'make': ' Google ', 'model': 216, 'color': 'Black'},
    {'make': 'Mi Max', 'model': '2', 'color': 'Gold'},
    {'make': 'Samsung', 'model': 7, 'color': 'Blue'}
]
sorted_dicts = sorted(dict_list, key=lambda d: d['color'])
print("Task 3:", sorted_dicts)


# ==========================================
# Task 4: Write a Python program to convert a given list of strings into list of lists using map function.
# ==========================================
words = ["Sky", "Blue", "Ice"]
nested_lists = list(map(list, words))
print("Task 4:", nested_lists)


# ==========================================
# Task 5: Create a dictionary with the events in Dortmund and the date of the event. List all events that were running during the Night of Museums in Dortmund on 19th September 2026. 
# ==========================================
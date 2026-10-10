import numpy as np

# ==========================================
# Task 1. Create a vector with values ranging from 10 to 49. Reverse a vector (first element becomes last)
# ==========================================
v = np.arange(10, 50)
v_reversed = v[::-1]
print("1. Original vector (10 to 49):\n", v)
print("   Reversed vector:\n", v_reversed)

# ==========================================
# Task 2. Create a 5x5 array with random values and find the minimum and maximum values
# ==========================================
arr_5x5 = np.random.random((5, 5))
print("\n2. 5x5 random array:\n", arr_5x5)
print("   Min value:", arr_5x5.min())
print("   Max value:", arr_5x5.max())

# ==========================================
# Task 3. Normalize a 5x5 random matrix
# ==========================================
norm_arr = (arr_5x5 - arr_5x5.min()) / (arr_5x5.max() - arr_5x5.min())
print("\n3. Normalized 5x5 matrix:\n", norm_arr)

# ==========================================
# Task 4. Multiply a 5x3 matrix by a 3x2 matrix (real matrix product)
# ==========================================
m1 = np.random.random((5, 3))
m2 = np.random.random((3, 2))
prod = m1 @ m2  # Or np.dot(m1, m2)
print("\n4. Matrix multiplication (5x3 @ 3x2) result shape:", prod.shape)
print(prod)

# ==========================================
# Task 5. How to get the dates of yesterday, today and tomorrow?
# ==========================================
today = np.datetime64("today", "D")
yesterday = today - np.timedelta64(1, "D")
tomorrow = today + np.timedelta64(1, "D")
print("\n5. Dates:")
print("   Yesterday:", yesterday)
print("   Today:    ", today)
print("   Tomorrow: ", tomorrow)

# ==========================================
# Task 6. Extract the integer part of a random array using 5 different methods
# ==========================================
z = np.random.uniform(1.0, 10.0, 5)
print("\n6. Original float array:", z)
print("   Method 1 (z - z % 1):", z - z % 1)
print("   Method 2 (np.floor): ", np.floor(z))
print("   Method 3 (np.trunc): ", np.trunc(z))
print("   Method 4 (astype):   ", z.astype(int))
print("   Method 5 (np.ceil-1):", np.ceil(z) - 1)

# ==========================================
# Task 7. Create a structured array representing a position ( x,y ) and a color (r,g,b)
# ==========================================
dtype_spec = [
    ("position", [("x", float), ("y", float)]),
    ("color", [("r", int), ("g", int), ("b", int)]),
]
structured_arr = np.zeros(2, dtype=dtype_spec)
structured_arr[0] = ((10.5, 20.2), (255, 0, 0))
structured_arr[1] = ((5.0, 12.8), (0, 128, 255))
print("\n7. Structured array:\n", structured_arr)


# ==========================================
# Task 1. Consider a generator function that generates 10 integers and use it to build an array
# ==========================================
def generate_integers():
    for i in range(10):
        yield i

gen_arr = np.fromiter(generate_integers(), dtype=int)
print("1. Array from generator:", gen_arr)

# ==========================================
# Task 2. Consider two random array A and B, check if they are equal
# ==========================================
A = np.random.randint(0, 2, 5)
B = np.random.randint(0, 2, 5)
print("\n2. Array A:", A)
print("   Array B:", B)
print("   Are A and B equal?:", np.array_equal(A, B))

# ==========================================
# Task 3. Consider a random vector with shape (100,2) representing coordinates, find point by point distances
# ==========================================
coords = np.random.random((100, 2))
distances = np.sqrt(np.sum((coords[:, np.newaxis, :] - coords[np.newaxis, :, :]) ** 2, axis=-1))
print("\n3. Pairwise distance matrix shape (100 coordinates):", distances.shape)


# ==========================================
# Task 4. Subtract the mean of each row of a matrix
# ==========================================
mat = np.random.random((4, 4))
mat_demeaned = mat - mat.mean(axis=1, keepdims=True)
print("\n4. Row-demeaned matrix (row means should now be ~0):\n", mat_demeaned)
print("   Check row means:", mat_demeaned.mean(axis=1))

# ==========================================
# Task 5. How to I sort an array by the nth column?
# ==========================================
sample_mat = np.random.randint(10, 99, (5, 4))
n = 1  
sorted_mat = sample_mat[sample_mat[:, n].argsort()]
print("\n5. Original matrix:\n", sample_mat)
print(f"   Sorted by column {n}:\n", sorted_mat)

# ==========================================
# Task 6. Compute a matrix rank
# ==========================================
square_mat = np.random.random((4, 4))
rank = np.linalg.matrix_rank(square_mat)
print("\n6. Matrix rank:", rank)

# ==========================================
# Task 7. Consider a 16x16 array, how to get the block sum (block size is 4x4)
# ==========================================
arr_16 = np.ones((16, 16))
block_sum = arr_16.reshape(4, 4, 4, 4).sum(axis=(1, 3))
print("\n7. 16x16 ones array block-sum (each 4x4 block sum should be 16):\n", block_sum)

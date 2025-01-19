from topsis_parth_102216063.topsis import Topsis

matrix = [[7, 9, 8], [8, 6, 7], [6, 8, 9]]
weights = [0.5, 0.3, 0.2]
impacts = ['+', '-', '+']

# Call the static method directly without instantiating the class
result = Topsis.topsis(matrix, weights, impacts)

print(result)

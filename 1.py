# ИЗМЕНЕНО


# Пример прямоугольной матрицы (можно изменить на свою)
matrix = [
    [1, 7, 2],
    [14, 5, 21],
    [3, 28, 9],
    [4, 6, 35]
]

rows = len(matrix)
cols = len(matrix[0]) if rows > 0 else 0

# Список для хранения элементов, кратных семи
result = []

# Проходим по элементам, расположенным на соседних диагоналях
for i in range(rows):
    for j in range(cols):
        # Проверяем главную диагональ (i == j)
        if i == j and matrix[i][j] % 7 == 0:
            result.append(matrix[i][j])
        # Проверяем диагональ выше главной (i == j - 1)
        if i == j - 1 and j > 0 and matrix[i][j] % 7 == 0:
            result.append(matrix[i][j])
        # Проверяем диагональ ниже главной (i == j + 1)
        if i == j + 1 and matrix[i][j] % 7 == 0:
            result.append(matrix[i][j])

# Проверяем, есть ли элементы в результате
if result:
    print("Элементы, кратные семи:", result)
else:
    print("Элементы, кратные семи на соседних диагоналях отсутствуют.")


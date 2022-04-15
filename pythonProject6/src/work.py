import csv
import math


def condition(x, y, i):
    return x <= i <= y


data_csv = []
with open("data.csv", encoding='utf-8') as r_file:
    file_reader = csv.reader(r_file, delimiter=" ")
    for row in file_reader:
        data_csv.append(float(row[0]))

n = len(data_csv)
print(f'n = {n}\n')
min_x = min(data_csv)
max_x = max(data_csv)
print(f'Xmin = {min_x}, Xmax = {max_x}\n')

k = 1 + 3.322 * math.log(n)
l = (max_x - min_x) / k
range_data = min_x

matrix = []
sum_for_x_avg = 0
while range_data <= max_x:
    first_column = [range_data, range_data + l]
    second_column = sum(condition(first_column[0], first_column[1], i) for i in data_csv)
    third_column = f'{second_column}/{n}'
    fourth_column = (first_column[0] + first_column[1]) / 2
    matrix.append([first_column, second_column, third_column, fourth_column])
    sum_for_x_avg += fourth_column * second_column
    range_data += l

x_avg = sum_for_x_avg / n
sums = 0
for i in matrix:
    sums += i[1]
    fourth_column = i[3]
    i.append(fourth_column - x_avg)
    i.append((fourth_column - x_avg) * (fourth_column - x_avg))
    i.append(sums)

print('Матрица')
for i in matrix:
    print(i)
sigma = math.sqrt(sum((i[6] * i[6] * i[1]) for i in matrix) / 30)
max_len = 0
for i in range(len(matrix)):
    if matrix[max_len][1] < matrix[i][1]:
        max_len = i

mo = matrix[max_len][0][0] - (matrix[max_len][1] - matrix[max_len - 1][1]) / (
        (matrix[max_len][1] - matrix[max_len - 1][1]) + ((matrix[max_len][1] - matrix[max_len + 1][1])))

print(f'\nM0 = {mo}\n')
m_e = matrix[max_len][0][0] + 0.5 * n
print(f"me = {m_e}\n")
a_three = (sum((i[4] ** 3) * i[1] for i in matrix) / 30) / (sigma ** 3)
print(f"A3 = {a_three}")
if a_three < 0.25:
    print('Незначительное\n')
elif 0.25 <= a_three <= 0.5:
    print('Умеренное\n')
else:
    print("Существенное\n")

e_k = (sum((i[4] ** 4) * i[1] for i in matrix) / sigma ** 4) - 3
print(f'Ek = {e_k}\n')
v = (sigma / x_avg) * 100
print(f'v = {v}')

if v < 30:
    print('Выборка однородна\n')
else:
    print('Выборка неоднородна\n')

t = 2.045

x_minus = x_avg - ((t * sigma) / math.sqrt(n))
x_plus = x_avg + ((t * sigma) / math.sqrt(n))
print(f'{x_minus} < x < {x_plus}\nС вероятостью 95 % наша генеральная средняя попадает в этот интервал')

k = n - 1
lambda_one = (1 - 0.95) / 2
lambda_two = (1 + 0.95) / 2
x_2_lambda_1 = 49.7
x_2_lambda_2 = 16

sigma_left = (k * (sigma ** 2)) / x_2_lambda_1
sigma_right = (k * (sigma ** 2)) / x_2_lambda_2

print(f"{sigma_left} < sigma^2 < {sigma_right}")
print(f"{math.sqrt(sigma_left)} < sigma < {math.sqrt(sigma_right)}")
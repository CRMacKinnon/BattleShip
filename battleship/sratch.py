numbers = list(range(10))

print(numbers)
while str(numbers[0]) != '8':
    numbers.append(numbers.pop(0))

print(numbers)
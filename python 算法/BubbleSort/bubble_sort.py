def bubble_sort(list):
    n = len(list)
    for i in range(n):
        for j in range(0, n - 1 - i):
            if list[j] > list[j + 1]:
                list[j], list[j + 1] = list[j + 1], list[j]
            else:
                break

if __name__ == '__main__':
    list = [50, 24, 12, 5]
    bubble_sort(list)
    print(list)
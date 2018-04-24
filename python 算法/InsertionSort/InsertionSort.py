# def insertion_sort(list):
#     n = len(list)
#     for i in range(1, n):
#         for j in range(i, 0, -1) :
#             if list[j] < list[j - 1]:
#                 list[j], list[j - 1] = list[j - 1], list[j]
#             else:
#                 break

def insert_sort(list):
    n = len(list)
    for i in range(1, n):
        key = list[i]
        j = i - 1
        while j >= 0 and list[j] > key:
            list[j + 1] = list[j]
            j -= 1
        list[j + 1] = key

if __name__ == '__main__':
    list = [52, 34, 75]
    print('原队列：%s' % list)
    insert_sort(list)
    print('排序后队列：%s' % list)


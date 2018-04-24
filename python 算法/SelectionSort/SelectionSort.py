def selection_sotr(list):
    n = len(list)
    for i in range(0, n):
        min_index = i
        for j in range(i + 1, n):
            if list[min_index] > list[j]:
                min_index = j
        
        if i != min_index:
            list[min_index], list[i] = list[i], list[min_index]

if __name__ == '__main__':
    list = [50, 26, 15, 30, 5]
    print('原队列：%s' % list)
    selection_sotr(list)
    print('排序后的队列：%s' % list)

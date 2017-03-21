#pure python
def generateRandomList(a, b):
    random.seed()
    rand_list = [random.randint(1, b) for k in range(b)]
    return rand_list


def analysis(n):
    list_v = generateRandomList(1, n)
    elapsed_time = 0.0
    start = time.process_time()
    list_v.sort()
    random.seed()
    while len(list_v) != 0:
        rand_idx = random.randint(0, len(list_v) - 1)
        list_v.pop(rand_idx)
    elapsed_time = time.process_time() - start
    print("Execution time was {:.6f} s".format(elapsed_time))


def is_within_limit(a: int, b: int) -> bool:
    return 1 <= abs(a - b) <= 3

def is_increasing(lst: list[int], tol: int = 0) -> bool:
    flag: bool = True
    
    for i in range(len(lst) - 1):
        if lst[i] < lst[i + 1] and is_within_limit(lst[i], lst[i + 1]):
            continue

        if tol > 0:
            trial_lst_A: list[int] = lst[:]
            del trial_lst_A[i]

            trial_lst_B: list[int] = lst[:]
            del trial_lst_B[i + 1]

            if is_increasing(trial_lst_A, tol - 1) or is_increasing(trial_lst_B, tol - 1):
                break

        flag = False
        break

    return flag

def is_decreasing(lst: list[int], tol: int = 0) -> bool:
    flag: bool = True
    
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1] and is_within_limit(lst[i], lst[i + 1]):
            continue

        if tol > 0:
            trial_lst_A: list[int] = lst[:]
            del trial_lst_A[i]

            trial_lst_B: list[int] = lst[:]
            del trial_lst_B[i + 1]
            
            if is_decreasing(trial_lst_A, tol - 1) or is_decreasing(trial_lst_B, tol - 1):
                break

        flag = False
        break

    return flag

if __name__ == "__main__":
    TOLERANCE_LEVEL: int = 1
    num_of_safe_reports: int = 0

    while True:
        report: list[int] = list(map(int, input().split()))

        if report == []:
            break

        if is_increasing(report, TOLERANCE_LEVEL):
            num_of_safe_reports += 1
        elif is_decreasing(report, TOLERANCE_LEVEL):
            num_of_safe_reports += 1

    print(num_of_safe_reports)
    
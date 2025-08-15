def is_desired_result(expected_res: int, operands: list[int], ops: list[str], idx: int = 0, 
                      res: int | None = None) -> bool:
    def concatenate(a: int, b: int) -> int:
        return int(str(a) + str(b))

    if idx == len(operands):
        return expected_res == res

    if res is None:
        return is_desired_result(expected_res, operands, ops, idx + 1, res=operands[idx])
 
    for op in ops:
        match op:
            case '+':
                if is_desired_result(expected_res, operands, ops, idx + 1, res + operands[idx]):
                    return True
            case '*':
                if is_desired_result(expected_res, operands, ops, idx + 1, res * operands[idx]):
                    return True
            case '||':
                if is_desired_result(expected_res, operands, ops, idx + 1, concatenate(res, operands[idx])):
                    return True
            case _:
                Exception("Unsupported operation.")

    return False

if __name__ == "__main__":  
    OPERATIONS_SET_A: list[str] = ['+', '*']
    OPERATIONS_SET_B: list[str] = ['+', '*', '||']
    total_calibration_set_A: int = 0
    total_calibration_set_B: int = 0

    while True:
        equations: list[str]= input().split(":")

        if equations == ['']:
            break

        expected_result: int = int(equations[0])
        operands: list[int] = list(map(int, equations[1].split()))

        if is_desired_result(expected_result, operands, OPERATIONS_SET_A, idx=0):
            total_calibration_set_A += expected_result
        
        if is_desired_result(expected_result, operands, OPERATIONS_SET_B, idx=0):
            total_calibration_set_B += expected_result
        
    print(total_calibration_set_A)
    print(total_calibration_set_B)

    
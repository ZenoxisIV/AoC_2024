import re

class RegExMul:
    def __init__(self) -> None:
        self.sum_of_mul_ops: int = 0
        self.restricted_sum_of_mul_ops: int = 0

    def extract_product(self, puzzle: str) -> int:
        total: int = 0
        mul_ops: list[str] = re.findall(r'mul\(\d+,\d+\)', puzzle)

        for mul_op in mul_ops:
            factors: list[str] = re.findall(r'\d+', mul_op)
            total += int(factors[0]) * int(factors[1])
        
        return total
    
    def free_mul(self, puzzle: str) -> int:
        self.sum_of_mul_ops += self.extract_product(puzzle)
        return self.sum_of_mul_ops

    def restricted_mul(self, puzzle: str) -> int:
        do_ops: list[str] = puzzle.split("do()")
        for do_op in do_ops:
            cleaned_do_op = re.search(r".*?don't\(\)", do_op) # Remove disabled mul()
            if cleaned_do_op:
                self.restricted_sum_of_mul_ops += self.extract_product(cleaned_do_op.group(0))
                continue
            self.restricted_sum_of_mul_ops += self.extract_product(do_op)
        return self.restricted_sum_of_mul_ops

puzzle = ""
while True:
    piece = input()

    if piece == "":
        break

    puzzle += piece

solver = RegExMul()
print(solver.free_mul(puzzle))
print(solver.restricted_mul(puzzle))
from copy import deepcopy

def calculate_order_sum(page_numbers: list[int], rules_book: list[tuple[list[int], list[list[int]]]], with_error_correction: bool = False) -> int:
    def reorder_pages() -> list[int]:
        temp_page_order: list[int] = []
        for page_number in page_numbers:
            for set_of_rules in rules_book:
                left_rule: list[int] = set_of_rules[0]
                if page_number == left_rule[0]:
                    if page_number in temp_page_order:
                        temp_page_order.remove(page_number)
                    temp_page_order.append(page_number)
                    for right_rules in set_of_rules[1]:
                        if right_rules[0] in temp_page_order:
                            temp_page_order.remove(right_rules[0])
                            temp_page_order.append(right_rules[0])
                        elif right_rules[0] in page_numbers:
                            temp_page_order.append(right_rules[0])
        return temp_page_order

    copy_of_rules_book: list[tuple[list[int], list[list[int]]]] = deepcopy(rules_book)
    for page_number in page_numbers:
        for set_of_rules in copy_of_rules_book:
            is_right_rule_evoked: bool = False
            for right_rules in set_of_rules[1]:
                if not is_right_rule_evoked and right_rules[1]:
                    is_right_rule_evoked = True
                    
                if page_number == right_rules[0]:
                    right_rules[1] = 1
                    break

            left_rule: list[int] = set_of_rules[0]
            if page_number == left_rule[0]:
                if with_error_correction and is_right_rule_evoked:
                    page_numbers = reorder_pages()
                    return calculate_order_sum(page_numbers, rules_book, with_error_correction=True)
                if is_right_rule_evoked:
                    return 0
                left_rule[1] = 1
    
    return page_numbers[len(page_numbers) // 2]

if __name__ == "__main__":
    rules_book: list[tuple[list[int], list[list[int]]]] = []
    middle_sum: int = 0
    middle_no_reorder_sum: int = 0

    while True:
        new_rule: list[str] | list[int] = input().split("|")

        if new_rule == ['']:
            break
        
        new_rule = list(map(int, new_rule))
        is_existing: bool = False
        for set_of_rules in rules_book:
            if [new_rule[0], 0] == set_of_rules[0]:
                is_existing = True
                set_of_rules[1].append([new_rule[1], 0])
                break
        if not is_existing:
            rules_book.append(([new_rule[0], 0], [[new_rule[1], 0]]))

    while True:
        page_numbers: list[str] | list[int] = input().split(",")
        
        if page_numbers == ['']:
            break

        page_numbers = list(map(int, page_numbers))
        middle_no_reorder_sum += calculate_order_sum(page_numbers, rules_book, with_error_correction=False)
        middle_sum += calculate_order_sum(page_numbers, rules_book, with_error_correction=True)

    middle_with_reorder_sum: int = middle_sum - middle_no_reorder_sum

    print(middle_no_reorder_sum)
    print(middle_with_reorder_sum)
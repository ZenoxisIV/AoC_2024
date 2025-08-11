class CeresWordSearch:
    def __init__(self, grid: list[list[str]]) -> None:
        self.grid: list[list[str]] = grid

    def count_words_found(self, word: str, x_pos: int, y_pos: int) -> int:
        DIRECTIONS: list[tuple[int, int]] = [(0,-1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]
        word_count: int = 0

        for direction in DIRECTIONS:
            dy, dx = direction
            is_found: bool = True
            for letter in word[1:]:
                if self.grid[y_pos + dy][x_pos + dx] == letter:
                    dy, dx = tuple(map(sum, zip((dy, dx), direction)))
                else:
                    is_found = False
                    break
            if is_found:
                word_count += 1

        return word_count

    def is_x_word_found(self, word: str, x_pos: int, y_pos: int) -> bool:
        DIRECTIONS: list[tuple[int, int]] = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        x_word: list[str] = [word[-3], word[-1]]

        for i in range(len(DIRECTIONS)):
            dy_i, dx_i = DIRECTIONS[i]

            if self.grid[y_pos + dy_i][x_pos + dx_i] not in x_word:
                return False
            
            adjacency_count: int = 0
            letter: str = self.grid[y_pos + dy_i][x_pos + dx_i]

            if letter in x_word:
                if letter == self.grid[y_pos - dy_i][x_pos - dx_i]:
                    return False

                for j in range(len(DIRECTIONS)):
                    if i == j:
                        continue

                    dy_j, dx_j = DIRECTIONS[j]
                    if letter == self.grid[y_pos + dy_j][x_pos + dx_j]:
                        adjacency_count += 1

                if adjacency_count != 1:
                    return False

        return True

if __name__ == "__main__":
    WORD: str = "XMAS"
    assert len(WORD) >= 3

    word_search_grid: list[list[str]] = []
    total: int = 0
    x_total: int = 0
    do_add_pad: bool = True

    while True:
        line: list[str] = list(input())

        if do_add_pad:
            word_search_grid.append(list("*" * (len(line) + 2)))
            do_add_pad = False

        if line == []:
            word_search_grid.append(list("*" * len(word_search_grid[0])))
            break

        word_search_grid.append(['*'] + line + ['*'])

    solver = CeresWordSearch(word_search_grid)

    for y in range(1, len(word_search_grid) - 1):
        for x in range(1, len(word_search_grid[y]) - 1):
            if word_search_grid[y][x] == WORD[0]:
                total += solver.count_words_found(WORD, x, y)

            if word_search_grid[y][x] == WORD[-2]:
                x_total += solver.is_x_word_found(WORD, x, y)

    print(total)
    print(x_total)
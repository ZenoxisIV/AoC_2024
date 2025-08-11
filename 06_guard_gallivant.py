from copy import deepcopy

class GuardGallivant:
    def __init__(self, grid: list[list[str]]) -> None:
        self.grid: list[list[str]] = grid
        self.directions: dict[str, tuple[int, int]] = {
            "UP": (-1, 0), 
            "RIGHT": (0, 1), 
            "DOWN": (1, 0), 
            "LEFT": (0, -1)
        }
        self.obstruction_states: list[str] = ['U', 'R', 'D', 'L']
        self.distinct_positions_total: int = 0
        self.is_valid_obstruction: bool = False

    def search_index(self, to_search: str) -> tuple[int | None, int | None]:
        for i, row in enumerate(self.grid):
            for j, symbol in enumerate(row):
                if symbol == to_search:
                    return i, j
        
        return None, None

    def can_traverse_map(self, init_pos: tuple[int | None, int | None], curr_state: str) -> bool:
        guard_y_pos, guard_x_pos = init_pos

        assert guard_y_pos != None
        assert guard_x_pos != None

        next_y_pos: int = guard_y_pos + self.directions[curr_state][0]
        next_x_pos: int = guard_x_pos + self.directions[curr_state][1]
        
        match curr_state:
            case "UP":
                if self.grid[next_y_pos][next_x_pos] == 'U':
                    self.is_valid_obstruction = True
                    return False
            case "RIGHT":
                if self.grid[next_y_pos][next_x_pos] == 'R':
                    self.is_valid_obstruction = True
                    return False
            case "DOWN":
                if self.grid[next_y_pos][next_x_pos] == 'D':
                    self.is_valid_obstruction = True
                    return False
            case "LEFT":
                if self.grid[next_y_pos][next_x_pos] == 'L':
                    self.is_valid_obstruction = True
                    return False
            case _:
                Exception("Unknown direction.")
                
        return self.grid[next_y_pos][next_x_pos] != "*"

    def predict_guard_path(self) -> list[list[str]]:
        predicted_map: list[list[str]] = deepcopy(self.grid)
        
        guard_symbol: str = "^"
        curr_state: str = "UP"
        guard_y_pos, guard_x_pos = self.search_index(guard_symbol)

        assert guard_y_pos != None
        assert guard_x_pos != None

        while self.can_traverse_map((guard_y_pos, guard_x_pos), curr_state):
            self.grid[guard_y_pos][guard_x_pos] = '.'

            if predicted_map[guard_y_pos][guard_x_pos] != 'X':
                predicted_map[guard_y_pos][guard_x_pos] = 'X'
                self.distinct_positions_total += 1

            next_y_pos: int = guard_y_pos + self.directions[curr_state][0]
            next_x_pos: int = guard_x_pos + self.directions[curr_state][1]

            match curr_state:
                case "UP":
                    if self.grid[next_y_pos][next_x_pos] == '#' or self.grid[next_y_pos][next_x_pos] in self.obstruction_states:
                        self.grid[next_y_pos][next_x_pos] = "U"
                        guard_symbol = '>'
                        curr_state = "RIGHT"
                    else:
                        guard_y_pos += self.directions[curr_state][0]
                        guard_x_pos += self.directions[curr_state][1]
                        self.grid[guard_y_pos][guard_x_pos] = guard_symbol
                case "RIGHT":
                    if self.grid[next_y_pos][next_x_pos] == '#' or self.grid[next_y_pos][next_x_pos] in self.obstruction_states:
                        self.grid[next_y_pos][next_x_pos] = "R"
                        guard_symbol = 'v'
                        curr_state = "DOWN"
                    else:
                        guard_y_pos += self.directions[curr_state][0]
                        guard_x_pos += self.directions[curr_state][1]
                case "DOWN":
                    if self.grid[next_y_pos][next_x_pos] == '#' or self.grid[next_y_pos][next_x_pos] in self.obstruction_states:
                        self.grid[next_y_pos][next_x_pos] = "D"
                        guard_symbol = '<'
                        curr_state = "LEFT"
                    else:
                        guard_y_pos += self.directions[curr_state][0]
                        guard_x_pos += self.directions[curr_state][1]
                case "LEFT":
                    if self.grid[next_y_pos][next_x_pos] == '#' or self.grid[next_y_pos][next_x_pos] in self.obstruction_states:
                        self.grid[next_y_pos][next_x_pos] = "L"
                        guard_symbol = '^'
                        curr_state = "UP"
                    else:
                        guard_y_pos += self.directions[curr_state][0]
                        guard_x_pos += self.directions[curr_state][1]
                case _:
                    Exception("Unknown direction.")

        predicted_map[guard_y_pos][guard_x_pos] = 'X'
        self.distinct_positions_total += 1         

        return predicted_map
    
    def get_distinct_positions_count(self) -> int:
        return self.distinct_positions_total
    
    def get_is_valid_obstruction(self) -> bool:
        return self.is_valid_obstruction

if __name__ == "__main__":
    map_grid: list[list[str]] = []
    distinct_pos_count: int = 0
    valid_obs_count: int = 0
    do_add_pad: bool = True

    while True:
        line: list[str] = list(input())

        if do_add_pad:
            map_grid.append(list("*" * (len(line) + 2)))
            do_add_pad = False

        if line == []:
            map_grid.append(list("*" * len(map_grid[0])))
            break

        map_grid.append(['*'] + line + ['*'])

    copy_of_map_grid: list[list[str]] = deepcopy(map_grid)
    solver = GuardGallivant(copy_of_map_grid)
    init_guard_y_pos, init_guard_x_pos = solver.search_index('^')
    plotted_map: list[list[str]] = solver.predict_guard_path()

    print(solver.get_distinct_positions_count())

    assert init_guard_y_pos != None
    assert init_guard_x_pos != None

    for i, row in enumerate(plotted_map):
        for j, symbol in enumerate(row):
            if symbol == 'X' and (i, j) != (init_guard_y_pos, init_guard_x_pos):
                copy_of_map_grid: list[list[str]] = deepcopy(map_grid)
                copy_of_map_grid[i][j] = '#'
                solver = GuardGallivant(copy_of_map_grid)
                _ = solver.predict_guard_path()
                valid_obs_count += solver.get_is_valid_obstruction()

    print(valid_obs_count)
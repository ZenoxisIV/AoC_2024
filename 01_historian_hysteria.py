loc_id_set_A: list[int] = []
loc_id_set_B: list[int] = []

while True:
    pair_loc_id: list[str] = input().split()

    if pair_loc_id == []:
        break

    loc_id_set_A.append(int(pair_loc_id[0]))
    loc_id_set_B.append(int(pair_loc_id[1]))

loc_id_set_A.sort()
loc_id_set_B.sort()

sum_of_dists: int = sum(list(map(lambda a, b: abs(a - b), loc_id_set_A, loc_id_set_B)))
sum_of_similarity_scores: int = sum(list(map(lambda a: a * len(list(filter(lambda b: a == b, loc_id_set_B))), loc_id_set_A)))

print(sum_of_dists)
print(sum_of_similarity_scores)
def get_partition_name(lower_bound: float, longitude: bool) -> str:
    if longitude:
        if lower_bound.is_integer():
            partition_name = f"{abs(int(lower_bound)):02d}_"
        else:
            partition_name = f"{abs(int(lower_bound)):02d}{str(lower_bound-int(lower_bound))[1:]}"
    else:
        if lower_bound < 0:
            hemisphere = "S"
        else:
            hemisphere = "N"
        partition_name = f"{abs(int(lower_bound))}{hemisphere}"
    return partition_name

def generate_partitions(start:float, end:float, step:float, longitude:bool) -> dict[str, tuple]:
    partitions = {}
    lower_bound = start
    upper_bound = start + step
    while upper_bound < end:
        partition_name = get_partition_name(lower_bound=lower_bound, longitude=longitude)
        partitions[partition_name] = (lower_bound, upper_bound)
        lower_bound = upper_bound
        upper_bound += step
    return partitions

def find_partition(number: float, partitions: dict[str, tuple]) -> str:
    for partition, interval in partitions.items():
        if interval[0] <= number < interval[1]:
            return partition
    return None

# Defina o intervalo
start:float = -63.0
end:float = -39.0
step:float = 1.5

# Gere as partições
partitions_long = generate_partitions(start, end, step, True)
part = find_partition(-57, partitions=partitions_long)

partitions_lat = generate_partitions(start = -33.0, end= 2.0, step = 1, longitude=False)
part_lat = find_partition(-20, partitions=partitions_lat)

print(part, part_lat)
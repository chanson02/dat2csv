import os, csv

# file_name = "test.dat2"
# path = (
#     f"/home/cooperhanson/Documents/Projects/cardiac_markers/data/singapore/{file_name}"
# )


def read_bytes(path):
    bytes = []
    with open(path, "rb") as f:
        byte = f.read(1)
        while byte != b"":
            bytes.append(byte)
            byte = f.read(1)
    return bytes


def decode_bytes(bytes):
    # Start/Stop of each data piece
    starts = []
    ends = []
    for i in range(0, len(bytes), 2):
        starts.append(bytes[i + 1])
        ends.append(bytes[i])

    # Encoded keys
    encoded = []
    for i in range(len(starts)):
        bit = starts[i] + ends[i]
        encoded.append(int.from_bytes(bit, "big"))

    # Decode keys
    mvs = []  # milivolt
    for e in encoded:
        mvs.append([round(0.01 * e - 5, 4)])

    return mvs


def write(data, path):
    writer = csv.writer(open(path, "w"))
    writer.writerows(data)


# bytes = read_bytes(path)
# data = decode_bytes(bytes)
# write(
#     data,
#     "/home/cooperhanson/Documents/Projects/cardiac_markers/data/singapore/test.csv",
# )
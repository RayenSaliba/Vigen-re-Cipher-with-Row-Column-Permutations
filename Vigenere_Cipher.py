ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def clean(text):
    """Keep only letters and make them uppercase."""
    return "".join(ch for ch in text.upper() if ch in ALPHABET)


# ---------- Round 1: Vigenere substitution ----------
def vigenere(text, key, decrypt=False):
    result = ""
    for i, ch in enumerate(text):
        shift = ALPHABET.index(key[i % len(key)])
        if decrypt:
            shift = -shift
        result += ALPHABET[(ALPHABET.index(ch) + shift) % 26]
    return result


# ---------- Permutation helpers ----------
def permute(items, order):
    """Put items in the order given (order is 1-based, e.g. [3, 1, 2])."""
    return [items[i - 1] for i in order]


def unpermute(items, order):
    """Exact reverse of permute()."""
    result = [None] * len(items)
    for position, i in enumerate(order):
        result[i - 1] = items[position]
    return result


# ---------- Round 2: column permutation ----------
def split_rows(text, width):
    return [list(text[i:i + width]) for i in range(0, len(text), width)]


def column_permutation(text, order, decrypt=False):
    func = unpermute if decrypt else permute
    rows = split_rows(text, len(order))
    return "".join("".join(func(row, order)) for row in rows)


# ---------- Round 3: row permutation ----------
def row_permutation(text, col_count, order, decrypt=False):
    func = unpermute if decrypt else permute
    rows = split_rows(text, col_count)
    result = ""
    # rows are shuffled in groups of len(order) rows
    for i in range(0, len(rows), len(order)):
        group = rows[i:i + len(order)]
        result += "".join("".join(row) for row in func(group, order))
    return result


# ---------- Full pipelines ----------
def encrypt(plaintext, key, col_order, row_order):
    text = clean(plaintext)

    # pad with X so the text fills complete rows AND complete row groups
    block = len(col_order) * len(row_order)
    while len(text) % block != 0:
        text += "X"

    text = vigenere(text, key)
    print("After Vigenere        :", text)

    text = column_permutation(text, col_order)
    print("After column permute  :", text)

    text = row_permutation(text, len(col_order), row_order)
    print("After row permute     :", text)
    return text


def decrypt(ciphertext, key, col_order, row_order):
    text = clean(ciphertext)

    text = row_permutation(text, len(col_order), row_order, decrypt=True)
    print("After row undo        :", text)

    text = column_permutation(text, col_order, decrypt=True)
    print("After column undo     :", text)

    text = vigenere(text, key, decrypt=True)
    return text


def read_order(prompt):
    """Read e.g. '3 1 4 2' and check it is a valid permutation."""
    while True:
        try:
            order = [int(n) for n in input(prompt).split()]
            if sorted(order) == list(range(1, len(order) + 1)):
                return order
        except ValueError:
            pass
        print("Invalid. Use each number from 1 to N exactly once, e.g. 3 1 4 2")


def main():
    mode = ""
    while mode not in ("E", "D"):
        mode = input("Mode - Encrypt (E) or Decrypt (D): ").strip().upper()[:1]

    text = input("Enter plaintext: " if mode == "E" else "Enter ciphertext: ")
    key = clean(input("Enter Vigenere key (letters only): "))
    while not key:
        key = clean(input("Key cannot be empty. Enter key: "))
    col_order = read_order("Column order (e.g. 3 1 4 2): ")
    row_order = read_order("Row order (e.g. 2 3 1): ")
    print()

    if mode == "E":
        result = encrypt(text, key, col_order, row_order)
        print("\nFINAL CIPHERTEXT:", result)
    else:
        result = decrypt(text, key, col_order, row_order)
        print("\nDECRYPTED TEXT:", result)


if __name__ == "__main__":
    main()
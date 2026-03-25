# logic.py — All gate and adder logic (unchanged from original)

def gate_xor(a: int, b: int) -> int:
    return a ^ b

def gate_and(a: int, b: int) -> int:
    return a & b

def gate_or(a: int, b: int) -> int:
    return a | b

def full_adder(a: int, b: int, cin: int):
    sum_bit = gate_xor(gate_xor(a, b), cin)
    carry_out = gate_or(gate_and(a, b), gate_and(cin, gate_xor(a, b)))
    return sum_bit, carry_out

def ripple_carry_adder(a_bits, b_bits, cin):
    sum_bits = []
    carries = []
    c = cin
    for i in range(4):
        s, c_out = full_adder(a_bits[i], b_bits[i], c)
        sum_bits.append(s)
        carries.append(c_out)
        c = c_out
    return sum_bits, carries

def string_to_bits_lsb(binary_str):
    return [int(ch) for ch in reversed(binary_str)]

def bits_to_string_msb(bits_lsb):
    return ''.join(str(bit) for bit in reversed(bits_lsb))

def validate_binary(value):
    if len(value) != 4:
        return False
    return all(ch in ('0', '1') for ch in value)
```

**2d — Scroll down, commit the file:**
```
Commit message : Add logic.py — gate and adder functions

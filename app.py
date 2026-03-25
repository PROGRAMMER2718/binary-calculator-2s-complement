import streamlit as st

# ── Logic Gates ───────────────────────────────────────────────
def gate_xor(a, b): return a ^ b
def gate_and(a, b): return a & b
def gate_or(a, b):  return a | b

# ── Full Adder ────────────────────────────────────────────────
def full_adder(a, b, cin):
    sum_bit   = gate_xor(gate_xor(a, b), cin)
    carry_out = gate_or(gate_and(a, b), gate_and(cin, gate_xor(a, b)))
    return sum_bit, carry_out

# ── Ripple Carry Adder ────────────────────────────────────────
def ripple_carry_adder(a_bits, b_bits, cin):
    sum_bits, carries, c = [], [], cin
    for i in range(4):
        s, c_out = full_adder(a_bits[i], b_bits[i], c)
        sum_bits.append(s)
        carries.append(c_out)
        c = c_out
    return sum_bits, carries

# ── Helpers ───────────────────────────────────────────────────
def validate_binary(value):
    return len(value) == 4 and all(ch in ('0','1') for ch in value)

def string_to_bits_lsb(binary_str):
    return [int(ch) for ch in reversed(binary_str)]

def bits_to_string_msb(bits_lsb):
    return ''.join(str(bit) for bit in reversed(bits_lsb))

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="4-bit Binary Calculator",
    page_icon="⚡",
    layout="centered"
)

# ── Title ─────────────────────────────────────────────────────
st.title("⚡ 4-bit Binary Calculator")
st.caption("Logic Gate Simulation — Ripple Carry Adder with 2's Complement")
st.divider()

# ── Inputs ────────────────────────────────────────────────────
st.subheader("🔢 Inputs")

col1, col2 = st.columns(2)
with col1:
    a_str = st.text_input("A (4-bit binary)", value="0011", max_chars=4)
with col2:
    b_str = st.text_input("B (4-bit binary)", value="0001", max_chars=4)

mode_label = st.radio(
    "Operation Mode",
    options=["Addition", "Subtraction (2's Complement)"],
    horizontal=True
)
mode = 0 if mode_label == "Addition" else 1

st.divider()

# ── Preset Test Cases ─────────────────────────────────────────
st.subheader("🧪 Preset Test Cases")

tc1, tc2, tc3, tc4 = st.columns(4)
with tc1:
    if st.button("0011 + 0001"): a_str, b_str, mode = "0011", "0001", 0
with tc2:
    if st.button("0111 + 0001"): a_str, b_str, mode = "0111", "0001", 0
with tc3:
    if st.button("0100 - 0001"): a_str, b_str, mode = "0100", "0001", 1
with tc4:
    if st.button("1000 - 0001"): a_str, b_str, mode = "1000", "0001", 1

st.divider()

# ── Validate ──────────────────────────────────────────────────
st.subheader("📊 Results")

if not validate_binary(a_str) or not validate_binary(b_str):
    st.error("⚠️ Both A and B must be exactly 4-bit binary strings (only 0s and 1s).")
    st.stop()

# ── Calculate ─────────────────────────────────────────────────
a_bits     = string_to_bits_lsb(a_str)
b_bits     = string_to_bits_lsb(b_str)
M          = mode
b_mod_bits = [gate_xor(bit, M) for bit in b_bits]
cin        = M

sum_bits, carries = ripple_carry_adder(a_bits, b_mod_bits, cin)
C1, C2, C3, C4   = carries
overflow          = gate_xor(C3, C4)
result_str        = bits_to_string_msb(sum_bits)
mod_b_str         = bits_to_string_msb(b_mod_bits)
result_decimal    = int(result_str, 2)

# ── Metrics ───────────────────────────────────────────────────
r1, r2, r3 = st.columns(3)
r1.metric("Result (Binary)",  result_str)
r2.metric("Result (Decimal)", result_decimal)
r3.metric("Carry Out",        C4)

if overflow:
    st.error("🚨 Overflow Detected!")
else:
    st.success("✅ No Overflow")

st.divider()

# ── Circuit Visualization ─────────────────────────────────────
st.subheader("🔌 Circuit Visualization")

v1, v2 = st.columns(2)
with v1:
    st.markdown("**Modified B (XOR with M)**")
    st.code(mod_b_str, language=None)
    st.markdown("**2's Complement Status**")
    if mode == 1:
        st.info("🔄 Applied — B XOR 1, Cin = 1")
    else:
        st.info("➕ Not Applied — B XOR 0, Cin = 0")

with v2:
    st.markdown("**Ripple Carry Signals**")
    st.table({
        "Stage" : ["After Bit 0","After Bit 1","After Bit 2","After Bit 3"],
        "Carry" : [C1, C2, C3, C4]
    })

st.divider()

# ── Full Adder Breakdown ──────────────────────────────────────
st.subheader("🧩 Full Adder — Step by Step")

with st.expander("Click to see each Full Adder in detail"):
    carries_in = [cin, C1, C2, C3]
    for i in range(4):
        st.markdown(f"""
**Full Adder {i} (Bit {i})**
- Inputs → A={a_bits[i]}, B={b_mod_bits[i]}, Cin={carries_in[i]}
- Sum Bit → `{sum_bits[i]}`
- Carry Out → `{carries[i]}`
---
        """)
```

**Commit message:**
```
Fix: merge logic into single app.py to resolve import error

# app.py — Streamlit UI for 4-bit Binary Calculator

import streamlit as st
from logic import (
    ripple_carry_adder,
    string_to_bits_lsb,
    bits_to_string_msb,
    validate_binary,
    gate_xor
)

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="4-bit Binary Calculator",
    page_icon="⚡",
    layout="centered"
)

# ── Title ─────────────────────────────────────────────────────
st.title("⚡ 4-bit Binary Calculator")
st.caption("Logic Gate Simulation — Ripple Carry Adder with 2's Complement")
st.divider()

# ── Inputs Section ────────────────────────────────────────────
st.subheader("🔢 Inputs")

col1, col2 = st.columns(2)

with col1:
    a_str = st.text_input(
        "A (4-bit binary)",
        value="0011",
        max_chars=4,
        help="Enter exactly 4 bits e.g. 1010"
    )

with col2:
    b_str = st.text_input(
        "B (4-bit binary)",
        value="0001",
        max_chars=4,
        help="Enter exactly 4 bits e.g. 0101"
    )

# ── Mode Selection ────────────────────────────────────────────
mode_label = st.radio(
    "Operation Mode",
    options=["Addition", "Subtraction (2's Complement)"],
    horizontal=True
)
mode = 0 if mode_label == "Addition" else 1

st.divider()

# ── Preset Test Cases ─────────────────────────────────────────
st.subheader("🧪 Preset Test Cases")

tc_col1, tc_col2, tc_col3, tc_col4 = st.columns(4)

with tc_col1:
    if st.button("0011 + 0001"):
        a_str, b_str, mode = "0011", "0001", 0

with tc_col2:
    if st.button("0111 + 0001"):
        a_str, b_str, mode = "0111", "0001", 0

with tc_col3:
    if st.button("0100 - 0001"):
        a_str, b_str, mode = "0100", "0001", 1

with tc_col4:
    if st.button("1000 - 0001"):
        a_str, b_str, mode = "1000", "0001", 1

st.divider()

# ── Calculate ─────────────────────────────────────────────────
st.subheader("📊 Results")

# Validate inputs
if not validate_binary(a_str) or not validate_binary(b_str):
    st.error("⚠️ Both A and B must be exactly 4-bit binary strings (only 0s and 1s).")
    st.stop()

# Convert to LSB-first bits
a_bits = string_to_bits_lsb(a_str)
b_bits = string_to_bits_lsb(b_str)
M = mode

# 2's complement prep
b_mod_bits = [gate_xor(bit, M) for bit in b_bits]
cin = M

# Run ripple carry adder
sum_bits, carries = ripple_carry_adder(a_bits, b_mod_bits, cin)
C1, C2, C3, C4 = carries

# Compute overflow
overflow = gate_xor(C3, C4)

# Convert results to strings
result_str   = bits_to_string_msb(sum_bits)
mod_b_str    = bits_to_string_msb(b_mod_bits)
result_decimal = int(result_str, 2)

# ── Result Metrics ────────────────────────────────────────────
r1, r2, r3 = st.columns(3)

r1.metric("Result (Binary)", result_str)
r2.metric("Result (Decimal)", result_decimal)
r3.metric("Carry Out", C4)

# Overflow badge
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
    carry_data = {
        "Stage": ["After Bit 0", "After Bit 1", "After Bit 2", "After Bit 3"],
        "Carry": [C1, C2, C3, C4]
    }
    st.table(carry_data)

st.divider()

# ── Full Adder Breakdown ──────────────────────────────────────
st.subheader("🧩 Full Adder — Step by Step")

with st.expander("Click to see each Full Adder in detail"):
    carries_in = [cin, C1, C2, C3]
    for i in range(4):
        s_bit = sum_bits[i]
        c_out = carries[i]
        c_in  = carries_in[i]
        a_b   = a_bits[i]
        b_b   = b_mod_bits[i]
        st.markdown(f"""
**Full Adder {i} (Bit {i})**
- Inputs → A={a_b}, B={b_b}, Cin={c_in}
- Sum Bit → `{s_bit}`
- Carry Out → `{c_out}`
---
        """)

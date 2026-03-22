import tkinter as tk
from tkinter import messagebox, ttk

# ----------------------------------------------------------------------
# Logic gate simulations (only bitwise XOR, AND, OR are used)
# ----------------------------------------------------------------------
def gate_xor(a: int, b: int) -> int:
    """XOR gate (returns 0 or 1)"""
    return a ^ b

def gate_and(a: int, b: int) -> int:
    """AND gate (returns 0 or 1)"""
    return a & b

def gate_or(a: int, b: int) -> int:
    """OR gate (returns 0 or 1)"""
    return a | b

# ----------------------------------------------------------------------
# Full Adder built from basic gates
# ----------------------------------------------------------------------
def full_adder(a: int, b: int, cin: int):
    """
    Full adder using only XOR, AND, OR.
    Returns: (sum, carry_out)
    """
    sum_bit = gate_xor(gate_xor(a, b), cin)
    carry_out = gate_or(gate_and(a, b), gate_and(cin, gate_xor(a, b)))
    return sum_bit, carry_out

# ----------------------------------------------------------------------
# 4-bit Ripple Carry Adder (uses 4 full adders)
# ----------------------------------------------------------------------
def ripple_carry_adder(a_bits, b_bits, cin):
    """
    a_bits, b_bits : list of 4 ints (LSB first, i.e., index 0 = bit0)
    cin : initial carry-in (int 0 or 1)
    Returns:
        sum_bits : list of 4 ints (LSB first)
        carries  : list of 4 ints [c1, c2, c3, c4] where
                   c1 = carry out after bit0,
                   c2 = after bit1,
                   c3 = after bit2,
                   c4 = after bit3 (final carry out)
    """
    sum_bits = []
    carries = []
    c = cin
    for i in range(4):
        s, c_out = full_adder(a_bits[i], b_bits[i], c)
        sum_bits.append(s)
        carries.append(c_out)
        c = c_out
    return sum_bits, carries

# ----------------------------------------------------------------------
# Main GUI Application
# ----------------------------------------------------------------------
class BinaryCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("4-bit Binary Calculator (Logic Gate Simulation)")
        self.root.resizable(False, False)

        # Variables
        self.a_var = tk.StringVar()
        self.b_var = tk.StringVar()
        self.mode_var = tk.IntVar(value=0)          # 0 = addition, 1 = subtraction

        # Build GUI
        self.create_widgets()

    def create_widgets(self):
        # ---------- Input Frame ----------
        input_frame = ttk.LabelFrame(self.root, text="Inputs", padding=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(input_frame, text="A (4-bit binary):").grid(row=0, column=0, sticky="w")
        ttk.Entry(input_frame, textvariable=self.a_var, width=10).grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="B (4-bit binary):").grid(row=1, column=0, sticky="w")
        ttk.Entry(input_frame, textvariable=self.b_var, width=10).grid(row=1, column=1, padx=5)

        # Mode selection (radio buttons)
        ttk.Label(input_frame, text="Mode:").grid(row=2, column=0, sticky="w", pady=(10,0))
        ttk.Radiobutton(input_frame, text="Addition", variable=self.mode_var, value=0).grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(input_frame, text="Subtraction (2's complement)", variable=self.mode_var, value=1).grid(row=2, column=2, sticky="w")

        ttk.Button(input_frame, text="Calculate", command=self.calculate).grid(row=3, column=0, columnspan=3, pady=10)

        # ---------- Output Frame ----------
        output_frame = ttk.LabelFrame(self.root, text="Results", padding=10)
        output_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.result_label = ttk.Label(output_frame, text="Result: ---", font=("Courier", 10))
        self.result_label.grid(row=0, column=0, sticky="w")

        self.carry_out_label = ttk.Label(output_frame, text="Carry Out: ---")
        self.carry_out_label.grid(row=1, column=0, sticky="w")

        self.overflow_label = ttk.Label(output_frame, text="Overflow: ---")
        self.overflow_label.grid(row=2, column=0, sticky="w")

        # ---------- Visualization Frame ----------
        vis_frame = ttk.LabelFrame(self.root, text="Digital Circuit Visualization", padding=10)
        vis_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # Modified B (after XOR with mode)
        self.mod_b_label = ttk.Label(vis_frame, text="Modified B (XOR with M): ---")
        self.mod_b_label.grid(row=0, column=0, sticky="w", pady=2)

        # Internal carries (C1, C2, C3, C4)
        self.carries_label = ttk.Label(vis_frame, text="Carry values: C1=---, C2=---, C3=---, C4=---")
        self.carries_label.grid(row=1, column=0, sticky="w", pady=2)

        # Informational labels (to satisfy "2's Complement Applied" and "Ripple Carry in Action")
        self.twos_comp_label = ttk.Label(vis_frame, text="2's Complement: not applied", foreground="blue")
        self.twos_comp_label.grid(row=2, column=0, sticky="w", pady=2)

        self.ripple_label = ttk.Label(vis_frame, text="Ripple Carry in Action (4 full adders)", foreground="green")
        self.ripple_label.grid(row=3, column=0, sticky="w", pady=2)

        # ---------- Test Cases Frame ----------
        test_frame = ttk.LabelFrame(self.root, text="Test Cases (Predefined)", padding=10)
        test_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Addition test cases
        ttk.Button(test_frame, text="Add: 0011 + 0001", command=lambda: self.set_test_case("0011", "0001", 0)).grid(row=0, column=0, padx=2, pady=2)
        ttk.Button(test_frame, text="Add: 0111 + 0001", command=lambda: self.set_test_case("0111", "0001", 0)).grid(row=0, column=1, padx=2, pady=2)

        # Subtraction test cases
        ttk.Button(test_frame, text="Sub: 0100 - 0001", command=lambda: self.set_test_case("0100", "0001", 1)).grid(row=1, column=0, padx=2, pady=2)
        ttk.Button(test_frame, text="Sub: 1000 - 0001", command=lambda: self.set_test_case("1000", "0001", 1)).grid(row=1, column=1, padx=2, pady=2)

    def validate_binary(self, value):
        """Return True if value is a 4-bit binary string (only 0/1, length 4)"""
        if len(value) != 4:
            return False
        return all(ch in ('0', '1') for ch in value)

    def string_to_bits_lsb(self, binary_str):
        """Convert 'abcd' (MSB first) to list [d,c,b,a] (LSB first)"""
        # binary_str like "1010" -> bits [0,1,0,1] (LSB first)
        return [int(ch) for ch in reversed(binary_str)]

    def bits_to_string_msb(self, bits_lsb):
        """Convert bits LSB-first list to MSB-first binary string"""
        # bits_lsb = [b0, b1, b2, b3] -> string "b3b2b1b0"
        return ''.join(str(bit) for bit in reversed(bits_lsb))

    def calculate(self):
        """Main calculation using only logic gates (no + or - operators)"""
        # Get user inputs
        a_str = self.a_var.get().strip()
        b_str = self.b_var.get().strip()
        mode = self.mode_var.get()          # 0 = add, 1 = subtract

        # Validate inputs
        if not self.validate_binary(a_str) or not self.validate_binary(b_str):
            messagebox.showerror("Invalid Input", "Both A and B must be 4-bit binary strings (e.g., 1010).")
            return

        # Convert to LSB-first lists of ints
        a_bits = self.string_to_bits_lsb(a_str)   # [LSB, ..., MSB]
        b_bits = self.string_to_bits_lsb(b_str)

        # Mode: M = 1 for subtraction, 0 for addition
        M = mode

        # ---------- 2's complement preparation (XOR with M) ----------
        # Modified B = B XOR M (bitwise)
        b_mod_bits = [gate_xor(bit, M) for bit in b_bits]

        # Initial carry-in = M
        cin = M

        # ---------- Ripple Carry Adder (only logic gates) ----------
        sum_bits, carries = ripple_carry_adder(a_bits, b_mod_bits, cin)

        # carries[0] = C1 (after bit0), carries[1]=C2, carries[2]=C3, carries[3]=C4
        C1, C2, C3, C4 = carries[0], carries[1], carries[2], carries[3]

        # Overflow = C3 XOR C4
        overflow = gate_xor(C3, C4)

        # Convert result to MSB-first string for display
        result_str = self.bits_to_string_msb(sum_bits)

        # Convert Modified B to MSB-first string for display
        mod_b_str = self.bits_to_string_msb(b_mod_bits)

        # Update GUI
        self.result_label.config(text=f"Result: {result_str}")
        self.carry_out_label.config(text=f"Carry Out: {C4}")
        self.overflow_label.config(text=f"Overflow: {'Yes' if overflow else 'No'}")

        self.mod_b_label.config(text=f"Modified B (XOR with M): {mod_b_str}")
        self.carries_label.config(text=f"Carry values: C1={C1}, C2={C2}, C3={C3}, C4={C4}")

        # Update informational labels
        if mode == 1:
            self.twos_comp_label.config(text="2's Complement Applied (B XOR 1, Cin=1)")
        else:
            self.twos_comp_label.config(text="2's Complement not applied (B XOR 0, Cin=0)")
        # Ripple label remains static but we keep it visible

    def set_test_case(self, a_val, b_val, mode):
        """Fill in the test case values and run calculation"""
        self.a_var.set(a_val)
        self.b_var.set(b_val)
        self.mode_var.set(mode)
        self.calculate()

# ----------------------------------------------------------------------
# Main execution
# ----------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryCalculatorApp(root)
    root.mainloop()
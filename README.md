# Binary Calculator using 2's Complement

##  Project Overview
This project implements a 4-bit binary calculator capable of performing:
- Binary Addition
- Binary Subtraction using 2’s Complement
- Overflow Detection

The system is designed using digital logic principles and simulates:
- Logic Gates (XOR, AND, OR)
- Full Adder
- Ripple Carry Adder

---

## Objective
To design a combinational circuit-based calculator that performs binary addition and subtraction using 2’s complement method.

---

## Concepts Used
- Binary Arithmetic  
- 1’s and 2’s Complement  
- Combinational Circuits  
- Full Adder  
- Ripple Carry Adder  
- Overflow Detection  

---

##  Modules Implemented

### 1. Binary Adder
- Implemented using 4 Full Adders  
- Performs bit-by-bit addition  

### 2. 2’s Complement Generator
- XOR gates are used to invert input B when subtraction mode is selected  
- Carry-in is set to 1 to complete 2’s complement  

### 3. Overflow Detection
- Overflow is detected using carry comparison logic  

---

##  Test Cases

### Addition (M = 0)

| A     | B     | Result |
|-------|-------|--------|
| 0101  | 0011  | 1000   |
| 0111  | 0001  | 1000 (Overflow) |

---

### Subtraction (M = 1)

| A     | B     | Result |
|-------|-------|--------|
| 0101  | 0011  | 0010   |
| 0011  | 0101  | 1110   |
| 0111  | 1111  | 1000 (Overflow) |

---


---

## Key Features
- Implements arithmetic using logic gates instead of direct operators  
- Uses ripple carry adder for computation  
- Supports both addition and subtraction  
- Includes overflow detection mechanism  

---
## Conclusion
This project demonstrates how binary arithmetic operations can be implemented using fundamental digital logic components, making it a practical application of combinational circuit design.

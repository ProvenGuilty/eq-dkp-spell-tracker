
# EQ DKP Spell Tracker - Spell Casting and Skill-Ups Tracker

This Python script processes **EverQuest (P99)** log files to calculate the total active time spent casting spells, the total AFK time, skill-ups for various skills, and experience message counts. It also allows you to optionally view detailed statistics and debug information.

The script supports the following features:
- Calculate **active time** spent casting spells.
- Track **AFK time** based on gaps between spell casts.
- Detect and report **skill-ups** (Alteration, Meditate, Channeling, etc.).
- Summarize **total experience messages**.
- Optional **verbose output** (`-v`) to include detailed statistics (log entries scanned, first/last cast times).
- Optional **debug output** (`-d`) to show detailed processing logs.

### **Features**
- **Default Output**: Displays the **total active time** and **AFK time** spent casting spells, along with **skill-up statistics** and the **total experience messages** detected.
- **Verbose Output** (`-v`): Includes **additional statistics**, such as the **total number of log entries**, **first and last cast entries**, and other metadata.
- **Debug Output** (`-d`): Enables detailed processing information, including timestamps and other debug details.

### **Installation**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/provenguilty/eq-dkp-spell-tracker.git
   cd eq-dkp-spell-tracker
   ```

2. **Install Python** (if not already installed):
   - Ensure you have Python 3.x installed. You can download it from the [official Python website](https://www.python.org/downloads/).

3. **Run the script**:
   After setting up, run the script directly from your terminal:
   ```bash
   python eq_dkp_spell_tracker.py
   ```

### **Usage**

- **Default Output (Clean Summary)**:
   ```bash
   python eq_dkp_spell_tracker.py
   ```

- **Verbose Output (With Statistics)**:
   ```bash
   python eq_dkp_spell_tracker.py -v
   ```

- **Debug Output (With Detailed Processing)**:
   ```bash
   python eq_dkp_spell_tracker.py -d
   ```

- **Combined Verbose and Debug Output**:
   ```bash
   python eq_dkp_spell_tracker.py -v -d
   ```

### **Example Output**

**Clean Output (Default)**:
```
Total active time spent casting spells: 7231.25 seconds
Total AFK time: 28486.25 seconds
Total processing time: 8.35 seconds

Skill-ups detected:
Alteration: 9 -> 167 (+158)
Channeling: 3 -> 144 (+141)
Meditate: 54 -> 178 (+124)

Total experience messages detected: 42
```

**Verbose Output**:
```
Total active time spent casting spells: 7231.25 seconds
Total AFK time: 28486.25 seconds
Total processing time: 8.35 seconds

Skill-ups detected:
Alteration: 9 -> 167 (+158)
Channeling: 3 -> 144 (+141)
Meditate: 54 -> 178 (+124)

Total experience messages detected: 42

Statistics:
Total log entries scanned: 6590
First cast entry: 2025-04-11 10:42:27
Last cast entry: 2025-04-11 20:37:44
```

### **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

### **Credits**

This script was created through **Vibe Coding** and **Prompt Engineering** in tandem with **ChatGPT-4o Mini**.

### **Author**
- [Christopher Ryan](https://github.com/provenguilty) - GitHub Profile


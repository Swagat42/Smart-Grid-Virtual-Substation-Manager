# ⚙️ Features and Logic

What each button does internally, step by step.

---

## ➕ Add Substation
1. A pop-up asks for **Name**, **Location** and **Capacity (MW)**.
2. Capacity is converted with `float()`. On failure the user sees *"Enter valid capacity (number)."*
3. A `Substation(name, location, capacity)` is created with load `0.0` and status `Offline`.
4. `SmartGridManager.add_substation()` appends it and calls `save_data()`.
5. The console prints `Added: <substation>` and the pop-up closes.

## 🗑️ Remove Substation
1. A pop-up asks for the **name**.
2. The manager scans the list and removes the **first** match, then rewrites the file.
3. The console prints `Removed Substation: <name>`, or an error appears if nothing matched.

## 📋 List Substations
Prints a `--- List of Substations ---` header and then `str(sub)` for every object:
```text
Sub1 | Coimbatore | 240.0 MW | Load: 0.0 MW | Offline
```
If the list is empty, it prints *"No substations available."*

## 🔄 Update Status
1. A pop-up asks for **name** and **status** (placeholder: `Online/Offline`).
2. The matching object's `update_status()` is called, then the data is saved.
3. The console confirms with `<name> status updated to <status>`.

## ⚡ Update Load
1. A pop-up asks for **name** and **new load (MW)**, converted with `float()`.
2. `Substation.update_load()` applies the rules:

```text
            load ≤ capacity ?
             ┌────┴────┐
            yes        no ──▶ ❌ "Load exceeds capacity" (value unchanged)
             │
     set current_load
             │
   load > 0.8 × capacity ?
        ┌────┴────┐
       yes        no ──▶ ✅ accepted silently
        │
  ⚠️ "exceeds 80% capacity" (value still accepted)
```

3. The data is saved and the console prints the update.

> ℹ️ The console message is printed even when step 2 rejects the load. See *Known quirks* in the main README.

## 📊 Total Energy Flow
```python
sum(sub.current_load for sub in self.substations)
```
This is a software-level total of the entered loads, **not** a physical power-flow result.

## 📑 Report Status
Prints `--- Status Report ---` followed by `<name>: <status>` for each substation.

## 💾 Persistence
| Direction | Method | Detail |
|---|---|---|
| Object → text | `to_text()` | `name,location,capacity,current_load,status` |
| Text → object | `Substation.from_text()` | Splits on `,`; exactly 5 fields are required, otherwise `ValueError` |
| Save | `save_data()` | Rewrites the whole file after every change |
| Load | `load_data()` | Runs at startup; skips blank lines and lines that raise `ValueError` |

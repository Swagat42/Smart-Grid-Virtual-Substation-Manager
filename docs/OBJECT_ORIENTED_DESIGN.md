# 🧱 Object-Oriented Design

The application is split into three classes, each with a single, clear job.

```text
SmartGridApp                     ← presentation layer (GUI)
   │
   └── owns ──▶ SmartGridManager  ← application logic + persistence
                     │
                     └── manages ──▶ [ Substation, Substation, ... ]  ← data model
```

---

## 🔌 `Substation`: the data model

Represents **one** substation and owns the rules for changing it.

| Attribute | Type | Default | Meaning |
|---|---|---|---|
| `name` | `str` | – | Identifier used for lookups |
| `location` | `str` | – | City or site |
| `capacity` | `float` | – | Rated capacity in MW |
| `current_load` | `float` | `0.0` | Present load in MW |
| `status` | `str` | `"Offline"` | Operating state |

| Method | Kind | Purpose |
|---|---|---|
| `update_status(status)` | instance | Replace the status string |
| `update_load(load)` | instance | Accept the load only if `load ≤ capacity`; warn above 80 % |
| `to_text()` | instance | Serialise to `name,location,capacity,current_load,status\n` |
| `from_text(line)` | **class method** | Alternate constructor: parse a stored line back into an object |
| `__str__()` | **dunder** | Human-readable line shown in the console |

---

## 🧠 `SmartGridManager`: the collection manager

Owns the list of `Substation` objects and is the **only** class that touches `data.txt`.

| Method | Responsibility |
|---|---|
| `__init__(file_path="data.txt")` | Creates an empty list, then calls `load_data()` |
| `add_substation(sub)` | Appends the object and saves |
| `remove_substation(name)` | Removes the first matching name and saves; returns `True` or `False` |
| `total_energy_flow()` | `sum(sub.current_load for sub in self.substations)` |
| `save_data()` | Rewrites the file from the in-memory list |
| `load_data()` | Rebuilds the list from the file, skipping blank or invalid lines |

---

## 🖥️ `SmartGridApp`: the presentation layer

Builds the CustomTkinter window (dark mode, blue theme, 400 × 700) and translates button clicks into manager or substation calls.

| Responsibility | How |
|---|---|
| Layout | `CTkLabel` header, eight `CTkButton`s and a `CTkTextbox` output console |
| Input | One `CTkToplevel` pop-up per action, with `CTkEntry` fields |
| Feedback | Results go to the console, problems to `tkinter.messagebox` |
| Delegation | Never edits the file directly; always goes through `SmartGridManager` |

---

## 🎓 Principles in practice

| Principle | Evidence |
|---|---|
| **Encapsulation** | Capacity and 80 % checks live inside `Substation.update_load()`, next to the data they protect |
| **Abstraction** | The GUI has no knowledge of the storage format |
| **Composition** | App → Manager → many Substations |
| **Single responsibility** | Model, logic and view are separate classes, even though they share one source file |
| **Alternate constructor** | `@classmethod from_text()` |

### Possible refactor
Splitting `src/Proj2.py` into `substation.py`, `manager.py` and `app.py` would make the layering visible at the file level too. It would also let `Substation` and `SmartGridManager` be unit-tested without a GUI. To do that, `update_load()` would raise or return a result instead of calling `messagebox` itself.

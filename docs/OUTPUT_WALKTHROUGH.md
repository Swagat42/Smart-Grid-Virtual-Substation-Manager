# 🎬 Output Walkthrough

One complete session, captured in eleven screenshots (`images/output/`).

| # | Screenshot | Action | Console shows |
|:-:|---|---|---|
| 01 | `01-main-window.png` | Launch the app | Empty console, eight action buttons |
| 02 | `02-add-substation-sub1.png` | Add **Sub1**: Coimbatore, 240 MW | Pop-up with the three fields |
| 03 | `03-add-substation-sub2.png` | Add **Sub2**: Chennai, 165 MW | `Added: Sub1 …` already listed |
| 04 | `04-list-substations.png` | List Substations | Both at 0.0 MW and Offline |
| 05 | `05-update-status.png` | Set **Sub1 → Online** | Pop-up with name and status |
| 06 | `06-update-load.png` | Set **Sub2 → 50 MW** | `Sub1 status updated to Online` |
| 07 | `07-total-energy-flow.png` | Total Energy Flow | `Total Energy Flow: 50.0 MW` |
| 08 | `08-list-after-updates.png` | List again | Sub1 Online, Sub2 50.0 MW |
| 09 | `09-status-report.png` | Report Status | `Sub1: Online` · `Sub2: Offline` |
| 10 | `10-remove-substation.png` | Remove **Sub1** | Pop-up with `Sub1` entered |
| 11 | `11-final-list-after-removal.png` | List after removal | Only `Sub2 \| Chennai \| 165.0 MW \| Load: 50.0 MW \| Offline` |

### What the session demonstrates
- ✅ Object creation with default load (0 MW) and status (Offline)
- ✅ Independent updates to status and load on different substations
- ✅ Aggregation across all objects (0 + 50 = 50 MW)
- ✅ Deletion and a consistent list afterwards
- ✅ Every step persisted to `data.txt`

The screenshots are also embedded as a gallery in the main [README](../README.md#-demo-walkthrough).

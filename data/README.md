# 💾 Data

The app stores its state in **`data.txt`**, created in the folder you launch it from. The file is git-ignored because it changes every time you use the app.

## Format

One substation per line, five comma-separated fields:

| Field | Type | Example |
|---|---|---|
| `name` | text | `Sub1` |
| `location` | text | `Coimbatore` |
| `capacity` | number (MW) | `240.0` |
| `current_load` | number (MW) | `0.0` |
| `status` | text | `Online` |

```text
Sub1,Coimbatore,240.0,0.0,Online
Sub2,Chennai,165.0,50.0,Offline
```

## Demo data

[`sample_data.txt`](sample_data.txt) contains the two substations from the demo. To start with them loaded:

```bash
cp data/sample_data.txt data.txt     # Windows: copy data\sample_data.txt data.txt
python src/Proj2.py
```

## Rules
- Lines without exactly five fields are **skipped** on load, and the app still starts.
- Avoid commas inside names or locations, because they break the format.

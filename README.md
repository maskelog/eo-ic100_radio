# I can't believe it's a radio!

Python proof of concept of using EO-IC100's FM radio function.

Based on decompiled Note10 framework.

Tested on EO-IC100BBEGKR (Korean model of EO-IC100) firmware version 0.56_050401_aa

![image](https://github.com/user-attachments/assets/4e2d6333-c526-4959-aad2-e1f0257fd2c4)
 
## Functions Working
- Turn on/off radio
- Frequency tuning
- Set volume/mute
- Get RDS data

## Favorites Feature (2x4 Layout)
- **2x4 Favorites Layout:**  
  The UI now includes 8 favorites buttons arranged in 2 rows by 4 columns for quick access.
  
- **Configuration:**  
  Right-click a favorites button to edit its station name and frequency.
  
- **Persistence with JSON:**  
  Favorites are saved in a JSON file (`favorites.json`) so that your settings persist between sessions.

### JSON Structure for Favorites
Favorites are stored as an array of objects. Each object has:
- `name`: Station name
- `freq`: Frequency in hundredths of MHz (e.g., 91.5 MHz is stored as `9150`)

Example:
```json
[
  { "name": "KBS 1FM", "freq": 9730 },
  { "name": "MBC FM4U", "freq": 9190 },
  { "name": "kbs classic fm", "freq": 9310 },
  { "name": "CBS MUSIC", "freq": 9390 },
  { "name": "MBC FM", "freq": 9590 },
  { "name": "SBS LOVE FM", "freq": 10350 },
  { "name": "EBS FM", "freq": 10450 },
  { "name": "Power FM", "freq": 10770 }
]


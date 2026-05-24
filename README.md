# ⚔️ TBC Farm Calculator
FarmCalcTBC: A simple web-based tool to calculate farming materials for TBC 2.4.3.

## features:
- "Interactive UI with Streamlit"
- "Dynamic CSV Database support"
- "Real-time item and reagent icons"
- "Automatic quantity stacking and synchronization"

# DATABASE FORMAT (mats.csv)
- Tipe: "Item category (Flask, Elixir, etc.)"
- Name: "Item name"
- icons_name: "URL for the consumable icon"
- Description: "Item effect or notes"
- n1_to_n4: "Quantities for reagents"
- Reagent_1_to_4: "Names of required materials"
- Icons: "Reagent name for icon mapping"
- icons_img: "URL for the reagent icon"

# License

GNU General Public License v3.0

FarmCalcTBC is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation.

# Release Notes 

### v1.1.0: The Persistence & UX Update

[New Feature] Added Browser Local Storage support: Your farming list now survives page refreshes (F5).
[UX/UI] Implemented color-coded categories (Flasks, Elixirs, Potions, Food) for better visual organization.
[Bugfix] Fixed JSON serialization error when adding items to the cart (Pandas Series to Dict conversion).
[Improvement] Optimized UI flow: Item cards now start collapsed for a cleaner look.

### v1.2.0: The Stability & Sync Update

[Bugfix] Fixed a Local Storage synchronization issue where deleted items or modified quantities would revert after a page refresh. Implemented Streamlit callbacks (`on_click` and `on_change`) for seamless state management.

### v1.3.0: The Task Tracking Update

[New Feature] Added a "Done?" checkbox column to the Total Shopping List to interactively track farmed materials.

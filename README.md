# ⚔️ TBC Farm Calculator
FarmCalcTBC: A simple web-based tool to calculate farming materials for TBC 2.4.3.

## features:
- "Interactive UI with Streamlit"
- "Dynamic CSV Database support"
- "Real-time item and reagent icons"
- "Automatic quantity stacking and synchronization"
installation:
step_1: "git clone https://github.com/debian-shamy/FarmCalcTBC.git"
step_2: "pip install -r requirements.txt"
step_3: "streamlit run app.py"
usage:
sidebar: "Select category, item, and quantity. Use +5/+10 buttons for quick adds."
main_page: "View detailed recipe breakdown and consolidated Shopping List."

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

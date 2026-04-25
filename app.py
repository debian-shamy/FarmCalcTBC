"""
TBC Farm Calculator
Description: A web-based tool to calculate materials needed for TBC WoW crafting.
Author: Debian
License: GNU General Public License v3.0
"""

import streamlit as st
import pandas as pd
import os

# --- Page Configuration ---
st.set_page_config(page_title="TBC Farm Calc", page_icon="⚔️", layout="wide")

# --- Data Logic ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(CURRENT_DIR, 'mats.csv')

@st.cache_data
def load_data() -> pd.DataFrame:
    """Loads material data from the CSV file."""
    return pd.read_csv(CSV_PATH)

df = load_data()

# --- Reagent Icon Mapping ---
# Maps reagent names (Icons column) to their image URLs (icons_img column)
reagent_icon_map = {}
for _, row in df.dropna(subset=['Icons', 'icons_img']).iterrows():
    name = str(row['Icons']).strip()
    url = str(row['icons_img']).strip()
    if name:
        reagent_icon_map[name] = url

# --- Session State Initialization ---
def init_session_state():
    """Initializes the required session state variables."""
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    if 'item_qty' not in st.session_state:
        st.session_state.item_qty = 0  

    if 'show_success' not in st.session_state:
        st.session_state.show_success = False

    if 'show_error' not in st.session_state:
        st.session_state.show_error = False

init_session_state()

# --- Callback Functions ---
def clear_cart():
    """Wipes the cart and clears associated widget memory."""
    st.session_state.cart = []
    # Clean up widget keys to prevent stale values
    for key in list(st.session_state.keys()):
        if key.startswith("q_cart_"):
            del st.session_state[key]

def increment_qty(val: int):
    """Increments the current input quantity."""
    st.session_state.item_qty += val

def add_to_cart(name: str, category: str, data: pd.Series):
    """Adds item to cart, stacks quantities, and syncs UI state."""
    qty_to_add = st.session_state.item_qty
    
    if qty_to_add <= 0:
        st.session_state.show_error = True
        return

    item_found = False
    for item in st.session_state.cart:
        if item['name'] == name:
            new_total = item['qty'] + qty_to_add
            item['qty'] = new_total
            
            # Sync main page number_input widget
            widget_key = f"q_cart_{name}"
            if widget_key in st.session_state:
                st.session_state[widget_key] = new_total
                
            item_found = True
            break
            
    if not item_found:
        st.session_state.cart.append({
            'name': name,
            'qty': qty_to_add,
            'type': category,
            'desc': data['Desciption'],
            'data': data,
            'icon': data['icons_name'] # Main item icon
        })
        
    st.session_state.item_qty = 0 # Reset sidebar counter
    st.session_state.show_success = True

# --- SIDEBAR: Input Panel ---
st.sidebar.header("⚒️ Crafting Panel")

# 1. Category Selection
categories = df['Tipe'].dropna().unique()
selected_cat = st.sidebar.selectbox("1. Category", categories, index=None, placeholder="Select category...")

if selected_cat:
    # 2. Item Selection
    items_in_cat = df[df['Tipe'] == selected_cat]['Name'].unique()
    selected_item = st.sidebar.selectbox("2. Consumable", items_in_cat, index=None, placeholder="Select item...")
    
    if selected_item:
        row = df[df['Name'] == selected_item].iloc[0]
        
        # Display Item Icon and Description in Sidebar
        col_side_img, col_side_txt = st.sidebar.columns([1, 3])
        with col_side_img:
            if pd.notna(row['icons_name']):
                st.image(row['icons_name'], width=50)
        with col_side_txt:
            st.caption(f"_{row['Desciption']}_")
        
        # 3. Quantity Input
        st.sidebar.number_input("3. Quantity", min_value=0, step=1, key="item_qty")
        
        # Shortcut Buttons
        c1, c2, c3, c4 = st.sidebar.columns(4)
        c1.button("+5", use_container_width=True, on_click=increment_qty, args=(5,))
        c2.button("+10", use_container_width=True, on_click=increment_qty, args=(10,))
        c3.button("+15", use_container_width=True, on_click=increment_qty, args=(15,))
        c4.button("+20", use_container_width=True, on_click=increment_qty, args=(20,))
        
        st.sidebar.markdown("<br>", unsafe_allow_html=True)
        
        # Add Button
        st.sidebar.button(
            "Add to List ➕", 
            use_container_width=True,
            on_click=add_to_cart,
            args=(selected_item, selected_cat, row)
        )
        
        # Feedback Messages
        if st.session_state.show_error:
            st.sidebar.warning("Quantity must be greater than zero!")
            st.session_state.show_error = False
        if st.session_state.show_success:
            st.sidebar.success("Cart updated!")
            st.session_state.show_success = False

if st.session_state.cart:
    st.sidebar.divider()
    st.sidebar.button("Clear All 🗑️", on_click=clear_cart)

# --- MAIN PAGE ---
st.title("⚔️ TBC Farm Calculator")

if not st.session_state.cart:
    st.info("Your cart is empty. Use the sidebar to add consumables.")
else:
    st.subheader("📋 Items in Cart")
    grand_total_mats = {}

    for idx, cart_item in enumerate(st.session_state.cart):
        name = cart_item['name']
        qty = cart_item['qty']
        data = cart_item['data']
        
        with st.expander(f"📦 {qty}x {name}", expanded=True):
            img_col, info_col, ctrl_col = st.columns([1, 4, 3], vertical_alignment="center")
            
            with img_col:
                if pd.notna(cart_item['icon']):
                    st.image(cart_item['icon'], width=65)
            
            with info_col:
                st.markdown(f"### {name}")
                st.caption(f"**Effect:** {cart_item['desc']}")
            
            with ctrl_col:
                q_col, d_col = st.columns([2, 1], vertical_alignment="center")
                with q_col:
                    new_q = st.number_input("Qty", value=qty, min_value=1, step=1, key=f"q_cart_{name}", label_visibility="collapsed")
                    if new_q != qty:
                        st.session_state.cart[idx]['qty'] = new_q
                        st.rerun()
                with d_col:
                    if st.button("🗑️", key=f"del_{name}"):
                        st.session_state.cart.pop(idx)
                        if f"q_cart_{name}" in st.session_state:
                            del st.session_state[f"q_cart_{name}"]
                        st.rerun()

            st.divider()

            # Ingredients Breakdown
            left_col, right_col = st.columns(2)
            with left_col:
                st.markdown("**📝 Recipe (1 unit):**")
                for i in range(1, 5):
                    reagent = data[f'Reagent {i}']
                    if pd.notna(reagent) and str(reagent).strip() != "":
                        st.markdown(f"• {reagent}: **{int(data[f'n{i}'])}**")

            with right_col:
                st.markdown("**🚜 Total for Farming:**")
                for i in range(1, 5):
                    reagent = data[f'Reagent {i}']
                    if pd.notna(reagent) and str(reagent).strip() != "":
                        r_name = str(reagent).strip()
                        total_req = int(data[f'n{i}']) * qty
                        st.markdown(f"• {r_name}: **{total_req}**")
                        grand_total_mats[r_name] = grand_total_mats.get(r_name, 0) + total_req

    # --- FINAL SHOPPING LIST ---
    st.markdown("---")
    with st.expander("📊 **TOTAL SHOPPING LIST**", expanded=True):
        if grand_total_mats:
            sorted_data = []
            for mat in sorted(grand_total_mats.keys()):
                sorted_data.append({
                    "Icon": reagent_icon_map.get(mat, ""),
                    "Ingredient": mat, 
                    "Total Amount": grand_total_mats[mat]
                })
            
            st.dataframe(
                pd.DataFrame(sorted_data),
                column_config={
                    "Icon": st.column_config.ImageColumn("", width="small"),
                    "Ingredient": "Material Name",
                    "Total Amount": st.column_config.NumberColumn("Quantity", format="%d")
                },
                hide_index=True, 
                use_container_width=True
            )

st.markdown("<br><center><small>TBC Farm Calc - Developed for the TBC community</small></center>", unsafe_allow_html=True)
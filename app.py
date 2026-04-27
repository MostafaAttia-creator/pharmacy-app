
import streamlit as st
import sqlite3
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Pharmacy System",
    page_icon="💊",
    layout="wide"
)

# DB
conn = sqlite3.connect("pharmacy.db")
cursor = conn.cursor()

# Title
st.title("💊 Pharmacy Sales System")

# Load Data
medicines = pd.read_sql_query("SELECT * FROM Medicines", conn)
customers = pd.read_sql_query("SELECT * FROM Customers", conn)
sales = pd.read_sql_query("SELECT * FROM Sales", conn)

# Sidebar
st.sidebar.header("⚙️ Navigation")
page = st.sidebar.radio("Go to", ["Sales", "Database"])

# SALES PAGE
if page == "Sales":

    st.subheader("📊 Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("💊 Medicines", len(medicines))
    col2.metric("👥 Customers", len(customers))
    col3.metric("🧾 Sales", len(sales))

    st.divider()

# Input Section
    col1, col2 = st.columns(2)

    with col1:
        customer_name = st.text_input("👤 Customer Name", key="customer_name")

    with col2:
        medicine = st.selectbox(
            "💊 Select Medicine",
            medicines["Name"].unique()
        )

    med_row = medicines[medicines["Name"] == medicine].iloc[0]

    med_id = med_row["Med_ID"]
    price = med_row["Price"]
    stock = med_row["Quantity"]

# Info Section
    info1, info2 = st.columns(2)
    info1.info(f"💰 Price: {price}")
    info2.warning(f"📦 Stock: {stock}")

# Quantity
    if stock == 0:
        st.error("❌ Out of stock")

    qty = st.number_input(
        "Enter Quantity",
        min_value=1,
        max_value=int(stock) if stock > 0 else 1,
        step=1
    )

# Cart
    if "cart" not in st.session_state:
        st.session_state.cart = []

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Add to Cart", width='stretch'):
            if stock == 0:
                st.error("No stock available")
            else:
                st.session_state.cart.append({
                    "med_id": int(med_id),
                    "name": medicine,
                    "qty": qty,
                    "price": price,
                    "total": qty * price
                })
                st.success("Added to cart")

    with col2:
        if st.button("🗑️ Clear Cart", width='stretch'):
            st.session_state.cart = []
            st.warning("Cart cleared")

# Show Cart
    st.subheader("🛒 Cart")

    if len(st.session_state.cart) == 0:
        st.info("Cart is empty")
    else:
        cart_df = pd.DataFrame(st.session_state.cart)
        st.dataframe(cart_df, width='stretch')

        total = cart_df["total"].sum()
        st.success(f"💰 Total = {total}")

    # Sell
    if st.button("🛒 Sell Now", width="stretch"):

        if not customer_name:
            st.error("Enter customer name")

        elif len(st.session_state.cart) == 0:
            st.error("Cart is empty")

        else:
            cursor.execute("SELECT Customer_ID FROM Customers WHERE Name = ?", (customer_name,))
            row = cursor.fetchone()

            if row:
                customer_id = row[0]
            else:
                cursor.execute("INSERT INTO Customers (Name) VALUES (?)", (customer_name,))
                conn.commit()
                customer_id = cursor.lastrowid

            total = sum(item["total"] for item in st.session_state.cart)

            cursor.execute("""
                INSERT INTO Sales (Customer_ID,Total_Amount)
                VALUES (?, ?)
            """, (customer_id, total))
            

            for item in st.session_state.cart:

                cursor.execute("""
                    UPDATE Medicines
                    SET Quantity = Quantity - ?
                    WHERE Med_ID = ?
                """, (item["qty"], item["med_id"]))


            sale_id = cursor.lastrowid

            for item in st.session_state.cart:
                cursor.execute("""
                    INSERT INTO Sale_Items (Sale_ID, Med_ID, Med_Name, Quantity, Price, Total)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    sale_id,
                    item["med_id"],
                    item["name"],
                    item["qty"],
                    item["price"],
                    item["qty"] * item["price"]
                ))

            st.session_state.cart = []
            st.success(f"✅ Sale completed! Total = {total}")

            
            conn.commit()
            st.rerun()

# DATABASE PAGE
elif page == "Database":

    st.subheader("🗂️ Database Tables")

    tab1, tab2, tab3, tab4 = st.tabs(
    ["💊 Medicines", "👥 Customers", "🧾 Sales", "📦 Sale Items"]
)

    with tab1:
        df = pd.read_sql_query("SELECT * FROM Medicines", conn)
        st.dataframe(df, width='stretch')

    with tab2:
        df = pd.read_sql_query("SELECT * FROM Customers", conn)
        st.dataframe(df, width='stretch')

    with tab3:
        df = pd.read_sql_query("SELECT * FROM Sales", conn)
        st.dataframe(df, width='stretch')
    with tab4:
        df = pd.read_sql_query("SELECT * FROM Sale_Items", conn)
        st.dataframe(df, width='stretch')

# Close
conn.close()
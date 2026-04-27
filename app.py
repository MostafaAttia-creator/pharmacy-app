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

    # 📦 STOCK SECTION (NEW)
    info1, info2 = st.columns(2)

    info1.info(f"💰 Price: {price}")

    info2.metric(
        label="📦 Stock Remaining",
        value=stock
    )

    # 🚨 Stock validation
    if stock <= 0:
        st.error("❌ Out of stock")
        st.stop()

    if stock <= 5:
        st.warning("⚠️ Low Stock!")

    # Quantity
    qty = st.number_input(
        "Enter Quantity",
        min_value=1,
        max_value=int(stock),
        step=1
    )

    # Cart
    if "cart" not in st.session_state:
        st.session_state.cart = []

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Add to Cart", use_container_width=True):
            st.session_state.cart.append({
                "med_id": int(med_id),
                "name": medicine,
                "qty": qty,
                "price": price,
                "total": qty * price
            })
            st.success("Added to cart")

    with col2:
        if st.button("🗑️ Clear Cart", use_container_width=True):
            st.session_state.cart = []
            st.warning("Cart cleared")

    # Show Cart
    st.subheader("🛒 Cart")

    if len(st.session_state.cart) == 0:
        st.info("Cart is empty")
    else:
        cart_df = pd.DataFrame(st.session_state.cart)
        st.dataframe(cart_df, use_container_width=True)

        total = cart_df["total"].sum()
        st.success(f"💰 Total = {total}")

    # Sell
    if st.button("🛒 Sell Now", use_container_width=True):

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
                INSERT INTO Sales (Customer_ID, Total_Amount)
                VALUES (?, ?)
            """, (customer_id, total))

            sale_id = cursor.lastrowid

            # Check stock before update
            for item in st.session_state.cart:
                cursor.execute("SELECT Quantity FROM Medicines WHERE Med_ID = ?", (item["med_id"],))
                current_stock = cursor.fetchone()[0]

                if current_stock < item["qty"]:
                    st.error(f"❌ Not enough stock for {item['name']}")
                    st.stop()

            # Update stock
            for item in st.session_state.cart:

                cursor.execute("""
                    UPDATE Medicines
                    SET Quantity = Quantity - ?
                    WHERE Med_ID = ? AND Quantity >= ?
                """, (item["qty"], item["med_id"], item["qty"]))

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

            conn.commit()
            st.session_state.cart = []

            st.success(f"✅ Sale completed! Total = {total}")
            st.rerun()

# DATABASE PAGE
elif page == "Database":

    st.subheader("🗂️ Database Tables")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["💊 Medicines", "👥 Customers", "🧾 Sales", "📦 Sale Items"]
    )

    with tab1:
        df = pd.read_sql_query("SELECT * FROM Medicines", conn)
        st.dataframe(df, use_container_width=True)

    with tab2:
        df = pd.read_sql_query("SELECT * FROM Customers", conn)
        st.dataframe(df, use_container_width=True)

    with tab3:
        df = pd.read_sql_query("SELECT * FROM Sales", conn)
        st.dataframe(df, use_container_width=True)

    with tab4:
        df = pd.read_sql_query("SELECT * FROM Sale_Items", conn)
        st.dataframe(df, use_container_width=True)

# Close
conn.close()
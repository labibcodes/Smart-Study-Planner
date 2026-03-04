import streamlit as st

st.title("📚 Smart Study Planner")

st.write("Welcome to your smart study planner app!")

# Input study plan
target = st.text_input("Nama Target Belajar")

jam = st.number_input("Total Jam Belajar", min_value=0.0)

deadline = st.date_input("Deadline")

if st.button("Tambah Target"):
    st.success(f"Target {target} disimpan!")
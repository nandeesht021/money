import streamlit as st
import json
import os

USER_FILE = "users.json"


def load_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


def register():
    st.subheader("📝 Register")

    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")

    if st.button("Register"):
        users = load_users()

        if any(u["username"] == username for u in users):
            st.error("User already exists ❌")
        else:
            users.append({"username": username, "password": password})
            save_users(users)
            st.success("Registered successfully ✅")


def login():
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()

        for user in users:
            if user["username"] == username and user["password"] == password:
                st.session_state["logged_in"] = True
                st.session_state["user"] = username
                st.success("Login successful ✅")
                st.rerun()

        st.error("Invalid credentials ❌")


def check_auth():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        option = st.radio("Select Option", ["Login", "Register"])

        if option == "Login":
            login()
        else:
            register()

        st.stop()

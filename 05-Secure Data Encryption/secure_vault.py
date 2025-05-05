import streamlit as st
import hashlib
import base64
import json
import os
from cryptography.fernet import Fernet

# ============== CONFIGURATION ==============
DATA_FILE = "data.json"
MASTER_PASSWORD = "admin@113"

# ============== INITIALIZATION ==============
# Initialize session state
for key, default in {
    "stored_data": {},
    "current_user": None,
    "authenticated": False,
    "failed_attempts": 0,
    "KEY": None,
    "cipher": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Load stored data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"users": {}}

# Save stored data
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.stored_data, f, indent=4)

# Load existing data at startup
st.session_state.stored_data = load_data()

# ============== SECURITY FUNCTIONS ==============
def generate_key():
    return Fernet.generate_key()

def get_cipher():
    if st.session_state.KEY is None:
        st.session_state.KEY = generate_key()
    if st.session_state.cipher is None:
        st.session_state.cipher = Fernet(st.session_state.KEY)
    return st.session_state.cipher

# PBKDF2 Passkey Hashing
def hash_passkey(passkey, salt=None):
    if salt is None:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', passkey.encode(), salt, 100000)
    return {
        "salt": base64.b64encode(salt).decode(),
        "key": base64.b64encode(key).decode()
    }

def verify_passkey(passkey, stored_hash):
    salt = base64.b64decode(stored_hash["salt"])
    true_key = base64.b64decode(stored_hash["key"])
    test_key = hashlib.pbkdf2_hmac('sha256', passkey.encode(), salt, 100000)
    return test_key == true_key

# Encrypt text
def encrypt_text(plain_text):
    cipher = get_cipher()
    return cipher.encrypt(plain_text.encode()).decode()

# Decrypt text
def decrypt_text(encrypted_text):
    cipher = get_cipher()
    return cipher.decrypt(encrypted_text.encode()).decode()

# ============== AUTHENTICATION SYSTEM ==============
def register_user(username, password):
    if username in st.session_state.stored_data["users"]:
        return False
    st.session_state.stored_data["users"][username] = {
        "password": hash_passkey(password),
        "data": {}
    }
    save_data()
    return True

def login_user(username, password):
    user = st.session_state.stored_data["users"].get(username)
    if not user:
        return False
    return verify_passkey(password, user["password"])

def reauthorize(master_pass):
    if master_pass == MASTER_PASSWORD:
        st.session_state.failed_attempts = 0
        st.session_state.authenticated = True
        return True
    return False

# ============== UI FUNCTIONS ==============

def show_home():
    st.title("🔐 Secure Vault")
    st.write("Welcome to your **personal encrypted storage system**.")
    st.success(f"Logged in as: {st.session_state.current_user}")

def show_register():
    st.title("📝 Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if username and password:
            if register_user(username, password):
                st.success("✅ Registration successful! Please log in.")
            else:
                st.error("⚠️ Username already exists.")
        else:
            st.warning("Please fill both fields.")

def show_login():
    st.title("🔑 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            if login_user(username, password):
                st.session_state.current_user = username
                st.session_state.authenticated = True
                st.success(f"✅ Welcome, {username}!")
            else:
                st.error("❌ Incorrect username or password.")
        else:
            st.warning("Please fill both fields.")

def show_store_data():
    st.title("📦 Store Data Securely")

    text_to_store = st.text_area("Enter text to encrypt")
    passkey = st.text_input("Set a passkey for this data", type="password")

    if st.button("Encrypt & Save"):
        if text_to_store and passkey:
            encrypted_text = encrypt_text(text_to_store)
            passkey_hash = hash_passkey(passkey)
            st.session_state.stored_data["users"][st.session_state.current_user]["data"][encrypted_text] = {
                "encrypted_text": encrypted_text,
                "passkey": passkey_hash
            }
            save_data()
            st.success("✅ Data encrypted and saved securely!")
            st.text_area("🔒 Your Encrypted Text:", encrypted_text, height=100)
        else:
            st.warning("Please fill all fields.")

def show_retrieve_data():
    st.title("🔍 Retrieve Your Data")

    if not st.session_state.authenticated:
        st.warning("🔒 Please reauthorize on the 'Login' page.")
        return

    encrypted_input = st.text_area("Paste your encrypted text")
    passkey = st.text_input("Enter your passkey", type="password")

    if st.button("Decrypt"):
        if encrypted_input and passkey:
            user_data = st.session_state.stored_data["users"][st.session_state.current_user]["data"]
            record = user_data.get(encrypted_input)

            if record and verify_passkey(passkey, record["passkey"]):
                decrypted = decrypt_text(encrypted_input)
                st.success("✅ Decryption successful!")
                st.code(decrypted)
                st.session_state.failed_attempts = 0
            else:
                st.session_state.failed_attempts += 1
                attempts_left = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect passkey. Attempts remaining: {attempts_left}")

                if st.session_state.failed_attempts >= 3:
                    st.session_state.authenticated = False
                    st.warning("🔒 Too many failed attempts. Please reauthorize.")
        else:
            st.warning("Please fill all fields.")

def show_master_login():
    st.title("🔑 Reauthorize")

    master_pass = st.text_input("Enter Master Password", type="password")

    if st.button("Reauthorize"):
        if reauthorize(master_pass):
            st.success("✅ Reauthorized successfully!")
        else:
            st.error("❌ Incorrect master password.")

# ============== MAIN PAGE LOGIC ==============

def main():
    st.sidebar.title("Navigation")
    if st.session_state.current_user:
        menu = ["Home", "Store Data", "Retrieve Data", "Logout"]
    else:
        menu = ["Login", "Register"]

    choice = st.sidebar.radio("Go to:", menu)

    if choice == "Home":
        show_home()
    elif choice == "Register":
        show_register()
    elif choice == "Login":
        show_login()
    elif choice == "Store Data":
        show_store_data()
    elif choice == "Retrieve Data":
        show_retrieve_data()
    elif choice == "Logout":
        st.session_state.current_user = None
        st.session_state.authenticated = False
        st.success("👋 Logged out successfully.")

    if not st.session_state.authenticated and st.session_state.current_user:
        st.sidebar.markdown("---")
        st.sidebar.title("Reauthorization")
        show_master_login()

# Run App
if __name__ == "__main__":
    main()

import streamlit as st
import re
import random

# Common weak passwords
blacklist = ['password', '123456', 'password123', 'admin', 'qwerty', 'abc123']

def check_password_strength(password):
    score = 0
    suggestions = []

    if password.lower() in blacklist:
        return 0, ["❌ Avoid using common passwords like 'password123' or 'admin'."]

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("🔸 Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("🔸 Include both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("🔸 Add at least one number (0-9).")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        suggestions.append("🔸 Include at least one special character (!@#$%^&*).")

    return score, suggestions

def generate_strong_password(length=12):
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower = "abcdefghijklmnopqrstuvwxyz"
    digits = "0123456789"
    special = "!@#$%^&*"
    all_chars = upper + lower + digits + special

    # Ensure at least one from each category
    password = random.choice(upper) + random.choice(lower) + random.choice(digits) + random.choice(special)
    password += ''.join(random.choice(all_chars) for _ in range(length - 4))
    return ''.join(random.sample(password, len(password)))

# Streamlit App UI
st.set_page_config(page_title="🔐 Password Strength Meter", layout="centered")
st.title("🔐 Password Strength Meter")

st.markdown("Check if your password is **secure enough** or get a **strong one suggested**! 💪")

password = st.text_input("Enter your password", type="password")
confirm_password = st.text_input("Confirm your password", type="password")

if password and confirm_password:
    if password != confirm_password:
        st.error("❌ Passwords do not match.")
    else:
        score, feedback = check_password_strength(password)
        st.subheader(f"🧪 Strength Score: {score}/4")

        if score == 4:
            st.success("✅ Excellent! Your password is strong.")
        elif score == 3:
            st.warning("⚠️ Moderate - consider improving:")
            for tip in feedback:
                st.info(tip)
        else:
            st.error("❌ Weak Password - please improve:")
            for tip in feedback:
                st.info(tip)

if st.button("🔁 Generate Strong Password"):
    strong_pass = generate_strong_password()
    st.success(f"✅ Suggested Password: `{strong_pass}`")

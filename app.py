import streamlit as st
import pandas as pd
import joblib
import pyttsx3
import os

# Load model and encoders
model = joblib.load("rf_model.pkl")
scaler = joblib.load("scaler.pkl")
le_tt = joblib.load("le_tt.pkl")
le_du = joblib.load("le_du.pkl")
le_loc = joblib.load("le_loc.pkl")
le_pm = joblib.load("le_pm.pkl")

# Speaker function
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 130)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
    except:
        st.warning("🔈 Speaker not supported.")

# Apply background style
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

USER = "admin"
PASS = "1234"

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 130)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
    except:
        st.warning("🔈 Speaker not supported on this device.")

def login():
    st.title("🔐 Fraud Detection Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.button("Login"):
        if username.strip() == USER and password.strip() == PASS:
            st.session_state.logged_in = True
            st.success("✅ Login successful!")  # UI Message
            speak("Login successful.")         # 🎤 Speaker speaks here
        else:
            st.error("❌ Invalid username or password")


# Prediction Page
def fraud_detector():
    #st.title("🛡️ Online Payment Fraud Detection")
    st.markdown("<h1 style='color:#FFD700;'>🛡️ Online Payment Fraud Detection</h1>", unsafe_allow_html=True)


    amount = st.number_input("Transaction Amount", min_value=1.0)
    t_type = st.selectbox("Transaction Type", le_tt.classes_)

    st.markdown(
    "<span style='color:#FFD700;'>ℹ 0 = ATM Withdrawal, 1 = POS Payment, 2 = Online Transfer, 3 = Bill Payment, 4 = Others</span>",
    unsafe_allow_html=True
)


    time = st.slider("Time of Transaction", 0.0, 23.99, step=0.25)
    device = st.selectbox("Device Used", le_du.classes_)
    st.markdown(
    "<span style='color:#FFD700;'>ℹ 0 = Mobile, 1 = Tablet, 2 = Desktop</span>",
    unsafe_allow_html=True
)


    location = st.selectbox("Location", le_loc.classes_)
    st.markdown(
    "<span style='color:#FFD700;'>ℹ 0 = San Francisco, 1 = New York, 2 = Boston, 3 = Chicago, 4 = Los Angeles, 5 = Seattle, 6 = Houston</span>",
    unsafe_allow_html=True
)

    prev = st.slider("Previous Fraudulent Transactions", 0, 10)
    age = st.slider("Account Age (months)", 1, 120)
    txn_24h = st.slider("Transactions in last 24h", 1, 20)
    payment = st.selectbox("Payment Method", le_pm.classes_)
    st.markdown(
    "<span style='color:#FFD700;'>ℹ 0 = Credit Card, 1 = Debit Card, 2 = Net Banking, 3 = Cash, 4 = UPI</span>",
    unsafe_allow_html=True
)

  


    

    if st.button("Predict Fraud"):
        input_data = {
            'Transaction_Amount': amount,
            'Transaction_Type': le_tt.transform([t_type])[0],
            'Time_of_Transaction': time,
            'Device_Used': le_du.transform([device])[0],
            'Location': le_loc.transform([location])[0],
            'Previous_Fraudulent_Transactions': prev,
            'Account_Age': age,
            'Number_of_Transactions_Last_24H': txn_24h,
            'Payment_Method': le_pm.transform([payment])[0]
        }






        input_df = pd.DataFrame([input_data])
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0]

        if prediction == 1:
            st.error("🚨 Transaction is Fraud!")
            st.markdown("🔴 **System Alert**: This transaction has been flagged based on risk pattern analysis.")
            st.markdown("""
        <script>alert("⚠️ Fraud Alert! Immediate action needed.");</script>
        """, unsafe_allow_html=True)
            speak("This transaction is predicted to be fraud.")
        else:
            st.success("✅ Transaction is Safe transaction.")
            st.markdown("🟢 **No anomaly found** in transaction pattern.")
            speak("This transaction is predicted to be safe transaction.")







        st.markdown("---")
    st.markdown("""
    <div style='background-color: black; color: white; padding: 20px; border-radius: 10px;'>
        <h3>🧾 Transaction Summary (What User Filled)</h3>
        <ul>
            <li><b>Transaction Amount:</b> ₹{amount}</li>
            <li><b>Transaction Type:</b> {t_type}</li>
            <li><b>Time of Transaction:</b> {time} hrs</li>
            <li><b>Device Used:</b> {device}</li>
            <li><b>Location:</b> {location}</li>
            <li><b>Previous Fraudulent Transactions:</b> {prev}</li>
            <li><b>Account Age:</b> {age} months</li>
            <li><b>Transactions in Last 24 Hours:</b> {txn_24h}</li>
            <li><b>Payment Method:</b> {payment}</li>
        </ul>
    </div>
    """.format(amount=amount, t_type=t_type, time=time, device=device, location=location, prev=prev, age=age, txn_24h=txn_24h, payment=payment),
    unsafe_allow_html=True)

    # 👇 Verdict line (show after prediction)
    if 'prediction' in locals() or 'prediction' in globals():
        if prediction == 1:
            st.markdown("""
            <div style='background-color:#8B0000; color:white; padding:10px; margin-top:10px; border-radius:10px; text-align:center;'>
                🚨 <strong>Final Decisions:</strong> This Transaction is <u>Fraudulent</u>.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background-color:#006400; color:white; padding:10px; margin-top:10px; border-radius:10px; text-align:center;'>
                ✅ <strong>Final Decision:</strong> This Transaction is <u>Safe</u>.
            </div>
            """, unsafe_allow_html=True)




# Control Login Session
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    fraud_detector()
else:
    login()



# Add robot image (you can use your own image too)
st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=150, use_column_width=False)



st.markdown(
    "<h4 style='text-align: center;'>🤖 Your AI Assistant is here for your help !</h4>",
    unsafe_allow_html=True
)


st.markdown("""
    <style>
    .stApp h1 {
        color: #FF9933;  /* Bright blue color for Fraud Transaction Prediction */
    }
    </style>
    """, unsafe_allow_html=True)


st.markdown("""
    <style>
    .stApp {
        background-color: #008080;  /* Teal */
    }
    </style>
    """, unsafe_allow_html=True)







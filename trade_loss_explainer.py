import streamlit as st
import requests

st.title("💹 Trade Loss Explainer AI")

st.markdown("Enter your trade details and get AI-powered insights on what may have gone wrong.")

# Inputs
trade_type = st.selectbox("📈 Trade Type", ["Buy", "Sell"])
entry_price = st.number_input("💰 Entry Price")
exit_price = st.number_input("💸 Exit Price")
stop_loss = st.number_input("🛑 Stop Loss (optional)", value=0.0)
take_profit = st.number_input("🎯 Take Profit (optional)", value=0.0)
market = st.text_input("💱 Market (e.g., BTC/USDT, AAPL)")
datetime = st.text_input("🕐 Entry/Exit Time (optional)", placeholder="e.g., 2025-05-30 09:15")

# Prompt generator
def create_prompt():
    return f"""
    I'm an AI trading analyst. A user made a {trade_type} trade in {market}.
    - Entry Price: {entry_price}
    - Exit Price: {exit_price}
    - Stop Loss: {stop_loss}
    - Take Profit: {take_profit}
    - Trade Time: {datetime}
    
    Please explain in simple terms why this trade might have failed.
    """

# Send to Ollama
def ask_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt},
            stream=True
        )
        full_response = ""
        for chunk in response.iter_lines():
            if chunk:
                line = chunk.decode('utf-8')
                # each line might be a JSON, extract the 'response' field
                import json
                data = json.loads(line)
                if 'response' in data:
                    full_response += data['response']
        return full_response
    except Exception as e:
        return f"Error: {e}"

# Button
if st.button("📊 Explain Trade Loss"):
    prompt = create_prompt()
    with st.spinner("🧠 Analyzing trade..."):
        result = ask_ollama(prompt)
    st.markdown("### 🧠 AI Explanation")
    st.write(result)


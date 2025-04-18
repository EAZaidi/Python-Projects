import streamlit as st


st.title("🌎 Unit Converter App")
st.markdown("### Converts Length, Weight & Time")
st.write("Welcome! Select a category, enter a value & get the converted value instantly")

category = st.selectbox("Select a Category", ["Length", "Weight", "Time", "Temperature"])

def convert_units(category, value, unit):
    if category == "Length":
        if unit == "Kilometers to Miles":
            return value * 0.621371
        elif unit == "Miles to Kilometers":
            return value / 0.621371
    
    elif category == "Weight":
        if unit == "Kilograms to Pounds":
            return value * 2.20462
        elif unit == "Pounds to Kilograms":
            return value / 2.20462
        elif unit == "Kilograms to Grams":
            return value * 1000
        elif unit == "Grams to Kilograms":
            return value / 1000
        elif unit == "Pounds to Grams":
            return value * 453.592
        elif unit == "Grams to Pounds":
            return value / 453.592
    
    elif category == "Time":
        if unit == "Seconds to Minutes":
            return value / 60
        elif unit == "Minutes to Seconds":
            return value * 60
        elif unit == "Minutes to Hours":
            return value / 60
        elif unit == "Hours to Minutes":
            return value * 60
        elif unit == "Hours to Days":
            return value / 24
        elif unit == "Days to Hours":
            return value * 24
        
    elif category == "Temperature":
        if unit == "Celsius to Fahrenheit":
            return value * (9/5) + 32
        elif unit == "Fahrenheit to Celsius":
            return (value - 32) * (5/9)
        
if category == "Length":
    unit = st.selectbox("Select a Conversion", ["Kilometers to Miles", "Miles to Kilometers"])
elif category == "Weight":
    unit = st.selectbox("Select a Conversion", ["Kilograms to Pounds", "Pounds to Kilograms", "Kilograms to Grams", "Grams to Kilograms", "Pounds to Grams", "Grams to Pounds"])
elif category == "Time":
    unit = st.selectbox("Select a Conversion", ["Seconds to Minutes", "Minutes to Seconds",
                                               "Minutes to Hours", "Hours to Minutes",
                                               "Hours to Days", "Days to Hours"])
elif category == "Temperature":
    unit = st.selectbox("Select a Conversion", ["Celsius to Fahrenheit", "Fahrenheit to Celsius"])

value = st.number_input("Enter a value to convert")

if st.button("Convert"):
    result = convert_units(category, value, unit)
    st.success(f"The result is: {result:.3f}")

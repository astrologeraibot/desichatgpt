import streamlit as st
import requests
import datetime

# Zodiac sign logic
def get_zodiac_sign(month, day):
    zodiac = [
        ("Capricorn", (12, 22), (1, 19)),
        ("Aquarius", (1, 20), (2, 18)),
        ("Pisces", (2, 19), (3, 20)),
        ("Aries", (3, 21), (4, 19)),
        ("Taurus", (4, 20), (5, 20)),
        ("Gemini", (5, 21), (6, 20)),
        ("Cancer", (6, 21), (7, 22)),
        ("Leo", (7, 23), (8, 22)),
        ("Virgo", (8, 23), (9, 22)),
        ("Libra", (9, 23), (10, 22)),
        ("Scorpio", (10, 23), (11, 21)),
        ("Sagittarius", (11, 22), (12, 21)),
    ]
    for sign, start, end in zodiac:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            return sign
    return "Capricorn"

# Horoscope API
def get_horoscope(sign):
    sign = sign.lower()
    url = f"https://ohmanda.com/api/horoscope/{sign}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["horoscope"]
        else:
            return f"⚠️ API Error: {response.status_code}"
    except Exception as e:
        return f"⚠️ API Exception: {str(e)}"

# UI
st.set_page_config(page_title="Astrologer Bot", page_icon="🔮")
st.title("🔮 Astrologer Bot")

name = st.text_input("Enter your name")

birth_date = st.date_input(
    "Select your birth date",
    value=datetime.date(2000, 1, 1),
    min_value=datetime.date(1900, 1, 1),
    max_value=datetime.date.today()
)

# ✅ Collect time of birth
birth_time = st.time_input("Enter your time of birth (approximate if unsure)", value=datetime.time(12, 0))

# ✅ Collect place of birth
birth_place = st.text_input("Enter your place of birth (City, Country)")

if st.button("Get My Horoscope"):
    sign = get_zodiac_sign(birth_date.month, birth_date.day)
    birth_time = st.time_input("Enter your time of birth...")
    birth_place = st.text_input("Enter your place of birth...")
    horoscope = get_horoscope(sign)
    st.subheader(f"Hello {name}!")
    st.write(f"🌟 Your Zodiac Sign is **{sign}**")
    st.write("🪐 Today's Horoscope:")
    st.info(horoscope)


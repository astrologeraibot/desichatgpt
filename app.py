st.write("🚀 Astrologer Chat v2.0")

import streamlit as st
import datetime
import requests

# Prediction data
predictions = {
    "love": {
        "Aries": "Expect passion and surprises.",
        "Taurus": "Stability in love is coming.",
        "Gemini": "Exciting conversations ahead.",
        "Cancer": "Emotional bonding deepens.",
        "Leo": "Romantic spotlight shines on you.",
        "Virgo": "Details matter—show you care.",
        "Libra": "Balance in love returns.",
        "Scorpio": "Deep emotional connections await.",
        "Sagittarius": "Adventure brings love.",
        "Capricorn": "Solid relationships get stronger.",
        "Aquarius": "Love takes an unconventional turn.",
        "Pisces": "Dreamy and soulful moments ahead."
    },
    "money": {k: f"Financial outlook for {k} looks steady." for k in range(12)},
    "career": {k: f"Career growth opportunities open for {k}." for k in range(12)}
}

# Zodiac logic
def get_zodiac_sign(month, day):
    zodiac = [
        ("Capricorn", (12, 22), (1, 19)), ("Aquarius", (1, 20), (2, 18)),
        ("Pisces", (2, 19), (3, 20)), ("Aries", (3, 21), (4, 19)),
        ("Taurus", (4, 20), (5, 20)), ("Gemini", (5, 21), (6, 20)),
        ("Cancer", (6, 21), (7, 22)), ("Leo", (7, 23), (8, 22)),
        ("Virgo", (8, 23), (9, 22)), ("Libra", (9, 23), (10, 22)),
        ("Scorpio", (10, 23), (11, 21)), ("Sagittarius", (11, 22), (12, 21)),
    ]
    for sign, start, end in zodiac:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            return sign
    return "Capricorn"

def estimate_moon_sign(day):
    moon_signs = list(predictions["love"].keys())
    return moon_signs[day % 12]

def estimate_rising_sign(hour):
    rising_signs = list(predictions["love"].keys())
    return rising_signs[hour % 12]

def get_horoscope(sign):
    try:
        r = requests.get(f"https://ohmanda.com/api/horoscope/{sign.lower()}/")
        return r.json()["horoscope"] if r.status_code == 200 else "Unable to fetch horoscope."
    except:
        return "Error connecting to horoscope API."

# State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_info" not in st.session_state:
    st.session_state.user_info = {"name": None, "dob": None, "time": None, "place": None}

# Chat header
st.title("🔮 Astrologer Assistant Chat")

# Chat area
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# Input field
user_input = st.chat_input("Ask me about your stars...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # System response
    with st.chat_message("assistant"):
        response = ""

        if user_input.lower() == "/start":
            response = "👋 Hi! I'm your astrologer bot. Please tell me:\n\n`My name is John`, `I was born on 21 July 1995 at 9:00 AM in Delhi`"
        
        # Capture user info
        elif "name is" in user_input.lower():
            name = user_input.split("name is")[-1].strip().split()[0]
            st.session_state.user_info["name"] = name
            response = f"Hi {name}, nice to meet you! Now tell me your date, time and place of birth."

        elif "born on" in user_input.lower():
            try:
                import re
                match = re.search(r"born on (\d{1,2}) (\w+) (\d{4}) at (\d{1,2}):(\d{2}) ?([APMapm]{2}) in (.+)", user_input)
                if match:
                    day, month_name, year, hour, minute, ampm, place = match.groups()
                    birth_date = datetime.datetime.strptime(f"{day} {month_name} {year}", "%d %B %Y").date()
                    hour = int(hour) % 12 + (12 if ampm.lower() == "pm" else 0)
                    birth_time = datetime.time(hour, int(minute))
                    st.session_state.user_info["dob"] = birth_date
                    st.session_state.user_info["time"] = birth_time
                    st.session_state.user_info["place"] = place
                    response = f"Thanks! I've got your birth details. Ask me your horoscope, sun sign, or love prediction!"
                else:
                    response = "Please use this format: `I was born on 21 July 1995 at 9:00 AM in Delhi`"
            except:
                response = "Couldn't read your birth details. Try again."

        # Provide readings
        elif "sun sign" in user_input.lower():
            dob = st.session_state.user_info["dob"]
            if dob:
                sun = get_zodiac_sign(dob.month, dob.day)
                response = f"☀️ Your Sun Sign is **{sun}**."
            else:
                response = "Please provide your birth date first."

        elif "moon sign" in user_input.lower():
            dob = st.session_state.user_info["dob"]
            if dob:
                moon = estimate_moon_sign(dob.day)
                response = f"🌙 Your Moon Sign is **{moon}** (estimated)."
            else:
                response = "Please provide your birth date first."

        elif "rising" in user_input.lower():
            t = st.session_state.user_info["time"]
            if t:
                rising = estimate_rising_sign(t.hour)
                response = f"⬆️ Your Rising Sign is **{rising}** (estimated)."
            else:
                response = "Please provide your birth time first."

        elif "horoscope" in user_input.lower():
            dob = st.session_state.user_info["dob"]
            if dob:
                sign = get_zodiac_sign(dob.month, dob.day)
                response = f"🪐 Today's horoscope for **{sign}**:\n\n{get_horoscope(sign)}"
            else:
                response = "Please provide your birth date first."

        elif "love" in user_input.lower():
            dob = st.session_state.user_info["dob"]
            if dob:
                sign = get_zodiac_sign(dob.month, dob.day)
                response = f"💖 Love Prediction: {predictions['love'][sign]}"
            else:
                response = "Please provide your birth date first."

        elif "career" in user_input.lower():
            dob = st.session_state.user_info["dob"]
            if dob:
                sign = get_zodiac_sign(dob.month, dob.day)
                response = f"🎯 Career Prediction: {predictions['career'][sign]}"
            else:
                response = "Please provide your birth date first."

        elif "finance" in user_input.lower() or "money" in user_input.lower():
            dob = st.session_state.user_info["dob"]
            if dob:
                sign = get_zodiac_sign(dob.month, dob.day)
                response = f"💰 Finance Prediction: {predictions['money'][sign]}"
            else:
                response = "Please provide your birth date first."

        else:
            response = "I'm not sure what you mean. Ask me your horoscope, sun sign, love prediction, etc."

        st.session_state.chat_history.append(("assistant", response))
        st.markdown(response)

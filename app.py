elif any(word in user_input.lower() for word in ["born", "birth", "dob"]):
    try:
        import re
        from dateutil import parser

        # Flexible pattern to extract birth details
        match = re.search(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\w+ \d{1,2},? \d{4}|\d{4}-\d{2}-\d{2})[ ,]*at[ ,]*(\d{1,2}):?(\d{0,2}) ?([apAP]?[mM]?)?[ ,]*in (.+)", user_input)

        if match:
            date_str, hour, minute, ampm, place = match.groups()
            hour = int(hour)
            minute = int(minute) if minute else 0
            if ampm.lower().startswith("p") and hour < 12:
                hour += 12
            elif ampm.lower().startswith("a") and hour == 12:
                hour = 0

            birth_date = parser.parse(date_str, fuzzy=True).date()
            birth_time = datetime.time(hour, minute)

            st.session_state.user_info["dob"] = birth_date
            st.session_state.user_info["time"] = birth_time
            st.session_state.user_info["place"] = place.strip()

            response = f"✅ Birth details recorded:\n\n📅 {birth_date}, 🕒 {birth_time}, 📍 {place.strip()}\n\nAsk me for your horoscope, sun sign, or love prediction!"
        else:
            response = "❌ I couldn't read your full birth details. Try: `I was born on 21 July 1995 at 9:00 AM in Delhi`"
    except Exception as e:
        response = f"⚠️ Error parsing birth info: {e}"

import requests
import streamlit as st

st.set_page_config(page_title="חוקר הסדרות", page_icon="🔎")
url = "https://api.themoviedb.org/3/search/tv"
st.title("**חוקר הסדרות** 🔎")
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    .stTextInput input {
        direction: rtl;
        text-align: right;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        direction: rtl;
        text-align: right;
    }
    div[data-testid="InputInstructions"] {
        display: none !important;
    }
    .stAppDeployButton {
        display: none !important;
    }
    #MainMenu {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }
    .stHeaderActionElements {
        display: none !important;
    }
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Heebo', sans-serif !important;
    }
    * {
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)
show = st.text_input("הכנס שם סדרה באנגלית: ")

if st.button("✨ **חקור סדרה** ✨"):
    if show != "":
        auth_envelope = {"Authorization": f"Bearer {st.secrets["TMDB_API_KEY"]}"}
        params = {"query": show}
        response = requests.get(url, headers=auth_envelope, params=params).json()

        try:
            show_id = response["results"][0]["id"]
            show_name = response["results"][0]["name"]

            show_url = f"https://api.themoviedb.org/3/tv/{show_id}"

            response_analysis = requests.get(show_url, headers=auth_envelope).json()

            seasons = response_analysis["number_of_seasons"]
            episodes = response_analysis["number_of_episodes"]
            status = response_analysis["status"]

            poster_path = response_analysis.get("poster_path")

            if status == "Ended":
                status = "נגמר"
            if status == "Canceled":
                status = "בוטל"
            if status == "Returning Series":
                status = "באוויר"
            if status == "In Production":
                status = "בצילומים"
            if status == "Planned":
                status = "מתוכנן"
            if status == "Pilot":
                status = "פילוט"

            col1, col2 = st.columns([1, 2])

            with col1:
                if poster_path:
                    st.image(f"https://image.tmdb.org/t/p/w500{poster_path}", use_container_width=True)

            all_episodes = []
            total_minutes = 0
            series_score = 0
            current_season = 0
            with st.spinner(f"חוקר את הסדרה: {show_name}"):  # type: ignore
                while current_season < seasons:
                    current_season += 1
                    season_url = f"https://api.themoviedb.org/3/tv/{show_id}/season/{current_season}"
                    response_season = requests.get(season_url, headers=auth_envelope)
                    response_season = response_season.json()

                    current_episode = 0
                    season_episodes = len(response_season["episodes"])
                    while current_episode < season_episodes:
                        episode_name = response_season["episodes"][current_episode]["name"]
                        episode_rating = response_season["episodes"][current_episode]["vote_average"]
                        if episode_rating > 0:
                            all_episodes.append(
                                {"name": episode_name, "score": episode_rating, "episode": current_episode + 1,
                                 "season": current_season})
                        episode_time = response_season["episodes"][current_episode]["runtime"]
                        if type(episode_time) == int:
                            total_minutes += episode_time
                        series_score += episode_rating
                        current_episode += 1
                if len(all_episodes) > 0:
                    marathons = total_minutes / 270
                    flights = total_minutes / 1320
                    soccer = total_minutes / 90

                    with col2:
                        st.subheader(f"נתוני סדרה: {show_name}")
                        st.write(f"**עונות:** {seasons} | **פרקים:** {episodes} | **סטטוס:** {status}")

                        total_hours = total_minutes // 60
                        total_minutes = total_minutes % 60
                        total_days = total_hours // 24
                        total_hours = total_hours % 24

                        st.metric(label="אורך הבינג':",
                                  value=f"{total_days} ימים, {total_hours} שעות, {total_minutes} דקות ")
                        st.warning(
                            f"בזמן הזה יכולת לרוץ {round(marathons)} מרתונים 🏃️\n\n בזמן הזה יכולת לטוס {round(flights)} פעמים הלוך חזור לניו יורק ✈️ \n\n בזמן הזה יכולת לראות {round(soccer)} משחקי כדורגל ⚽")
                        # st.write(f" ")
                        # st.write(f"")

                    i = 1
                    max_drop = 0
                    worst_episode = ""
                    while i < len(all_episodes):
                        current_episode_rating = all_episodes[i]["score"]
                        last_episode_rating = all_episodes[i - 1]["score"]
                        drop = last_episode_rating - current_episode_rating
                        if drop > max_drop:
                            max_drop = drop
                            worst_episode = all_episodes[i]["name"]
                        i += 1
                    with st.expander("לחץ לפתיחת הפרק הכי גרוע ⬇️"):
                        st.metric(label="הפרק הגרוע ביותר", value=f"{worst_episode}",
                                  delta=f"{-round(max_drop, 3)} נקודות")

                    t = 0
                    turning_point_detect = False
                    while t < len(all_episodes) - 2:
                        if all_episodes[t]["score"] >= 8:
                            if all_episodes[t + 1]["score"] >= 8:
                                if all_episodes[t + 2]["score"] >= 8:
                                    if all_episodes[t]["season"] == 1 and all_episodes[t]["episode"] <= 5:
                                        with st.expander("לחץ לפתיחת נקודת המפנה של הסדרה ⬇️"):
                                            st.balloons()
                                            st.metric(label="סטטוס התמכרות 💣", value="מאסטרפיס!",delta="הסדרה מטורפת כבר מההתחלה")
                                        turning_point_detect = True
                                        break
                                    else:
                                        with st.expander("לחץ לפתיחת נקודת המפנה של הסדרה ⬇️"):
                                            st.metric(label="נקודת מפנה אותרה 🎯",value=f"עונה {all_episodes[t]['season']} | פרק {all_episodes[t]['episode']}",delta=f"שם הפרק: {all_episodes[t]['name']}")
                                            turning_point_detect = True
                                            break
                        t += 1

                    all_episodes.sort(key=lambda x: x["score"], reverse=True)
                    with st.expander("לחץ לפתיחת עשרת הפרקים הכי טובים ⬇️"):
                        k = 0
                        st.subheader("טופ 10 פרקים 🏆: ")
                        if 10 > len(all_episodes):
                            for k in range(len(all_episodes)):
                                st.write(
                                    f"‎ ‎ {k + 1}. עונה {all_episodes[k]["season"]} פרק {all_episodes[k]["episode"]} - {all_episodes[k]["name"]}, ציון: {all_episodes[k]["score"]}")
                                k += 1
                        if len(all_episodes) >= 10:
                            for k in range(10):
                                st.write(
                                    f"‎ ‎ {k + 1}. עונה {all_episodes[k]["season"]} פרק {all_episodes[k]["episode"]} - {all_episodes[k]["name"]}, ציון: {all_episodes[k]["score"]}")
                                k += 1
        except:
            st.write("הסדרה שחיפשת לא נמצאה")
    if show == "":
        st.error("בבקשה תכניס שם של סדרה")

st.markdown("---")
st.caption("This product uses the TMDB API but is not endorsed or certified by TMDB.")
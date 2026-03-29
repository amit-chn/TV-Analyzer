# TV ANALYZER 🔎

An advanced, data-driven TV show analysis tool built with Python and Streamlit. This application leverages the TMDB API to provide objective insights into television series, helping users identify high-quality content and manage their viewing time.

## 🚀 Key Features

* **The Hook Point Detector:** An algorithm that scans episode ratings to identify the exact moment a series becomes "addictive" (defined by a streak of 3+ episodes rated 8.0 or higher).
* **Binge-Time Index:** Calculates the total runtime of the entire series and converts it into real-world metrics (Marathons, Flights, Football matches).
* **Worst Episode:** Automatically detects the largest "score drop" between consecutive episodes and highlights the series' lowest point.
* **Top 10:** A dynamically sorted list of the highest-rated episodes across all seasons.
* **Interface:** A sleek, RTL-supported dark mode UI with neon accents, optimized for Hebrew-speaking users.

## 🛠️ Tech Stack

* **Frontend/Hosting:** [Streamlit](https://streamlit.io/)
* **Language:** Python 3.x
* **Data Source:** [TMDB API](https://www.themoviedb.org/documentation/api)
* **Styling:** Custom CSS Injection (RTL & Component Hiding)

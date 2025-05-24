# BoToKoTo BTKT

A simple data viewer for the 2025 Midterm Election data for Partylist and Senators, built with Streamlit. This app allows users to visualize, explore, and analyze election results from an SQLite database, with interactive charts and location-based lookups.

## Features

- **Senatorial and Partylist Rankings:** Interactive bar charts showing top candidates.
- **Vote Lookup:** Search and display total votes for any candidate, with breakdowns by region, province, city/municipality, and barangay.
- **Location-based Summaries:** Visualize votes by region, province, city/municipality, or barangay.
- **Custom SQL Query Tool:** Run custom SQL queries on the election database.
- **Modern UI:** Responsive, themed interface using Streamlit and Plotly.

## Project Structure

```
.
├── main.py                # Main Streamlit app
├── widgets.py             # Visualization and UI widgets
├── database.py            # SQLite3 database logic
├── test.py                # SQL query tool for advanced users
├── election_data.db       # SQLite database file
├── requirements.txt       # Python dependencies
├── btkt.png               # Logo/image asset
├── templates/             # HTML templates for vote display
│   ├── showvotes.html
│   ├── showvotes_brgy.html
│   └── showvotes_city.html
└── .streamlit/
    └── config.toml        # Streamlit theme configuration
```

## Getting Started

### Prerequisites

- Python 3.10+
- [pip](https://pip.pypa.io/en/stable/)

### Installation

1. **Clone the repository:**
    ```sh
    git clone <repo-url>
    cd botoKo
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Prepare the database:**
    - Ensure `election_data.db` is present in the root directory.
    - If you need to upload new datasets, use the upload tool in `database.py`.

4. **Run the app:**
    ```sh
    streamlit run main.py
    ```

5. **(Optional) Advanced SQL Query Tool:**
    ```sh
    streamlit run test.py
    ```

## Usage

- Use the sidebar and forms to select candidates, tables, and locations.
- Visualizations update interactively based on your selections.
- For advanced users, use the "Advanced" expander in `test.py` to run custom SQL queries.

## Customization

- **Theme:** Modify `.streamlit/config.toml` for color and font changes.
- **Templates:** Edit HTML files in `templates/` for custom vote display cards.

## License

MIT License

---

*Developed for the 2025 Philippine Midterm Election Data Analysis.*
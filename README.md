# 📈 Real-Time Financial Market Dashboard

![image](https://github.com/user-attachments/assets/bb54a071-f46e-40f6-a7d0-408ef17c2f85)

 
*Replace with actual screenshot after deployment*

A powerful real-time financial analytics dashboard that demonstrates end-to-end data processing from ingestion to visualization using Python, Streamlit, and Yahoo Finance API.

## 🚀 Features

- **Real-time market data** from Yahoo Finance API
- **Interactive visualizations** with Plotly and Streamlit
- **Technical indicators**:
  - Moving Averages (SMA 20, 50, 200)
  - Relative Strength Index (RSI)
  - Bollinger Bands
  - Historical Volatility
- **Correlation analysis** between multiple assets
- **SQL database integration** for historical data storage
- **Responsive design** works on desktop and mobile

## 🛠️ Tech Stack

- **Python** (Pandas, NumPy)
- **Streamlit** (Web framework)
- **yfinance** (Yahoo Finance API)
- **SQLite** (Database)
- **Plotly** (Interactive visualizations)
- **Git** (Version control)

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/NikitaKundle01/Financial-Market-Dashboard.git
cd Financial-Market-Dashboard
```

2.Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

🏃 Running the Application
Start the Streamlit dashboard:
```bash
streamlit run main.py
```
The dashboard will open in your default browser at http://localhost:8501

### 📂 Project Structure

```bash
financial-dashboard/
├── data/                   # Data storage
│   ├── historical/         # Historical price data
│   └── database/           # SQLite database files
├── src/
│   ├── config/             # Configuration files
│   ├── data/               # Data collection and processing
│   ├── analytics/          # Financial analytics modules
│   └── visualization/      # Visualization components
├── tests/                  # Unit tests
├── requirements.txt        # Python dependencies
├── main.py                 # Main entry point
└── README.md               # Project documentation
```

## 📊 How to Use
Enter ticker symbols (comma separated) in the sidebar

Select a time frame (1 day to 5 years)

Choose which technical indicators to display

Explore different tabs:

Price Charts: Interactive candlestick charts

Technical Indicators: RSI, Volatility, Bollinger Bands

Correlation Analysis: Heatmap of asset correlations

## 🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some amazing feature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

## 📧 Contact
Nikita Kundle -  - kundlenikita@gmail.com

Project Link: https://github.com/NikitaKundle01/Financial-Market-Dashboard


### Additional notes:

1. Replace the placeholder screenshot with an actual screenshot after you deploy your dashboard
2. Update the contact information with your details
3. Add a LICENSE file if you want to use a different license
4. You may want to add a "Roadmap" or "Future Features" section if you plan to expand the project
5. For a more professional look, consider adding badges from shields.io for:
   - Build status
   - Python version
   - License
   - Downloads

To add badges, you can include lines like this at the top of your README:
```markdown
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-1.22.0-orange)]()

# Company Health Dashboard

**A simple web app to visualise UK company financial health in seconds.**

Enter any UK company number and instantly see their assets, liabilities, debt ratios, and key business information - all pulled from official Companies House data via the DataLedger API.

![Dashboard Preview](screenshot.png) *(Add a screenshot of your dashboard here)*

## What it does

- **Company Overview**: Name, location, employee count, and industry classification
- **Financial Position**: Visual chart showing assets, liabilities, and equity
- **Health Metrics**: Automatic debt-to-equity ratio calculation
- **Clean Interface**: No technical knowledge required - just enter a company number

Perfect for investors, sales teams, recruiters, or anyone who needs quick company insights.

## Quick Start

1. **Clone this repo:**
   ```bash
   git clone https://github.com/yourusername/company-health-dashboard.git
   cd company-health-dashboard
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser to:** `http://localhost:8501`

5. **Get your API key:** Sign up at [DataLedger](https://hub.dataledger.uk) for 25 free credits

## Example Companies to Try

Test the dashboard with real UK company numbers:
- Find more on the [Companies House website](https://find-and-update.company-information.service.gov.uk/)

## API Integration

This project demonstrates how to:
- Make authenticated API calls to DataLedger
- Parse JSON responses into usable data
- Create interactive charts with Plotly
- Build instant web interfaces with Streamlit

The entire dashboard is built in under 40 lines of Python - showing how simple it is to turn company data into actionable insights.

## About DataLedger

[DataLedger](https://dataledger.uk) provides structured UK company financial data via a simple REST API. This removes the need to parse PDFs or scrape websites - just make an API call and get clean JSON data back.

Perfect for:
- Lead qualification and sales prospecting
- Investment research and due diligence  
- Recruitment and talent acquisition
- Market analysis and competitor research

## Contributing

Feel free to fork this project and add features like:
- Multi-company comparison charts
- Search with location and financial filters via the search endpoint of the API
- Industry benchmarking
- Export functionality

## License

MIT License - feel free to use this code in your own projects.

---

**Check out the [DataLedger documentation](https://dataledger.uk/docs) **.

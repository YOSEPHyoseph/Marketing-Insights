# Advertising Campaign Dashboard

## Overview
The Advertising Campaign Dashboard is an interactive web application built using Streamlit that allows users to visualize and analyze advertising campaign data. The dashboard provides insights into key metrics, performance trends, and geographical performance, enabling data-driven decision-making.

## Features
- **Dynamic Filtering**: Users can filter data based on campaigns, channels, cities, devices, and date ranges.
- **Key Metrics Calculation**: Displays essential advertising metrics such as Total Spend, Impressions, Clicks, Conversions, and ROAS (Return on Advertising Spend).
- **Interactive Visualizations**: Utilizes Plotly to create various visualizations, including:
  - Spend vs. Conversion Value over time
  - Impressions vs. Clicks
  - Average CTR (Click-Through Rate) over time
  - Daily performance heatmap
  - Device performance comparison
  - Geographical performance scatter plot
- **User-Friendly Interface**: Designed with Streamlit for an intuitive user experience.

## Technologies Used
- **Programming Languages**: Python
- **Frameworks**: Streamlit
- **Data Manipulation**: Pandas
- **Data Visualization**: Plotly
- **Data Input/Output**: OpenPyXL
- **Version Control**: Git
- **Deployment**: Streamlit Cloud

## Installation
To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOSEPHyoseph/Marketing-Insights.git
   cd Marketing-Insights
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run dashboard.py
   ```

## Data
The application requires an Excel file named `campaign_data.xlsx` located in the same directory as `dashboard.py`. Ensure that the file contains the necessary data for the dashboard to function correctly.

## Deployment
The application is deployed on Streamlit Cloud. You can access it [here](https://marketinginsight.streamlit.app/).

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Thanks to the Streamlit community for their support and resources.
- Special thanks to the developers of the libraries used in this project.

# Open-Source Contributor Performance Analysis System

This project aims to analyze the performance of open-source contributors based on key metrics such as contributions, commits, pull requests, and issues. The system includes a Streamlit app that allows users to upload a CSV file of contributor data and view various insights, including performance plots, contributor rankings, and a downloadable PDF report.

## Features

- **Upload Contributor Data**: Upload a CSV file containing contributor data.
- **Data Analysis**: The system processes the data and calculates performance scores for each contributor.
- **Visualizations**:
  - Bar chart comparing actual vs. predicted performance scores.
  - Pie chart showing contributions, commits, pull requests, and issues for the top 10 contributors.
- **Modeling**: A machine learning model predicts the performance score based on features such as contributions, commits, pull requests, and issues.
- **PDF Report Generation**: Download a generated PDF report summarizing the analysis and visualizations.

### Install Dependencies

To install the required dependencies, run:

```bash
pip install -r requirements.txt

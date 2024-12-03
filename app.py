import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from utils import load_data, generate_performance_plot, generate_pie_chart  # Import the pie chart function
from report import generate_pdf_report  # Import the PDF generation function

st.title("Open-Source Contributor Performance Analysis System")

# Load data
uploaded_file = st.file_uploader("Upload your Contributor CSV file", type=["csv"])
if uploaded_file is not None:
    df = load_data(uploaded_file)
    
    # Sidebar options
    st.sidebar.header("User Options")
    if st.sidebar.checkbox("View Raw Data"):
        st.subheader("Raw Data")
        st.write(df)

    # Data preprocessing and modeling
    imputer = SimpleImputer(strategy='mean')
    df['contributions'] = imputer.fit_transform(df[['contributions']])
    
    df['performance_score'] = (
        df['contributions'] * 0.4 +
        df['commits'] * 0.3 +
        df['pull_requests'] * 0.2 +
        df['issues'] * 0.1
    )

    # Train and predict
    X = df[['contributions', 'commits', 'pull_requests', 'issues']]
    y = df['performance_score']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)

    df['predicted_performance_score'] = model.predict(scaler.transform(X))
    df.head()
    
    # Display metrics
    st.write(f"**Mean Squared Error (MSE):** {mean_squared_error(y_test, y_pred):.2f}")
    st.write(f"**R² Score:** {r2_score(y_test, y_pred):.2f}")
    
    # Display performance plot
    st.subheader("Top Contributors: Actual vs. Predicted Performance")
    fig = generate_performance_plot(df)
    st.image(fig, use_column_width=True)
    
    # Display pie chart for top 10 contributors
    st.subheader("Top 10 Contributors Breakdown")
    pie_chart_buf = generate_pie_chart(df)
    st.image(pie_chart_buf, caption="Top 10 Contributor Performance Breakdown", use_column_width=True)
    
    # Generate and download report
    if st.button("Generate PDF Report"):
        pdf_file_path = generate_pdf_report(df)  # Ensure this returns a valid path to the PDF
        with open(pdf_file_path, "rb") as file:
            st.download_button(
                label="Download Report",
                data=file,
                file_name="contributor_report.pdf",
                mime="application/pdf"
            )
            st.success("Report ready for download!")

else:
    st.info("Please upload a CSV file to proceed.")
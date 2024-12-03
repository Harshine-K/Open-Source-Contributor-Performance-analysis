import pandas as pd
import matplotlib.pyplot as plt
import io

def load_data(uploaded_file):
    """
    Load CSV data into a pandas DataFrame.
    """
    df = pd.read_csv(uploaded_file)
    return df

def generate_performance_plot(df):
    # Sort contributors by performance score and select the top 20
    top_20_df = df.sort_values(by='performance_score', ascending=False).head(20)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    bar_positions_actual = range(len(top_20_df))
    bar_positions_predicted = [pos + bar_width for pos in bar_positions_actual]

    # Plot actual vs predicted performance scores
    ax.bar(bar_positions_actual, top_20_df['performance_score'], width=bar_width, label='Actual Performance Score', color='b', alpha=0.7)
    ax.bar(bar_positions_predicted, top_20_df['predicted_performance_score'], width=bar_width, label='Predicted Performance Score', color='r', alpha=0.7)

    # Customize the plot
    ax.set_xlabel('Contributor')
    ax.set_ylabel('Performance Score')
    ax.set_title('Top 20 Contributors: Actual vs. Predicted Performance Scores')
    ax.set_xticks([pos + bar_width / 2 for pos in bar_positions_actual])
    ax.set_xticklabels(top_20_df['login'], rotation=90)
    ax.legend()

    plt.tight_layout()
    
    # Save the plot as a PNG image in memory
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

def generate_pie_chart(df):
    """
    Generate a pie chart for the top 10 contributors based on their contributions, commits,
    pull requests, and issues.
    """
    top_10_df = df.sort_values(by='performance_score', ascending=False).head(10)

    num_rows = 2
    num_cols = 5
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(20, 10))
    axs = axs.flatten()

    for i, (index, row) in enumerate(top_10_df.iterrows()):
        labels = ['Contributions', 'Commits', 'Pull Requests', 'Issues']
        sizes = [row['contributions'], row['commits'], row['pull_requests'], row['issues']]
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

        axs[i].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        axs[i].set_title(f"{row['login']}", fontsize=10)

    for j in range(len(top_10_df), num_rows * num_cols):
        axs[j].axis('off')

    plt.tight_layout()

    # Save the pie chart to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return buf
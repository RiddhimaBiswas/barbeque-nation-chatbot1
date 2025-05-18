import pandas as pd
from datetime import datetime

# Step 1: Generate conversation logs if missing
def generate_sample_log(log_file="conversation_log.txt"):
    """Creates a sample log file if it doesn't exist."""
    sample_logs = [
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},FAQ,Resolved,0.9",
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},New_Booking,Pending,0.7",
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},Cancellation,Resolved,0.8"
    ]

    with open(log_file, "w") as file:
        for log in sample_logs:
            file.write(log + "\n")

    print(f"Sample conversation log '{log_file}' generated!")

# Step 2: Parse the log file
def parse_log(log_file: str) -> pd.DataFrame:
    """Reads and processes the conversation log into a structured DataFrame."""
    logs = []

    try:
        with open(log_file, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    logs.append({"timestamp": parts[0], "intent": parts[1], "status": parts[2], "satisfaction": float(parts[3])})
    except FileNotFoundError:
        print(f"Log file '{log_file}' not found! Generating a new one...")
        generate_sample_log(log_file)  # Generate a sample log automatically
        return parse_log(log_file)  # Retry parsing

    df = pd.DataFrame(logs)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

# Step 3: Generate and save the analysis report
def generate_report(df: pd.DataFrame):
    """Analyzes the conversation log and exports insights to an Excel file."""
    if df.empty:
        print("No data available for analysis.")
        return

    # Calculate metrics
    total_interactions = len(df)
    resolved_rate = df[df["status"] == "Resolved"].shape[0] / total_interactions * 100
    avg_satisfaction = df["satisfaction"].mean()

    summary = {
        "Total Interactions": total_interactions,
        "Resolved Rate (%)": round(resolved_rate, 2),
        "Average Satisfaction Score": round(avg_satisfaction, 2)
    }

    # Export analysis to Excel
    df.to_excel("post_call_analysis.xlsx", index=False)
    
    print("✅ Analysis complete! Report saved as 'post_call_analysis.xlsx'.")
    print("📊 Summary:", summary)

# Step 4: Run the script
if __name__ == "__main__":
    log_file = "conversation_log.txt"
    df = parse_log(log_file)
    generate_report(df)
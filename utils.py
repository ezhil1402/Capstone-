import pandas as pd
import matplotlib.pyplot as plt

def save_data(name, subject, hours, break_time):
    data = pd.DataFrame([[name, subject, hours, break_time]],
                        columns=["Name", "Subject", "Hours", "Break"])
    try:
        old = pd.read_csv("data.csv")
        data = pd.concat([old, data])
    except:
        pass

    data.to_csv("data.csv", index=False)

def load_data():
    try:
        return pd.read_csv("data.csv")
    except:
        return pd.DataFrame(columns=["Name", "Subject", "Hours", "Break"])

def plot_data(df):
    if df.empty:
        return None

    fig, ax = plt.subplots()
    df.groupby("Subject")["Hours"].sum().plot(kind='bar', ax=ax)
    ax.set_title("Study Hours per Subject")
    return fig
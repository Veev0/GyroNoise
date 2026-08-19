import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Set up the web page layout
st.set_page_config(page_title="Velox Gyro Noise Analyzer", layout="wide")
st.title("S892 Velox Gyro Noise Analyzer")
st.markdown("Upload the Rev C CSV output file to generate the noise resonance graphs.")

# Create a file upload button
uploaded_file = st.file_uploader("Upload Gyro Noise CSV", type=['csv'])

if uploaded_file is not None:
    # Read the uploaded file
    content = uploaded_file.getvalue().decode("utf-8")
    lines = content.splitlines()

    axis_0_lines = []
    axis_1_lines = []
    current_axis = None

    # Parse the text to split Axis 0 and Axis 1 data
    for line in lines:
        line = line.strip()
        if not line: continue
        if 'Motor Enabled - Axis_0' in line:
            current_axis = 0
            continue
        if 'Motor Enabled - Axis_1' in line:
            current_axis = 1
            continue
        
        if current_axis == 0:
            axis_0_lines.append(line)
        elif current_axis == 1:
            axis_1_lines.append(line)

    if not axis_0_lines or not axis_1_lines:
        st.error("Error formatting data. Please ensure you are uploading the correct Rev C CSV.")
    else:
        # Load the parsed text into Pandas DataFrames
        df0 = pd.read_csv(io.StringIO('\n'.join(axis_0_lines)))
        df1 = pd.read_csv(io.StringIO('\n'.join(axis_1_lines)))
        
        # Clean up column names
        df0.columns = df0.columns.str.strip()
        df1.columns = df1.columns.str.strip()

        st.success("File parsed successfully! Generating graphs...")

        # Plot the data
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

        # Plot Axis 0
        ax1.plot(df0['MFREQ'], df0['GRAWX_std'], label='Azimuth (X std)', color='r', alpha=0.8)
        ax1.plot(df0['MFREQ'], df0['GRAWY_std'], label='Y std', color='g', alpha=0.8)
        ax1.plot(df0['MFREQ'], df0['GRAWZ_std'], label='Elevation (Z std)', color='b', alpha=0.8)
        ax1.axhline(y=0.2, color='red', linestyle='--', linewidth=3, alpha=0.7, label='Threshold (0.2)')
        ax1.set_title('Gyro Noise vs Motor Frequency (Axis 0)')
        ax1.set_ylabel('Noise (Standard Deviation)')
        ax1.grid(True)
        ax1.legend()
        y_max_0 = max(0.4, df0[['GRAWX_std', 'GRAWY_std', 'GRAWZ_std']].max().max() * 1.1)
        ax1.set_ylim(0, y_max_0)
        
        # Plot Axis 1
        ax2.plot(df1['MFREQ'], df1['GRAWX_std'], label='Azimuth (X std)', color='r', alpha=0.8)
        ax2.plot(df1['MFREQ'], df1['GRAWY_std'], label='Y std', color='g', alpha=0.8)
        ax2.plot(df1['MFREQ'], df1['GRAWZ_std'], label='Elevation (Z std)', color='b', alpha=0.8)
        ax2.axhline(y=0.2, color='red', linestyle='--', linewidth=3, alpha=0.7, label='Threshold (0.2)')
        ax2.set_title('Gyro Noise vs Motor Frequency (Axis 1)')
        ax2.set_xlabel('Motor Frequency (MFREQ)')
        ax2.set_ylabel('Noise (Standard Deviation)')
        ax2.grid(True)
        ax2.legend()
        y_max_1 = max(0.4, df1[['GRAWX_std', 'GRAWY_std', 'GRAWZ_std']].max().max() * 1.1)
        ax2.set_ylim(0, y_max_1)

        plt.tight_layout()
        
        # Display the matplotlib figure in Streamlit
        st.pyplot(fig)

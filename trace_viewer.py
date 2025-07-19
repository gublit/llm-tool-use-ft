import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path

def load_traces_data(file_path):
    """Load traces data from CSV file"""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def parse_trace(trace_str):
    """Parse trace string into list of messages"""
    try:
        # Handle the trace string which appears to be a JSON string
        trace_data = json.loads(trace_str)
        return trace_data
    except json.JSONDecodeError:
        st.error("Error parsing trace data")
        return []

def display_trace(trace_data):
    """Display a single trace with role-based partitioning"""
    if not trace_data:
        st.warning("No trace data to display")
        return
    
    # Create tabs for each message in the trace
    if len(trace_data) > 1:
        tabs = st.tabs([f"Message {i+1} ({msg.get('role', 'unknown')})" for i, msg in enumerate(trace_data)])
        
        for i, (tab, msg) in enumerate(zip(tabs, trace_data)):
            with tab:
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                
                # Color-coded role display
                if role == 'user':
                    st.markdown("### 👤 **User**")
                    st.markdown(f"<div style='background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 4px solid #2196f3;'>{content}</div>", unsafe_allow_html=True)
                elif role == 'assistant':
                    st.markdown("### 🤖 **Assistant**")
                    st.markdown(f"<div style='background-color: #f3e5f5; padding: 10px; border-radius: 5px; border-left: 4px solid #9c27b0;'>{content}</div>", unsafe_allow_html=True)
                elif role == 'system':
                    st.markdown("### ⚙️ **System**")
                    st.markdown(f"<div style='background-color: #fff3e0; padding: 10px; border-radius: 5px; border-left: 4px solid #ff9800;'>{content}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"### ❓ **{role.title()}**")
                    st.markdown(f"<div style='background-color: #f5f5f5; padding: 10px; border-radius: 5px; border-left: 4px solid #9e9e9e;'>{content}</div>", unsafe_allow_html=True)
                
                # Raw JSON view
                with st.expander("Raw JSON"):
                    st.json(msg)
    else:
        # Single message case
        msg = trace_data[0]
        role = msg.get('role', 'unknown')
        content = msg.get('content', '')
        
        if role == 'user':
            st.markdown("### 👤 **User**")
            st.markdown(f"<div style='background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 4px solid #2196f3;'>{content}</div>", unsafe_allow_html=True)
        elif role == 'assistant':
            st.markdown("### 🤖 **Assistant**")
            st.markdown(f"<div style='background-color: #f3e5f5; padding: 10px; border-radius: 5px; border-left: 4px solid #9c27b0;'>{content}</div>", unsafe_allow_html=True)
        elif role == 'system':
            st.markdown("### ⚙️ **System**")
            st.markdown(f"<div style='background-color: #fff3e0; padding: 10px; border-radius: 5px; border-left: 4px solid #ff9800;'>{content}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"### ❓ **{role.title()}**")
            st.markdown(f"<div style='background-color: #f5f5f5; padding: 10px; border-radius: 5px; border-left: 4px solid #9e9e9e;'>{content}</div>", unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Trace Viewer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🔍 Trace Data Viewer")
    st.markdown("View and analyze conversation traces from CSV files")
    
    # Sidebar for file selection
    st.sidebar.header("📁 File Selection")
    
    # Find CSV files in data directory
    data_dir = Path("data")
    csv_files = []
    if data_dir.exists():
        csv_files = list(data_dir.glob("*.csv"))
    
    if not csv_files:
        st.error("No CSV files found in the data directory")
        return
    
    # File selector
    selected_file = st.sidebar.selectbox(
        "Select CSV file:",
        options=csv_files,
        format_func=lambda x: x.name,
        index=0 if any(f.name == "traces.csv" for f in csv_files) else 0
    )
    
    # Load data
    df = load_traces_data(selected_file)
    if df is None:
        return
    
    # Display file info
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**File:** {selected_file.name}")
    st.sidebar.markdown(f"**Rows:** {len(df)}")
    st.sidebar.markdown(f"**Columns:** {len(df.columns)}")
    
    # Display column info
    st.sidebar.markdown("**Columns:**")
    for col in df.columns:
        st.sidebar.markdown(f"- {col}")
    
    # Main content area
    st.markdown("---")
    
    # Trace selection
    if len(df) > 0:
        st.subheader("📋 Trace Selection")
        
        # Create a selection interface
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Show query preview for selection
            if 'query' in df.columns:
                trace_options = [f"{i+1}: {row['query'][:100]}{'...' if len(row['query']) > 100 else ''}" 
                               for i, row in df.iterrows()]
                selected_trace_idx = st.selectbox(
                    "Select a trace to view:",
                    options=range(len(df)),
                    format_func=lambda x: trace_options[x] if x < len(trace_options) else f"Trace {x+1}"
                )
            else:
                selected_trace_idx = st.selectbox(
                    "Select a trace to view:",
                    options=range(len(df)),
                    format_func=lambda x: f"Trace {x+1}"
                )
        
        with col2:
            # Show trace metadata
            if selected_trace_idx < len(df):
                row = df.iloc[selected_trace_idx]
                st.markdown("**Trace Info:**")
                if 'query_type' in df.columns:
                    st.markdown(f"**Type:** {row['query_type']}")
                if 'num_tools_available' in df.columns:
                    st.markdown(f"**Tools Available:** {row['num_tools_available']}")
                if 'tool_needed' in df.columns:
                    st.markdown(f"**Tool Needed:** {row['tool_needed']}")
                if 'tool_name' in df.columns and pd.notna(row['tool_name']):
                    st.markdown(f"**Tool Used:** {row['tool_name']}")
        
        # Display selected trace
        if selected_trace_idx < len(df):
            st.markdown("---")
            st.subheader("💬 Trace Details")
            
            row = df.iloc[selected_trace_idx]
            
            # Show original query if available
            if 'query' in df.columns:
                st.markdown("### 📝 Original Query")
                st.info(row['query'])
            
            # Parse and display trace
            if 'trace' in df.columns:
                trace_data = parse_trace(row['trace'])
                display_trace(trace_data)
            else:
                st.warning("No trace column found in the data")
        
        # Raw data view
        with st.expander("📊 Raw Data View"):
            st.dataframe(df)
            
    else:
        st.warning("No data found in the selected file")

if __name__ == "__main__":
    main() 
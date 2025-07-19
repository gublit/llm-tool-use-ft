import streamlit as st
import pandas as pd
import json
import os
import ast
from typing import Dict, List, Any
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Conversation Trace Viewer",
    page_icon="💬",
    layout="wide"
)

def load_data(file_path: str) -> pd.DataFrame:
    """Load CSV data from file path."""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading {file_path}: {str(e)}")
        return pd.DataFrame()

def parse_trace(trace_str: str) -> List[Dict[str, Any]]:
    """Parse the trace string into a list of messages."""
    try:
        if pd.isna(trace_str) or trace_str == "":
            return []
        
        # First try to parse as JSON
        try:
            trace_data = json.loads(trace_str)
            return trace_data
        except json.JSONDecodeError:
            # If JSON parsing fails, try to evaluate as Python literal
            try:
                trace_data = ast.literal_eval(trace_str)
                return trace_data
            except (ValueError, SyntaxError):
                # If that fails too, try to fix common issues and parse again
                # Handle single quotes by replacing with double quotes
                fixed_str = trace_str.replace("'", '"')
                try:
                    trace_data = json.loads(fixed_str)
                    return trace_data
                except json.JSONDecodeError:
                    # Last resort: try to evaluate the original string as Python code
                    try:
                        trace_data = eval(trace_str)
                        return trace_data
                    except:
                        st.error(f"Could not parse trace data. First 200 chars: {trace_str[:200]}...")
                        return []
                        
    except Exception as e:
        st.error(f"Error processing trace: {str(e)}")
        return []

def serialize_trace(trace_data: List[Dict[str, Any]]) -> str:
    """Serialize trace data back to JSON string."""
    try:
        return json.dumps(trace_data, indent=2)
    except Exception as e:
        st.error(f"Error serializing trace data: {str(e)}")
        return ""

def display_message(message: Dict[str, Any], message_idx: int, edit_mode: bool = False):
    """Display a single message in the conversation."""
    role = message.get('role', 'unknown')
    content = message.get('content', '')
    
    if edit_mode:
        # Edit mode - show input fields within an expander
        with st.expander(f"📝 Message {message_idx + 1} - {role.title()}", expanded=True):
            col1, col2 = st.columns([1, 4])
            with col1:
                new_role = st.selectbox(
                    f"Role {message_idx + 1}:",
                    ['user', 'assistant', 'system'],
                    index=['user', 'assistant', 'system'].index(role) if role in ['user', 'assistant', 'system'] else 0,
                    key=f"role_{message_idx}"
                )
            with col2:
                new_content = st.text_area(
                    f"Content {message_idx + 1}:",
                    value=content,
                    height=100,
                    key=f"content_{message_idx}"
                )
            
            # Update the message data
            message['role'] = new_role
            message['content'] = new_content
        
        return message
    else:

        expander_title = f"Message {message_idx + 1} - {role.title()}"
        
        with st.expander(expander_title, expanded=True):
            # Color coding for different roles with borders
            if role == 'user':
                st.markdown(f"<div style='background-color: #1e1e1e; padding: 15px; border-radius: 8px; margin: 5px 0; border-left: 4px solid #4CAF50; border: 2px solid #4CAF50;'><strong>User</strong><br><br>{content}</div>", unsafe_allow_html=True)
            elif role == 'assistant':
                st.markdown(f"<div style='background-color: #1e1e1e; padding: 15px; border-radius: 8px; margin: 5px 0; border-left: 4px solid #2196F3; border: 2px solid #2196F3;'><strong>Assistant</strong><br><br>{content}</div>", unsafe_allow_html=True)
            elif role == 'system':
                st.markdown(f"<div style='background-color: #1e1e1e; padding: 15px; border-radius: 8px; margin: 5px 0; border-left: 4px solid #FF9800; border: 2px solid #FF9800;'><strong>System</strong><br><br>{content}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background-color: #1e1e1e; padding: 15px; border-radius: 8px; margin: 5px 0; border-left: 4px solid #9E9E9E; border: 2px solid #9E9E9E;'><strong>{role.title()}</strong><br><br>{content}</div>", unsafe_allow_html=True)

def edit_query_info(query_info: Dict[str, Any]) -> Dict[str, Any]:
    """Allow editing of query information."""
    st.subheader("📋 Edit Query Information")
    
    col1, col2 = st.columns(2)
    with col1:
        query_type = st.text_input("Query Type:", value=str(query_info.get('query_type', '')))
        tool_needed = st.text_input("Tool Needed:", value=str(query_info.get('tool_needed', '')))
    with col2:
        tool_name = st.text_input("Tool Name:", value=str(query_info.get('tool_name', '')))
        num_tools_available = st.text_input("Num Tools Available:", value=str(query_info.get('num_tools_available', '')))
    
    query_text = st.text_area("Query:", value=str(query_info.get('query', '')), height=100)
    
    return {
        'query': query_text,
        'query_type': query_type,
        'tool_needed': tool_needed,
        'tool_name': tool_name,
        'num_tools_available': num_tools_available
    }

def display_conversation(trace_data: List[Dict[str, Any]], query_info: Dict[str, Any], edit_mode: bool = False):
    """Display the entire conversation."""
    if edit_mode:
        # Edit mode
        edited_query_info = edit_query_info(query_info)
        
        st.subheader("💬 Edit Conversation Trace")
        
        if not trace_data:
            st.warning("No conversation data available for this query.")
            # Add button to create new message
            if st.button("➕ Add New Message"):
                trace_data.append({"role": "user", "content": ""})
                st.rerun()
            return trace_data, edited_query_info
        
        # Edit each message
        edited_trace_data = []
        for idx, message in enumerate(trace_data):
            edited_message = display_message(message, idx, edit_mode=True)
            edited_trace_data.append(edited_message)
            
            # Add delete button for this message
            if st.button(f"🗑️ Delete Message {idx + 1}", key=f"delete_{idx}"):
                trace_data.pop(idx)
                st.rerun()
        
        # Add button to create new message
        if st.button("➕ Add New Message"):
            trace_data.append({"role": "user", "content": ""})
            st.rerun()
        
        return edited_trace_data, edited_query_info
    else:
        # View mode
        st.subheader("📋 Query Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Query Type:** {query_info.get('query_type', 'N/A')}")
            st.write(f"**Tool Needed:** {query_info.get('tool_needed', 'N/A')}")
        with col2:
            st.write(f"**Tool Name:** {query_info.get('tool_name', 'N/A')}")
            st.write(f"**Num Tools Available:** {query_info.get('num_tools_available', 'N/A')}")
        
        st.write(f"**Query:** {query_info.get('query', 'N/A')}")
        
        st.subheader("💬 Conversation Trace")
        
        if not trace_data:
            st.warning("No conversation data available for this query.")
            return trace_data, query_info
        
        # Display each message in the conversation
        for idx, message in enumerate(trace_data):
            display_message(message, idx, edit_mode=False)
        
        return trace_data, query_info

def export_data(df: pd.DataFrame, filename: str):
    """Export DataFrame to CSV file."""
    try:
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        
        # Add timestamp to filename if not already present
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        # Check if filename already exists and add timestamp if needed
        base_name = filename[:-4]  # Remove .csv extension
        counter = 1
        while os.path.exists(os.path.join(data_dir, filename)):
            filename = f"{base_name}_{counter}.csv"
            counter += 1
        
        full_path = os.path.join(data_dir, filename)
        df.to_csv(full_path, index=False)
        st.success(f"Data exported successfully to {full_path}")
        return True
    except Exception as e:
        st.error(f"Error exporting data: {str(e)}")
        return False

def main():
    st.title("💬 Conversation Trace Viewer & Editor")
    st.markdown("View, edit, and export conversation traces from your CSV data.")
    
    # Initialize session state for modifications
    if 'modified_data' not in st.session_state:
        st.session_state.modified_data = None
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False
    if 'changes_made' not in st.session_state:
        st.session_state.changes_made = False
    
    # Sidebar for controls
    with st.sidebar:
        st.header("📁 File Selection")
        
        # Get available CSV files in data directory
        data_dir = "data"
        if os.path.exists(data_dir):
            csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        else:
            csv_files = []
        
        if not csv_files:
            st.error("No CSV files found in the data directory.")
            return
        
        # File selection dropdown
        default_file = 'traces.csv' if 'traces.csv' in csv_files else csv_files[0]
        selected_file = st.selectbox(
            "Select CSV file:",
            csv_files,
            index=csv_files.index(default_file) if default_file in csv_files else 0
        )
        
        # Load the selected file
        file_path = os.path.join(data_dir, selected_file)
        df = load_data(file_path)
        
        if df.empty:
            st.error("Unable to load data from the selected file.")
            return
        
        # Use modified data if available
        if st.session_state.modified_data is not None:
            df = st.session_state.modified_data
            st.info(f"Using modified data ({len(df)} rows)")
        else:
            st.success(f"Loaded {len(df)} rows from {selected_file}")
        
        # Query selection
        st.header("🔍 Query Selection")
        
        # Initialize session state for current query index
        if 'current_query_idx' not in st.session_state:
            st.session_state.current_query_idx = 0
        
        # Ensure current index is within bounds
        if st.session_state.current_query_idx >= len(df):
            st.session_state.current_query_idx = len(df) - 1
        elif st.session_state.current_query_idx < 0:
            st.session_state.current_query_idx = 0
        
        # Query dropdown
        query_options = [f"Row {i}: {query[:50]}..." if len(query) > 50 else f"Row {i}: {query}" 
                        for i, query in enumerate(df['query'].fillna('No query').astype(str))]
        
        selected_query_idx = st.selectbox(
            "Select query:",
            range(len(query_options)),
            index=st.session_state.current_query_idx,
            format_func=lambda x: query_options[x]
        )
        
        # Update session state
        st.session_state.current_query_idx = selected_query_idx
        
        # Navigation buttons
        st.header("🧭 Navigation")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Previous", disabled=st.session_state.current_query_idx == 0):
                st.session_state.current_query_idx -= 1
                st.rerun()
        
        with col2:
            if st.button("➡️ Next", disabled=st.session_state.current_query_idx == len(df) - 1):
                st.session_state.current_query_idx += 1
                st.rerun()
        
        # Manual query number entry
        st.header("📝 Manual Entry")
        manual_query_num = st.number_input(
            "Enter query number (row):",
            min_value=0,
            max_value=len(df) - 1,
            value=st.session_state.current_query_idx,
            help=f"Enter a number between 0 and {len(df) - 1}"
        )
        
        if st.button("Go to Query"):
            st.session_state.current_query_idx = manual_query_num
            st.rerun()
        
        # Current position indicator
        st.markdown(f"**Current Position:** {st.session_state.current_query_idx + 1} / {len(df)}")

        # Edit mode toggle
        st.header("✏️ Edit Mode")
        edit_mode = st.checkbox("Enable Edit Mode", value=st.session_state.edit_mode)
        st.session_state.edit_mode = edit_mode
        
        if edit_mode:
            st.warning("⚠️ Edit mode is enabled. Changes will be tracked.")
        
        # Export section
        st.header("📤 Export Data")
        
        # Show changes indicator
        if st.session_state.changes_made:
            st.success("✅ Changes detected")
        
        export_filename = st.text_input(
            "Export filename:",
            value=f"modified_{selected_file.replace('.csv', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if st.button("💾 Export as CSV"):
            if export_data(df, export_filename):
                st.session_state.changes_made = False
        
        # Reset changes button
        if st.session_state.changes_made:
            if st.button("🔄 Reset Changes"):
                st.session_state.modified_data = None
                st.session_state.changes_made = False
                st.rerun()
    
    # Main content area
    current_row = df.iloc[st.session_state.current_query_idx]
    
    # Extract query information
    query_info = {
        'query': current_row.get('query', 'N/A'),
        'query_type': current_row.get('query_type', 'N/A'),
        'tool_needed': current_row.get('tool_needed', 'N/A'),
        'tool_name': current_row.get('tool_name', 'N/A'),
        'num_tools_available': current_row.get('num_tools_available', 'N/A')
    }
    
    # Parse and display the conversation
    if 'trace' in current_row and pd.notna(current_row['trace']):
        trace_data = parse_trace(current_row['trace'])
        
        # Display conversation with edit capability
        updated_trace_data, updated_query_info = display_conversation(
            trace_data, query_info, edit_mode=edit_mode
        )
        
        # Save changes if in edit mode
        if edit_mode:
            if st.button("💾 Save Changes"):
                # Initialize modified_data if not already done
                if st.session_state.modified_data is None:
                    st.session_state.modified_data = df.copy()
                
                # Update the current row with modified data
                row_idx = st.session_state.current_query_idx
                
                # Update query information with proper type conversion
                for key, value in updated_query_info.items():
                    if key in st.session_state.modified_data.columns:
                        # Get the original column dtype
                        original_dtype = st.session_state.modified_data[key].dtype
                        
                        try:
                            # Convert value to appropriate type
                            if pd.api.types.is_integer_dtype(original_dtype):
                                # Handle integer conversion
                                if isinstance(value, str):
                                    if value.strip() == '' or value.strip().lower() == 'nan':
                                        converted_value = pd.NA
                                    else:
                                        converted_value = original_dtype.type(int(value))
                                else:
                                    # Already a numeric type
                                    converted_value = original_dtype.type(value)
                            elif pd.api.types.is_float_dtype(original_dtype):
                                # Handle float conversion
                                if isinstance(value, str):
                                    if value.strip() == '' or value.strip().lower() == 'nan':
                                        converted_value = pd.NA
                                    else:
                                        converted_value = original_dtype.type(float(value))
                                else:
                                    # Already a numeric type
                                    converted_value = original_dtype.type(value)
                            elif pd.api.types.is_bool_dtype(original_dtype):
                                # Handle boolean conversion
                                if isinstance(value, str):
                                    converted_value = value.lower() in ('true', '1', 'yes', 'on')
                                else:
                                    converted_value = bool(value)
                            else:
                                # Keep as string for other types
                                converted_value = str(value)
                            
                            st.session_state.modified_data.loc[row_idx, key] = converted_value
                            
                        except (ValueError, TypeError) as e:
                            st.error(f"Error converting '{value}' for column '{key}': {e}")
                            # Keep original value if conversion fails
                            continue
                
                # Update trace data
                if 'trace' in st.session_state.modified_data.columns:
                    st.session_state.modified_data.loc[row_idx, 'trace'] = serialize_trace(updated_trace_data)
                
                st.session_state.changes_made = True
                st.success("✅ Changes saved!")
                st.rerun()
        
        # Raw JSON view section (at the bottom) - now with dropdown
        st.markdown("---")
        with st.expander("🔍 Raw JSON View", expanded=False):
            # Use updated_trace_data if in edit mode, otherwise use original trace_data
            json_data = updated_trace_data if edit_mode else trace_data
            
            # Create tabs for different views
            tab1, tab2 = st.tabs(["📝 Formatted JSON", "🔤 Original Raw Data"])
            
            with tab1:
                if json_data:
                    json_str = serialize_trace(json_data)
                    st.code(json_str, language='json', wrap_lines=True)
                else:
                    st.info("No trace data available")
            
            with tab2:
                raw_trace = current_row.get('trace', 'N/A')
                if raw_trace != 'N/A':
                    st.code(str(raw_trace), language='text', wrap_lines=True)
                else:
                    st.info("No raw trace data available")
    else:
        st.warning("No trace data available for this query.")
        
        # Show raw JSON section even when no trace data is available
        st.markdown("---")
        with st.expander("🔍 Raw JSON View", expanded=False):
            st.info("No trace data available for this query.")

if __name__ == "__main__":
    main()

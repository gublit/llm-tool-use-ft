import ast

def add_answer_tags(trace_str, row_idx=None):
    trace = ast.literal_eval(trace_str)
    final_response = trace[-1]['content']
    
    # Check if both opening and closing tags exist
    if '<final_answer>' in final_response and '</final_answer>' in final_response:
        return trace
    
    # Otherwise, add final_answer tags around the content
    if row_idx is not None:
        print(f"Row {row_idx}: adding tags")
    trace[-1]['content'] = f"<final_answer>\n{final_response}</final_answer>"

    return trace

def replace_trace_messages(df, row_idx, replacements):
    """
    Replace specific messages in the trace for a given row.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The dataframe containing the trace data
    row_idx : int
        The index of the row to modify
    replacements : dict or list
        Either a dict mapping message indices to new content, or a list of dicts
        with 'index', 'role', and 'content' keys for more complex replacements

    """
    
    # Get the trace (convert from string if needed)
    trace = df.at[row_idx, 'trace']
    if isinstance(trace, str):
        trace = ast.literal_eval(trace)
    
    # Make a copy to avoid modifying the original
    trace_copy = trace.copy()
    
    if isinstance(replacements, dict):
        # Simple case: index -> content mapping
        for msg_idx, new_content in replacements.items():
            if 0 <= msg_idx < len(trace_copy):
                trace_copy[msg_idx]['content'] = new_content
            else:
                print(f"Warning: Message index {msg_idx} is out of range (trace has {len(trace_copy)} messages)")
    
    elif isinstance(replacements, list):
        # Complex case: list of replacement specifications
        for replacement in replacements:
            msg_idx = replacement['index']
            if 0 <= msg_idx < len(trace_copy):
                if 'role' in replacement:
                    trace_copy[msg_idx]['role'] = replacement['role']
                if 'content' in replacement:
                    trace_copy[msg_idx]['content'] = replacement['content']
            else:
                print(f"Warning: Message index {msg_idx} is out of range (trace has {len(trace_copy)} messages)")
    
    # Update the dataframe
    df.at[row_idx, 'trace'] = trace_copy
    
    return trace_copy

# Helper function to view a trace in a more readable format
def view_trace(df, row_idx):
    """
    Display the trace for a given row in a readable format.
    """
    
    trace = df.at[row_idx, 'trace']
    if isinstance(trace, str):
        trace = ast.literal_eval(trace)
    
    print(f"Trace for row {row_idx}:")
    print("=" * 50)
    for i, message in enumerate(trace):
        role = message.get('role', 'unknown')
        content = message.get('content', '')
        print(f"[{i}] {role.upper()}:")
        print(f"    {content}")
        print()

# Helper function to find messages by role
def find_messages_by_role(df, row_idx, role):
    """
    Find all message indices with a specific role.
    """
    
    trace = df.at[row_idx, 'trace']
    if isinstance(trace, str):
        trace = ast.literal_eval(trace)
    
    indices = []
    for i, message in enumerate(trace):
        if message.get('role') == role:
            indices.append(i)
    
    return indices

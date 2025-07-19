import importlib
import inspect
from typing import Any, Dict, List, Union, Optional, Tuple
import re
import json

def call_tool(tool_name: str, args: Dict[str, Any]) -> Any:
    """
    Dynamically execute a tool function based on its name and arguments.
    
    Args:
        tool_name: Name of the tool to execute (must match a function in tools.py)
        args: Dictionary of arguments to pass to the tool function
        
    Returns:
        The result of the tool execution
        
    Raises:
        ValueError: If tool_name is not found or arguments are invalid
        Exception: Any exception raised by the tool function
    """
    # Import the tools module
    try:
        tools_module = importlib.import_module('utils.tools')
    except ImportError:
        raise ValueError("Could not import utils.tools module")
    
    # Check if the tool function exists
    if not hasattr(tools_module, tool_name):
        available_tools = [name for name in dir(tools_module) 
                          if callable(getattr(tools_module, name)) and not name.startswith('_')]
        raise ValueError(f"Tool '{tool_name}' not found. Available tools: {available_tools}")
    
    # Get the tool function
    tool_func = getattr(tools_module, tool_name)
    
    # Get function signature to understand expected parameters
    sig = inspect.signature(tool_func)
    parameters = sig.parameters
    
    # Prepare arguments for the function call
    call_args = {}
    
    for param_name, param_info in parameters.items():
        if param_name in args:
            # Convert argument to the expected type based on annotation
            param_type = param_info.annotation
            arg_value = args[param_name]
            
            # Handle type conversion
            if param_type != inspect.Parameter.empty:
                try:
                    # Handle Union types (e.g., Union[int, float])
                    if hasattr(param_type, '__origin__') and param_type.__origin__ is Union:
                        # Try each type in the Union
                        converted = False
                        for union_type in param_type.__args__:
                            if union_type is type(None):  # Handle Optional types
                                continue
                            try:
                                if union_type == List[Any] or union_type == List:
                                    # Handle list types
                                    if isinstance(arg_value, list):
                                        call_args[param_name] = arg_value
                                        converted = True
                                        break
                                elif union_type == Dict[str, Any] or union_type == Dict:
                                    # Handle dict types
                                    if isinstance(arg_value, dict):
                                        call_args[param_name] = arg_value
                                        converted = True
                                        break
                                elif union_type == bool:
                                    # Handle boolean conversion
                                    if isinstance(arg_value, bool):
                                        call_args[param_name] = arg_value
                                        converted = True
                                        break
                                    elif isinstance(arg_value, (int, float)):
                                        call_args[param_name] = bool(arg_value)
                                        converted = True
                                        break
                                elif union_type in (int, float):
                                    # Handle numeric types
                                    call_args[param_name] = union_type(arg_value)
                                    converted = True
                                    break
                                elif union_type == str:
                                    # Handle string types
                                    call_args[param_name] = str(arg_value)
                                    converted = True
                                    break
                            except (ValueError, TypeError):
                                continue
                        
                        if not converted:
                            call_args[param_name] = arg_value  # Use original value if conversion fails
                    else:
                        # Handle simple types
                        if param_type == List[Any] or param_type == List:
                            if isinstance(arg_value, list):
                                call_args[param_name] = arg_value
                            else:
                                raise ValueError(f"Parameter '{param_name}' expects a list")
                        elif param_type == Dict[str, Any] or param_type == Dict:
                            if isinstance(arg_value, dict):
                                call_args[param_name] = arg_value
                            else:
                                raise ValueError(f"Parameter '{param_name}' expects a dictionary")
                        elif param_type == bool:
                            if isinstance(arg_value, bool):
                                call_args[param_name] = arg_value
                            elif isinstance(arg_value, (int, float)):
                                call_args[param_name] = bool(arg_value)
                            else:
                                raise ValueError(f"Parameter '{param_name}' expects a boolean")
                        elif param_type in (int, float):
                            call_args[param_name] = param_type(arg_value)
                        elif param_type == str:
                            call_args[param_name] = str(arg_value)
                        else:
                            call_args[param_name] = arg_value
                except (ValueError, TypeError) as e:
                    raise ValueError(f"Invalid type for parameter '{param_name}': {e}")
        elif param_info.default != inspect.Parameter.empty:
            # Use default value if parameter is not provided
            call_args[param_name] = param_info.default
        else:
            # Required parameter is missing
            raise ValueError(f"Required parameter '{param_name}' is missing")
    
    # Execute the tool function
    try:
        result = tool_func(**call_args)
        return result
    except Exception as e:
        # Re-raise the exception with context
        raise Exception(f"Error executing tool '{tool_name}': {str(e)}")
    
    import re
import json
from typing import Dict, Any, Optional, Tuple

def parse_tool_call(response: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    """
    Parse an LLM response to extract tool calls in XML format.
    
    Args:
        response: The LLM response string that may contain tool calls
        
    Returns:
        Tuple of (tool_name, args_dict) if a tool call is found, None otherwise
        
    Example:
        response = '''Here's the calculation:
        <tool_call>
        {
          "tool_name": "calculator",
          "args": {
            "expression": "75 / 8"
          }
        }
        </tool_call>'''
        
        tool_name, args = parse_tool_call(response)
        # Returns: ("calculator", {"expression": "75 / 8"})
    """
    # Regex pattern to match tool calls in XML format
    # This handles both single-line and multi-line JSON content
    pattern = r'<tool_call>\s*(\{.*?\})\s*</tool_call>'
    
    # Find all matches in the response
    matches = re.findall(pattern, response, re.DOTALL)
    
    if not matches:
        return None
    
    # Take the first tool call if multiple are found
    tool_call_json = matches[0]
    
    try:
        # Parse the JSON content
        tool_call_data = json.loads(tool_call_json)
        
        # Extract tool_name and args
        tool_name = tool_call_data.get('tool_name')
        args = tool_call_data.get('args', {})
        
        if tool_name is None:
            return None
            
        return tool_name, args
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON in tool call: {e}")
        return None
    except Exception as e:
        print(f"Error parsing tool call: {e}")
        return None
    
def format_tool_result(result: str):
    return f"""<tool_result>\n{result}\n</tool_result>"""
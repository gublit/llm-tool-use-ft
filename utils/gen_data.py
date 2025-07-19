from dotenv import load_dotenv
import os
from openai import OpenAI
from together import Together

import yaml
import random
import json
from typing import List, Dict, Any

# import sk from .env file
load_dotenv()

def send_openai_request(instructions: str, user_input: str, model_name: str = 'gpt-4.1', temperature: float = 1.0, n: int = 1):
    """
    Send a request to OpenAI's responses API.

    Args:
        instructions (str): The instructions for the response
        user_input (str): The input for the response
        model_name (str): OpenAI model to use (default: 'gpt-4.1')
        temperature (float): Temperature for the response (default: 1.0)

    Returns:
        str: Response from OpenAI's responses API
    """
    # connect to openai API
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "developer", "content": instructions},
            {"role": "user", "content": user_input}
        ],
        temperature=temperature,
        n=n
    )
    
    return [completion.choices[i].message.content for i in range(len(completion.choices))]

def send_tai_request(system_prompt: str, query: str, model_name: str = 'google/gemma-3n-E4B-it', temperature: int = 1):
    """
    Send a request to Together AI's chat completions API.

    Args:
        system_prompt (str): The system prompt to guide the model's behavior
        query (str): The user query or input to process
        model_name (str): Together AI model to use (default: 'google/gemma-3n-E4B-it')
        temperature (int): Temperature for controlling response randomness (default: 1)

    Returns:
        str: Response content from the Together AI model
    """
    client = Together()
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        temperature=temperature
    )
    
    return response.choices[0].message.content

def send_tai_messages(message_list: list, model_name: str = 'google/gemma-3n-E4B-it', temperature: int = 1):
    """
    Send a list of messages to Together AI's chat completions API.

    Args:
        message_list (list): List of message dictionaries with 'role' and 'content' keys
        model_name (str): Together AI model to use (default: 'google/gemma-3n-E4B-it')
        temperature (int): Temperature for controlling response randomness (default: 1)

    Returns:
        str: Response content from the Together AI model
    """
    client = Together()
    
    response = client.chat.completions.create(
        model=model_name,
        messages=message_list,
        temperature=temperature
    )
    
    return response.choices[0].message.content

def load_tool_metadata(file_path='utils/tools.yaml'):
    """
    Load and parse tool metadata from a YAML file.
    
    Args:
        file_path (str): Path to the tools YAML file (default: 'tools/tools.yaml')
    
    Returns:
        list: List of tool metadata strings, each containing name, description, and parameters
    """
    # Read and parse the tools.yaml file
    with open(file_path, 'r') as file:
        tools = yaml.safe_load(file)

    tool_metadata_list = []

    # Build metadata strings for each tool
    for i, tool in enumerate(tools, 1):
        metadata_parts = []
        metadata_parts.append(f"Name: {tool['name']}")
        metadata_parts.append(f"Description: {tool['description']}")
        
        # Add parameters if they exist
        if 'parameters' in tool and 'properties' in tool['parameters']:
            metadata_parts.append("Parameters:")
            for param_name, param_details in tool['parameters']['properties'].items():
                metadata_parts.append(f"  {param_name}: {param_details['type']} - {param_details['description']}")
        else:
            metadata_parts.append("  Parameters: None")
        
        # Join all parts into a single string and add to list
        tool_metadata = '\n'.join(metadata_parts)
        tool_metadata_list.append(tool_metadata)
    
    return tool_metadata_list

def get_tool_name(tool_metadata):
    """Get tool name from metadata"""
    return tool_metadata.split('\n')[0].split(':')[1].strip()

def load_tools_from_yaml() -> List[Dict[str, Any]]:
    """Load all available tools from the tools.yaml file."""
    with open('utils/tools.yaml', 'r') as file:
        tools_data = yaml.safe_load(file)
    return tools_data

def format_tool_for_system_prompt(tool: Dict[str, Any]) -> Dict[str, Any]:
    """Format a tool from YAML format to the system prompt format."""
    formatted_tool = {
        "tool_name": tool["name"],
        "description": tool["description"],
        "input_args": {}
    }
    
    # Convert parameters to input_args format
    if "parameters" in tool and "properties" in tool["parameters"]:
        for param_name, param_info in tool["parameters"]["properties"].items():
            param_type = param_info.get("type", "string")
            param_desc = param_info.get("description", "")
            
            # Format the type description
            if param_type == "array":
                type_desc = "array"
            elif param_type == "integer":
                type_desc = "integer"
            elif param_type == "number":
                type_desc = "number"
            elif param_type == "boolean":
                type_desc = "boolean"
            else:
                type_desc = "string"
            
            # Include both type and description
            if param_desc:
                formatted_tool["input_args"][param_name] = f"{type_desc} - {param_desc}"
            else:
                formatted_tool["input_args"][param_name] = type_desc
    
    return formatted_tool

def generate_system_prompt(correct_tool: str, num_random_tools: int = 5, filepath: str = 'prompts/system.md') -> str:
    """
    Generate a system prompt using the template in system.md.
    
    Args:
        correct_tool: The name of the tool that should be called (can be None)
        num_random_tools: Number of random tools to include (excluding the correct tool)
    
    Returns:
        The formatted system prompt string
    """
    # Load all available tools
    all_tools = load_tools_from_yaml()
    
    # Find the correct tool
    correct_tool_data = None
    if correct_tool is not None:
        for tool in all_tools:
            if tool["name"] == correct_tool:
                correct_tool_data = tool
                break

        if not correct_tool_data:
            raise ValueError(f"Tool '{correct_tool}' not found in tools.yaml")
    
    # Get random tools (excluding the correct tool if it exists)
    available_tools = [tool for tool in all_tools if tool["name"] != correct_tool]
    random_tools = random.sample(available_tools, min(num_random_tools, len(available_tools)))
    
    # Combine correct tool with random tools and shuffle the order
    if correct_tool_data is not None:
        selected_tools = [correct_tool_data] + random_tools
    else:
        selected_tools = random_tools
    random.shuffle(selected_tools)  # This randomizes the order
    
    # Format all tools
    formatted_tools = [format_tool_for_system_prompt(tool) for tool in selected_tools]
    
    # Load the system template
    with open(filepath, 'r') as file:
        template = file.read()
    
    # Convert tools to JSON format
    tools_json = json.dumps(formatted_tools, indent=2)
    
    # Replace the {tools} placeholder in the template
    system_prompt = template.replace("{tools}", tools_json)

    # add today's date for time-based queries
    if correct_tool in ['create_event', 'set_reminder', 'add_to_do_list']:
        system_prompt = system_prompt + "\n\n Current date: 2024-01-15"
    
    return system_prompt

def num_tools_available(user_input: str) -> int:
    """
    Returns different values based on user input:
    - If input is 'none': returns 0
    - If input is 'single': returns 1
    - If input is 'few': returns random number between 0-9
    - If input is 'many': returns random number between 10-39
    - Otherwise: raises ValueError
    
    Args:
        user_input: String indicating the desired number of tools
        
    Returns:
        Integer representing the number of tools available
    """
    if user_input.lower() == 'none':
        return 0
    elif user_input.lower() == 'single':
        return 1
    elif user_input.lower() == 'few':
        return random.randint(0, 9)
    elif user_input.lower() == 'many':
        return random.randint(10, 39)
    else:
        raise ValueError("Input must be 'single', 'few', or 'many'")

import json
import os
from termcolor import colored
import openai
from typing import Dict, List

# Constants
SYSTEM_FILE = "10_000_system.json"
MODEL = "gpt-4"

def load_system_messages() -> List[Dict]:
    """Load system messages from JSON file"""
    try:
        print(colored("Loading system messages...", "cyan"))
        with open(SYSTEM_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(colored(f"Successfully loaded {len(data)} system messages", "green"))
        return data
    except Exception as e:
        print(colored(f"Error loading system messages: {str(e)}", "red"))
        raise

def get_system_message_by_id(messages: List[Dict], message_id: str) -> Dict:
    """Get a system message by ID"""
    try:
        for msg in messages:
            if msg.get("id") == message_id:
                return msg
        raise ValueError(f"No system message found with ID: {message_id}")
    except Exception as e:
        print(colored(f"Error getting system message: {str(e)}", "red"))
        raise

def chat_with_ai(system_message: Dict):
    """Chat with AI using selected system message"""
    try:
        print(colored("\nStarting chat with AI specialized in:", "cyan"))
        print(colored(f"Category: {system_message.get('parent_category')}", "yellow"))
        print(colored(f"Subcategory: {system_message.get('subcategory')}\n", "yellow"))
        
        openai.api_key = os.getenv("OPENAI_API_KEY")
        messages = [{"role": "system", "content": system_message["system_message"]}]
        
        while True:
            user_input = input(colored("You: ", "green"))
            if user_input.lower() in ["quit", "exit", "bye"]:
                break
                
            messages.append({"role": "user", "content": user_input})
            
            try:
                response = openai.chat.completions.create(
                    model=MODEL,
                    messages=messages
                )
                ai_response = response.choices[0].message.content
                messages.append({"role": "assistant", "content": ai_response})
                print(colored(f"\nAI: {ai_response}\n", "blue"))
                
            except Exception as e:
                print(colored(f"Error getting AI response: {str(e)}", "red"))
                break
                
    except Exception as e:
        print(colored(f"Error in chat: {str(e)}", "red"))
        raise

def main():
    """Main function"""
    try:
        # Load system messages
        messages = load_system_messages()
        
        # Get system message ID from user
        print(colored("\nEnter the ID of the system message (e.g. '149-1'):", "cyan"))
        message_id = input(colored("ID: ", "yellow")).strip()
        
        # Get system message
        system_message = get_system_message_by_id(messages, message_id)
        
        # Start chat
        chat_with_ai(system_message)
        
    except Exception as e:
        print(colored(f"Error in main: {str(e)}", "red"))

if __name__ == "__main__":
    main()

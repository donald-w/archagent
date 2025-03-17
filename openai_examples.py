#%% [markdown]
"""
# OpenAI API Examples
This file demonstrates various ways to interact with the OpenAI API.
Each section shows different functionality and usage patterns.
"""

#%% [markdown]
"""
## Setup and Initialization
First, we'll set up our environment and test the API connection
"""

#%% Setup and Imports
# region: Initial Setup
# Import required libraries
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()
# endregion

#%% API Client Initialization
# region: OpenAI Client
# Initialize the OpenAI client
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

# Test the API connection
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print("✅ API connection successful!")
except Exception as e:
    print("❌ API connection failed. Please check your API key and internet connection.")
    print(f"Error: {str(e)}")
# endregion

#%% [markdown]
"""
## Basic Completion
Simple example of getting a completion from the API
"""

#%% Basic Completion Function
# region: Basic Completion
def get_completion(prompt, model="gpt-3.5-turbo"):
    """Simple function to get a completion from OpenAI"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Example usage
prompt = "Explain what a large language model is in simple terms."
response = get_completion(prompt)
print("Prompt:", prompt)
print("\nResponse:", response)
# endregion

#%% [markdown]
"""
## Chat with History
Demonstrates how to maintain conversation history
"""

#%% Chat History Implementation
# region: Chat History
def chat_with_history(conversation, model="gpt-3.5-turbo"):
    """Function to chat while maintaining conversation history"""
    response = client.chat.completions.create(
        model=model,
        messages=conversation
    )
    return response.choices[0].message.content

# Start a conversation about programming
conversation = [
    {"role": "user", "content": "What is Python programming language best used for?"}
]

# Get first response
response = chat_with_history(conversation)
print("User: What is Python programming language best used for?")
print("Assistant:", response)

# Add the response to conversation history
conversation.append({"role": "assistant", "content": response})

# Ask a follow-up question
conversation.append({"role": "user", "content": "Can you give me a simple example of Python code?"})
response = chat_with_history(conversation)
print("\nUser: Can you give me a simple example of Python code?")
print("Assistant:", response)
# endregion

#%% [markdown]
"""
## Advanced Parameters
Example showing how to use temperature and other parameters
"""

#%% Temperature and Parameters
# region: Advanced Parameters
def get_completion_with_params(prompt, model="gpt-3.5-turbo", temperature=0.7, max_tokens=150):
    """Get completion with adjustable parameters"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

# Let's see how temperature affects creativity
prompt = "Write a short story about a robot discovering emotions"

print("With low temperature (more focused/deterministic):")
print(get_completion_with_params(prompt, temperature=0.2))

print("\nWith high temperature (more creative/random):")
print(get_completion_with_params(prompt, temperature=0.9))
# endregion

#%% [markdown]
"""
## Structured Responses
Getting responses in JSON format using system messages
"""

#%% JSON Responses
# region: Structured Output
def get_structured_response(prompt):
    """Get a structured response from the model"""
    system_message = "You are a helpful assistant that always responds in JSON format."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Example: Get a structured response about a book
prompt = "Give me information about the book '1984' by George Orwell. Include: title, author, year, and main themes"
structured_response = get_structured_response(prompt)
print(structured_response)
# endregion

#%% [markdown]
"""
## Error Handling
Implementing retry logic and error handling
"""

#%% Error Handling Implementation
# region: Error Handling
def safe_completion(prompt, model="gpt-3.5-turbo", max_retries=3):
    """Function with error handling and retries"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            print(f"Attempt {attempt + 1} failed. Retrying in 1 second...")
            time.sleep(1)

# Example usage with potentially problematic prompt
try:
    response = safe_completion("Tell me about error handling in Python", max_retries=2)
    print("Success! Response:", response)
except Exception as e:
    print(f"Failed after all retries. Error: {str(e)}")
# endregion 
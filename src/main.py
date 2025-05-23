"""
Main module containing core functionality.
"""

def greet(name: str) -> str:
    """
    Return a greeting message.
    
    Args:
        name (str): Name to greet
        
    Returns:
        str: Greeting message
    """
    return f"Hello, {name}!"

def main():
    """Main function to demonstrate usage."""
    print(greet("World"))

if __name__ == "__main__":
    main() 
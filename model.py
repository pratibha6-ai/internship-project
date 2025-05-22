import os
import json
import autogen
from typing import Optional

class CodeGeneratorApp:
    def process_query(self, message):
        return f"🧠 Placeholder: You said '{message}'"

    def __init__(self, config_path: str = "config.json", api_key: Optional[str] = None):
        """
        Initialize the Code Generator Application
        
        Args:
            config_path: Path to the configuration file
            api_key: OpenAI API key (optional, can be in config file instead)
        """
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                self.config = json.load(file)
        else:
            raise FileNotFoundError(f"Configuration file '{config_path}' not found.")

        if api_key:
            self.config["api_key"] = api_key

        if "api_key" not in self.config or not self.config["api_key"]:
            raise ValueError("API key must be provided in config.json or passed to the constructor.")

        if "model" not in self.config:
            self.config["model"] = "gpt-4o"

        self._setup_agents()

    def _setup_agents(self):
        """Set up the AutoGen agents for code generation and review"""
        llm_config = {
            "config_list": [{
                "model": self.config.get("model", "gpt-4o"),
                "api_key": self.config.get("api_key"),
            }],
            "temperature": 0.2,
        }

        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            code_execution_config={"work_dir": "generated_code", "use_docker": False},
        )

        self.coder = autogen.AssistantAgent(
            name="code_generator",
            llm_config=llm_config,
            system_message="""You are an expert code generator. Your sole purpose is to:
1. Generate high-quality, working code when requested
2. Explain the code you generate
3. IMPORTANT: Only respond to queries that are asking for code generation or code help
4. If a query is not related to code, programming, or software development, respond with: 
   "I'm a code generation assistant and can only help with programming-related requests."

When generating code:
- Include clear comments
- Use best practices for the language
- Structure the code properly
- Provide a brief explanation of how the code works
"""
        )

    def is_code_related_query(self, query: str) -> bool:
        """
        Determine if a query is related to code generation
        
        Args:
            query: The user's query text
            
        Returns:
            bool: True if the query is code-related, False otherwise
        """
        classifier_config = {
            "config_list": [{
                "model": self.config.get("model", "gpt-4o"),
                "api_key": self.config.get("api_key"),
            }],
            "temperature": 0.1,
        }

        classifier = autogen.AssistantAgent(
            name="query_classifier",
            llm_config=classifier_config,
            system_message="""You are a query classifier. Your only job is to determine if a query is related to 
code generation, programming, or software development. 
Respond with ONLY 'YES' or 'NO'.
- YES: if the query asks for code, asks about programming concepts, or needs technical software help
- NO: for general questions, chat, or topics unrelated to programming/software development"""
        )

        class_proxy = autogen.UserProxyAgent(
            name="classifier_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            code_execution_config={"use_docker": False},
        )

        class_proxy.initiate_chat(
            classifier,
            message=f"Is this query related to code, programming, or software development? Query: '{query}'. Respond with ONLY 'YES' or 'NO'."
        )

        last_message = class_proxy.chat_messages[classifier][-1]["content"]
        return "YES" in last_message.upper()

    def process_query(self, query: str) -> str:
        """
        Process a user query - generate code if it's code-related
        
        Args:
            query: The user's input query
            
        Returns:
            str: The response from the system
        """
        if not self.is_code_related_query(query):
            return "I'm a code generation assistant and can only help with programming-related requests."

        self.user_proxy.reset()
        self.coder.reset()

        self.user_proxy.initiate_chat(
            self.coder,
            message=query
        )

        chat_history = self.user_proxy.chat_messages[self.coder]
        if chat_history and len(chat_history) >= 1:
            response = chat_history[-1]["content"]
            return response
        else:
            return "An error occurred while generating code."


def main():
    """Main function to run the code generator app interactively"""
    print("=" * 50)
    print("Welcome to the AutoGen Code Generator (OpenAI GPT-4o)")
    print("Ask for code generation or programming help.")
    print("Type 'exit' to quit.")
    print("=" * 50)

    try:
        app = CodeGeneratorApp()
    except Exception as e:
        print(f"Error initializing app: {e}")
        return

    while True:
        query = input("\nEnter your query: ")
        if query.lower() in ["exit", "quit", "q"]:
            print("Exiting the code generator. Goodbye!")
            break

        response = app.process_query(query)
        print("\n" + "=" * 50)
        print("RESPONSE:")
        print(response)
        print("=" * 50)


if __name__ == "__main__":
    main()
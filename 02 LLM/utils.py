import os

import tiktoken


def get_secret(name, default=None):
    # Making decouple first as os.environ can fail on local sometimes.
    try:
        from decouple import config
        return config(name, default)
    except (ImportError, ModuleNotFoundError):
        return os.environ.get(name, default)



def count_tokens(text: str, model_name: str = "gpt-4o") -> int:
    """
    Returns the exact number of tokens in a text string for a specific model.
    # --- Example Usage ---
    sample_prompt = "Language tokenization is essential for AI!"
    model = "gpt-4o"
    num_tokens = count_tokens(sample_prompt, model_name=model)
    """
    try:
        # Automatically loads the correct tokenizer vocabulary for the model
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
        
    # Convert text to token IDs and calculate the length of the list
    token_list = encoding.encode(text)
    return len(token_list)


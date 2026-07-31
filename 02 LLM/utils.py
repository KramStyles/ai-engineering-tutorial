import os

from huggingface_hub import HfApi
import tiktoken


api = HfApi()


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


def get_hugging_model_size(model: str, revision=None):
    # model = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"

    model_info = api.model_info(repo_id=model, files_metadata=True, revision=revision)  # noqa:E501

    # Calculate total size of all repo files
    total_bytes = sum(file.size for file in model_info.siblings if file.size)
    total_mb = total_bytes / (1024 * 1024)

    print(f"Total download size: {total_mb:.2f} MB")

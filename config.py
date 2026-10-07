
key = ""
with open("key.txt", "r") as f:
    key = f.read().strip()


class Config:
    gemini_api_key: str = key


config_obj = Config()
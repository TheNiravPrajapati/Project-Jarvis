from openai import OpenAI

client = OpenAI(
    api_key = "",
)


completion = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "system","content": "You are a Virtual Assistant, Named Jarvis, skilled in general task like alexa and google"},
        {"role": "user","content": "What is Coding"}
    ]
)
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def analyze_resume(text):

    prompt = f"""
    Analyze this resume:

    {text}

    Return:
    - Resume Score (0-100)
    - Strengths
    - Weaknesses
    - Missing Skills
    - Recommended Roles
    """

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role":"user","content":prompt}
        ]
    )

    return response.choices[0].message.content

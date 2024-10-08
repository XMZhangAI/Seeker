from openai import OpenAI
BASE_URL = "your_base_url"
API_KEY = "your_api_key"
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

model_names = ["gpt-4", "gpt-4-0613", "gpt-4-1106-preview", "gpt-3.5-turbo", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-1106", "gpt-4-vision-preview"]

def gpt_call(model_name, prompt):
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    print(gpt_call(model_names[0], "Please introduce yourself in twenty words."))
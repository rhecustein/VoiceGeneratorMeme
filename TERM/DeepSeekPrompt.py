import os, sys, re, json

print(" [+] DeepSeekPrompt")

print(" [!] Loading dependency...")
try:
    from dotenv import load_dotenv
    from openai import OpenAI
except Exception as e:
    print(" [+] Installing dependency...")
    dependeny = ["python-dotenv", "openai"]
    for i in dependeny:
        os.system("python -m pip install " + i)

    try:
        from dotenv import load_dotenv
        from openai import OpenAI
    except:
        print(" [!] Failed to install dependency")
        input(" [!] Error, please check internet connection")
        sys.exit()


dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

try:
    DEEPSEEK_KEY = os.getenv("DEEPSEEK_KEY")
except:
    sys.exit(" [!] INVALID CONFIG")
DEEPSEEK_CLIENT = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com/v1")
DEEPSEEK_OUTPUT_LANGUAGE = "en"


def create_5_jokes(topic):
    response = DEEPSEEK_CLIENT.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "You are a funny standup comedian, your language code is "
                + DEEPSEEK_OUTPUT_LANGUAGE
                + "and you must search topic based in this language and anwer only in this language, create 5 jokes from the topic inputted by user, jokes must have setup and punchline, you must output only json array containing setup and punchline",
            },
            {
                "role": "user",
                "content": topic,
            },
        ],
    )
    patt_markdown = r'"setup": "(.*?)",\s*"punchline": "(.*?)"'
    match_markdown = re.findall(patt_markdown, response.choices[0].message.content)

    try:
        extracted_arr = []
        for setup, punchline in match_markdown:
            extracted_arr.append({"setup": setup, "punchline": punchline})
        response_json = json.loads(json.dumps(extracted_arr))
        return response_json
    except Exception as e:
        print(e)
        print(" [ERROR 1]")
        return None


def main():

    while True:
        prompt = input(" [INPUT TOPIC] >> ")
        if prompt == "exit":
            break
        else:
            print(" ...please wait")
            try:
                jokes = create_5_jokes(prompt)
                index = 0
                for joke in jokes:
                    print(f" {index +1}. {joke['setup']}")
                    print(f" >> {joke['punchline']}")
                    index += 1
            except Exception as e:
                print(e)
                print(" [ERROR 2]")
            input("...press enter to Continue")
    sys.exit(" [EXIT] ")


if __name__ == "__main__":
    main()

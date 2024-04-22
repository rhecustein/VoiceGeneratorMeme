import os, sys, re, json

# Please manually install
# - PyTorch with CUDA -- https://pytorch.org/get-started/locally/
# - GIT SCM -- https://git-scm.com/downloads

print(" [+] DeepSeekBarkPrompt")

print(" [!] Loading dependency...")
try:
    from dotenv import load_dotenv
    from openai import OpenAI
    from transformers import AutoProcessor, BarkModel
    import torch
except Exception as e:
    print(" [+] Installing dependency...")
    dependeny = ["python-dotenv", "openai"]
    for i in dependeny:
        os.system("python -m pip install " + i)
        os.system("pip install git+https://github.com/huggingface/transformers.git")
        sys.exit(
            "Please manually install PyTorch -- https://pytorch.org/get-started/locally/"
        )

    try:
        from dotenv import load_dotenv
        from openai import OpenAI
        from transformers import AutoProcessor, BarkModel
        import torch
    except:
        print(" [!] Failed to install dependency")
        input(" [!] Error, please check internet connection")
        sys.exit()


dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

os.environ["SUNO_OFFLOAD_CPU"] = "True"
os.environ["SUNO_USE_SMALL_MODELS"] = "True"

OUTPUT_DIR = "./tmp"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


try:
    DEEPSEEK_KEY = os.getenv("DEEPSEEK_KEY")
except:
    sys.exit(" [!] INVALID CONFIG")
DEEPSEEK_CLIENT = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com/v1")
DEEPSEEK_OUTPUT_LANGUAGE = "en"


def check_cuda_device():
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    return device


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


def generate_voice(jokes, filename):
    device = check_cuda_device()
    print(" [i] Loading autoprocessor...")
    processor = AutoProcessor.from_pretrained("suno/bark")
    voice_preset = "v2/en_speaker_9"
    text_prompts = jokes

    print(" [i] Loading bark model...")
    model = BarkModel.from_pretrained("suno/bark").to(device)

    print(" ...processing")
    inputs = processor(text_prompts, voice_preset=voice_preset).to(device)

    print(" ...generating")
    audio_array = model.generate(**inputs, pad_token_id=10500)
    audio_array = audio_array.cpu().numpy().squeeze()

    import scipy

    sample_rate = model.generation_config.sample_rate
    scipy.io.wavfile.write(
        f"{OUTPUT_DIR}/{filename}.wav", rate=sample_rate, data=audio_array
    )


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
                    index += 1
                    print(f" {index}. {joke['setup']}")
                    print(f" >> {joke['punchline']}")

                print("")
                print(" [AI VOICE] Generating File")
                index = 0
                for joke in jokes:
                    index += 1
                    filename = f"{prompt}_{index}.wave"
                    print(f" {index}. {filename}")
                    generate_voice(
                        f"{joke['setup']} [silent] {joke['punchline']}", filename
                    )

            except Exception as e:
                print(e)
                print(" [ERROR 2]")
            input("...press enter to Continue")
            print("")
    sys.exit(" [EXIT] ")


if __name__ == "__main__":
    main()

import os, subprocess, sys, re, json, threading, shutil

print(" [!] Loading dependency...")
# try:
#     from openai import OpenAI
#     from transformers import AutoProcessor, BarkModel
#     from playsound import playsound
#     from pydub import AudioSegment
#     import torch
#     import eel
#     import webview
#     import configparser
#     import scipy
# except Exception as e:
#     print(" [+] Installing dependency...")
#     dependeny = [
#         "openai",
#         "eel",
#         "pywebview",
#         "configparser",
#         "scipy",
#         "playsound==1.2.2",
#         "pydub",
#     ]
#     for i in dependeny:
#         os.system("python -m pip install " + i)
#         os.system("python -m pip install git+https://github.com/huggingface/transformers.git")
#         sys.exit(
#             "Please manually install PyTorch -- https://pytorch.org/get-started/locally/"
#         )

#     try:
#         from openai import OpenAI
#         from transformers import AutoProcessor, BarkModel
#         from playsound import playsound
#         from pydub import AudioSegment
#         import torch
#         import eel
#         import webview
#         import configparser
#         import scipy
#     except:
#         print(" [!] Failed to install dependency")
#         input(" [!] Error, please check internet connection")
#         sys.exit()

from openai import OpenAI
from transformers import AutoProcessor, BarkModel
from playsound import playsound
from pydub import AudioSegment
import torch
import eel
import webview
import configparser
import scipy

os.environ["SUNO_OFFLOAD_CPU"] = "True"
os.environ["SUNO_USE_SMALL_MODELS"] = "True"

TMP_DIR = "./output"
if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)
for filename in os.listdir(TMP_DIR):
    file_path = os.path.join(TMP_DIR, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except:
        pass

deepseek_key = None


def check_config():
    global deepseek_key
    """
    Check the configuration settings by reading the 'config.ini' file.
    If the 'DEEPSEEK_KEY' is found in the config file, create an OpenAI client
    using the key and specified base URL. Set the output language to English.
    Returns True if configuration is successful, False otherwise.
    """
    config = configparser.ConfigParser()
    try:
        config.read("./config.ini")
        deepseek_key = config.get("DEFAULT", "DEEPSEEK_KEY")
        deepseek_key = deepseek_key.replace('"', "")
        return True
    except:
        return False


if check_config():
    window_app = webview.create_window(
        "DeepSeek Prompt 5 Jokes to Voice with Bark",
        "http://localhost:27000/index.html",
        frameless=True,
        width=1280,
        height=660,
        resizable=False,
        fullscreen=False,
    )
else:
    window_app = webview.create_window(
        "DeepSeek Prompt 5 Jokes to Voice with Bark",
        html="Invalid Configuration -- config.ini",
        width=300,
        height=200,
        resizable=False,
        fullscreen=False,
    )
    webview.start(window_app)
    sys.exit()

DEEPSEEK_CLIENT = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com/v1")
DEEPSEEK_OUTPUT_LANGUAGE = "en"


def check_cuda_device():
    """
    A function to check for the availability of CUDA device and return the appropriate torch device.
    """
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    return device


@eel.expose
def generate_voice(jokes, filename, type):
    """
    A function to generate voice from jokes using a specified voice preset.

    Parameters:
    - jokes (str): The jokes to be converted to voice.
    - filename (str): The name of the file to save the generated voice.
    - type (str): The type of voice preset to use, can be "female" for a female voice.

    Returns:
    - str: The file path of the generated voice in .wav format.
    """
    device = check_cuda_device()
    print(" [i] Loading autoprocessor...")
    processor = AutoProcessor.from_pretrained("suno/bark")
    voice_preset = "v2/en_speaker_6"
    if type == "female":
        voice_preset = "v2/en_speaker_9"
    text_prompts = jokes

    print(" [i] Loading bark model...")
    model = BarkModel.from_pretrained("suno/bark").to(device)

    print(" ...processing")
    inputs = processor(text_prompts, voice_preset=voice_preset).to(device)

    print(" ...generating")
    audio_array = model.generate(**inputs, pad_token_id=10500)
    audio_array = audio_array.cpu().numpy().squeeze()

    sample_rate = model.generation_config.sample_rate

    # save wav file
    scipy.io.wavfile.write(
        f"{TMP_DIR}/{filename}.wav", rate=sample_rate, data=audio_array
    )

    # export to mp3
    mp3_export = AudioSegment.from_wav(f"{TMP_DIR}/{filename}.wav")
    mp3_export.export(f"{TMP_DIR}/{filename}.mp3", format="mp3")

    return f"{TMP_DIR}/{filename}.mp3"


@eel.expose
def create_5_jokes(topic):
    """
    A function that creates 5 jokes based on a given topic input.
    The function interacts with DEEPSEEK_CLIENT to generate jokes in the form of setup and punchline.
    It then extracts and formats the jokes into a JSON array containing setup and punchline pairs, and returns the JSON array.
    If an exception occurs during the process, it prints the error message and returns None.
    """
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
    except:
        print(" [ERROR 1]")
        return None


@eel.expose
def play_voice(filename):
    playsound(filename)


@eel.expose
def close_python():
    print(" [PREPARING EXIT]")
    window_app.destroy()
    sys.exit(0)


@eel.expose
def open_folder():
    if os.path.exists(TMP_DIR):
        if os.name == "posix":
            subprocess.run(["xdg-open", TMP_DIR])
        elif os.name == "nt":
            os.startfile(TMP_DIR[2:])
        elif os.name == "mac":
            subprocess.run(["open", TMP_DIR])
        else:
            print("Unsupported operating system.")
    else:
        print("Folder does not exist.")


def start_app():
    eel_thread = threading.Thread(target=eel_start, daemon=True)
    eel_thread.start()
    webview.start(window_app)


def eel_start():
    eel.init("web")
    eel.start(
        "index.html",
        mode=None,
        # mode="default",
        # mode="chrome",
        host="localhost",
        port=27000,
        shutdown_delay=0.0,
    )


if __name__ == "__main__":
    # Dont forget to run "yarn build"
    start_app()
    print(" [EXIT]")

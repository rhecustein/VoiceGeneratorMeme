import os

# Please manually install
# - PyTorch with CUDA -- https://pytorch.org/get-started/locally/
# - GIT SCM -- https://git-scm.com/downloads

print(" [!] Loading dependency...")
try:
    from transformers import AutoProcessor, BarkModel
    import torch
except Exception as e:
    print(" [+] Installing dependency...")
    os.system("pip install git+https://github.com/huggingface/transformers.git")

    try:
        from transformers import AutoProcessor, BarkModel
        import torch
    except:
        print(" [!] Failed to install dependency")
        input(" [!] Error, please check internet connection")
        sys.exit()


os.environ["SUNO_OFFLOAD_CPU"] = "True"
os.environ["SUNO_USE_SMALL_MODELS"] = "True"

OUTPUT_DIR = "./tmp"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def check_device():
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    return device


def main():
    device = check_device()
    print("Loading autoprocessor...")
    processor = AutoProcessor.from_pretrained("suno/bark")
    voice_preset = "v2/en_speaker_9"
    text_prompts = """
         Hello, my name is Serpy. And, uh — and I like pizza. [laughs] 
         But I also have other interests such as playing tic tac toe.
    """

    print("Loading bark model...")
    model = BarkModel.from_pretrained("suno/bark").to(device)

    print("Processing...")
    inputs = processor(text_prompts, voice_preset=voice_preset).to(device)

    print("Generating...")
    audio_array = model.generate(**inputs, pad_token_id=10500)
    audio_array = audio_array.cpu().numpy().squeeze()

    import scipy

    sample_rate = model.generation_config.sample_rate
    scipy.io.wavfile.write(
        f"{OUTPUT_DIR}/bark_out.wav", rate=sample_rate, data=audio_array
    )


if __name__ == "__main__":
    main()

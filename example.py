import time
import traceback

from STTS2Dash.tts import StyleTTS2Pipeline
import torch

if __name__ == '__main__':
    tts = StyleTTS2Pipeline()
    tts.load_from_files("./test_models/....pth",
                        "./test_models/....yml", is_tsukasa=True, precision="fp32")

    # Default parameters
    diffusion_steps = 30
    alpha = 0.0
    beta = 0.0
    embedding_scale = 2
    speed = 0.9
    audio_style_path = "./test_models/n-sample.wav"

    while True:
        text = input("Enter text to synthesize (or 'quit' to exit): ").strip()

        if text.lower() == 'quit':
            break

        if not text:
            print("Text cannot be empty. Please try again.")
            continue

        # Parameter customization
        while True:
            customize = "[custom]" in text

            if customize:
                try:
                    alpha = float(input("Enter alpha (current: {0}): ".format(alpha)) or alpha)
                    beta = float(input("Enter beta (current: {0}): ".format(beta)) or beta)
                    embedding_scale = float(
                        input("Enter embedding scale (current: {0}): ".format(embedding_scale)) or embedding_scale)
                    diffusion_steps = int(
                        input("Enter diffusion steps (current: {0}): ".format(diffusion_steps)) or diffusion_steps)
                    speed = float(
                        input("Enter speed (current: {0}): ".format(speed)) or speed)

                    # New option for audio style path
                    audio_style_path = input(
                        "Enter audio style path (current: {0}): ".format(audio_style_path)) or audio_style_path

                    break
                except ValueError:
                    print("Invalid input. Please enter numeric values for numeric parameters.")
                    continue
            elif not customize:
                break

        # Generate audio
        try:
            start = time.time()
            tts.generate(text,
                         audio_style_path,
                         diffusion_steps=diffusion_steps,
                         alpha=alpha,
                         beta=beta,
                         embedding_scale=embedding_scale,
                         output_file_path="./test.wav",
                         speed=speed,
                         force_espeak_dialect=True,
                         language="en")
            print(f"Done... Saved audio with parameters:")
            print(f"Audio Style Path: {audio_style_path}")
            end = time.time()

            print("took: " + str(end - start))
            print(
                f"Alpha: {alpha}, Beta: {beta}, Embedding Scale: {embedding_scale}, Diffusion Steps: {diffusion_steps}")
        except Exception as e:
            print(f"Error generating audio: {e}")
            traceback.print_exc()

    print("Text-to-speech generation ended.")

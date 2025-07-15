import os
import csv
import sys
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Load Florence-2
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Florence-2-base",
    trust_remote_code=True,
    torch_dtype=dtype
).to(device)

processor = AutoProcessor.from_pretrained(
    "microsoft/Florence-2-base",
    trust_remote_code=True
)

def choose_prompt():
    print("Choose the type of label you want:")
    print("1. Object Description")
    print("2. Light Description")
    print("3. Extensive Description")
    choice = input("Enter 1, 2, or 3: ").strip()
    if choice == "1":
        return "<OD>"
    elif choice == "2":
        return "<DETAILED_CAPTION>"
    elif choice == "3":
        return "<MORE_DETAILED_CAPTION>"
    else:
        print("Invalid choice. Defaulting to Light Description.")
        return "<DETAILED_CAPTION>"

prompt = choose_prompt()

def is_image_file(filename):
    return filename.lower().endswith((".jpg", ".jpeg", ".png"))

def process_image(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, text=prompt, return_tensors="pt").to(device, dtype)

    with torch.no_grad():
        out_ids = model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=512,
            num_beams=3,
        )

    text = processor.batch_decode(out_ids, skip_special_tokens=False)[0]
    return text

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    output_file = "labels.csv"

    with open(output_file, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["file_path", "file_name", "label"])

        for root, _, files in os.walk(folder_path):
            for file in files:
                if is_image_file(file):
                    file_path = os.path.join(root, file)
                    try:
                        label = process_image(file_path)
                        writer.writerow([file_path, file, label])
                        print(f"\n🖼️ {file_path}\n📝 {label}\n")
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")

    print(f"\n✅ All done! Labels saved to {output_file}")

if __name__ == "__main__":
    main()
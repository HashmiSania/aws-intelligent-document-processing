import os
import json
from pathlib import Path
from typing import List, Tuple
import boto3
from tqdm import tqdm

# Initialize AWS Textract client
textract_client = boto3.client("textract")


def get_image_files(folder_path: str) -> List[Path]:
    """
    Scan a folder and return all supported image files.
    """
    valid_extensions = {".jpg", ".jpeg", ".png"}

    image_files = [
        file
        for file in Path(folder_path).iterdir()
        if file.suffix.lower() in valid_extensions
    ]

    return sorted(image_files)


def should_skip_file(image_path: Path, output_folder: Path) -> bool:
    """
    Skip processing if text output already exists.
    """
    txt_path = output_folder / f"{image_path.stem}.txt"
    return txt_path.exists()


def extract_text_from_image(image_path: Path) -> Tuple[str, dict]:
    """
    Send image to Amazon Textract and extract detected text.
    """
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = textract_client.detect_document_text(
        Document={"Bytes": image_bytes}
    )

    extracted_text = "\n".join(
        block["Text"]
        for block in response["Blocks"]
        if block["BlockType"] == "LINE"
    )

    return extracted_text, response


def save_outputs(
    image_path: Path,
    extracted_text: str,
    response: dict,
    output_folder: Path,
):
    """
    Save extracted text and raw JSON response.
    """
    txt_path = output_folder / f"{image_path.stem}.txt"
    json_path = output_folder / f"{image_path.stem}.json"

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    with open(json_path, "w") as f:
        json.dump(response, f, indent=2)

    return txt_path, json_path


def process_single_image(image_path: Path, output_folder: Path) -> bool:
    """
    Process one document image.
    """
    try:

        if should_skip_file(image_path, output_folder):
            print(f"⊘ Skipped: {image_path.name}")
            return False

        print(f"Processing: {image_path.name}")

        extracted_text, response = extract_text_from_image(image_path)

        txt_path, json_path = save_outputs(
            image_path,
            extracted_text,
            response,
            output_folder,
        )

        print(f"✓ Text saved → {txt_path}")
        print(f"✓ JSON saved → {json_path}")

        return True

    except Exception as e:
        print(f"✗ Error processing {image_path.name}: {str(e)}")
        return False


def process_all_images(input_folder: str, output_folder: str):
    """
    Process all images inside the input folder.
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    output_path.mkdir(exist_ok=True)

    image_files = get_image_files(input_folder)

    if not image_files:
        print("No image files found.")
        return

    print(f"Found {len(image_files)} document(s)")

    processed = 0

    for image in tqdm(image_files, desc="Processing documents"):
        success = process_single_image(image, output_path)

        if success:
            processed += 1

    print("\nProcessing complete")
    print(f"Documents processed: {processed}")
    print(f"Documents skipped: {len(image_files) - processed}")


def main():
    """
    Entry point for the document processing pipeline.
    """

    INPUT_FOLDER = "../sample-documents"
    OUTPUT_FOLDER = "../outputs"

    process_all_images(INPUT_FOLDER, OUTPUT_FOLDER)


if __name__ == "__main__":
    main()

import re
import img2pdf
from pathlib import Path
import os
import sys

def jpg_to_pdf(
    input_path: str,
    output_path: str,
    pdf_name: str,
):
    input_path = Path(input_path)
    if output_path == "default":
        output_path = input_path
    else:
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

    # Regular expression to find 2 digits
    regex = r"\d{2}"

    # Supported image extensions
    supported_extensions = (".jpg", ".jpeg", ".png", ".PNG", ".JPG", ".JPEG")

    # Get all subdirectories
    subdirs = [d for d in input_path.iterdir() if d.is_dir()]
    
    if not subdirs:  # If no subdirectories, process current directory
        imgs = []
        for file in input_path.glob("*"):
            if file.suffix in supported_extensions:
                imgs.append(str(file))
        
        if imgs:  # Only create PDF if there are images
            output_file = output_path / f"{pdf_name}.pdf"
            with open(output_file, "wb") as f:  # Open in binary write mode
                f.write(img2pdf.convert(imgs))
    
    else:  # Process each subdirectory
        for dir_path in subdirs:
            match = re.findall(regex, str(dir_path))
            imgs = []
            
            # Walk through the directory
            for file in dir_path.glob("*"):
                if file.suffix in supported_extensions:
                    imgs.append(str(file))
            
            # Sort the images.
            imgs.sort()
            
            if imgs:  # Only create PDF if there are images
                output_file = output_path / f"{pdf_name}_{match[0]}.pdf"
                with open(output_file, "wb") as f:  # Open in binary write mode
                    f.write(img2pdf.convert(imgs))

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description="Converts images to PDF recursively."
    )
    parser.add_argument("input_path", help="Directory containing images or folders that contain images.")
    parser.add_argument("-o", "--output_path", help="Output file path.", default="default")
    parser.add_argument("-n", "--pdf_name", help="Name for the pdf file", default="name")
    return parser.parse_args()

def main():
    try:
        args = parse_args()
        jpg_to_pdf(
            args.input_path,
            args.output_path,
            args.pdf_name,
        )
        return 0
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())

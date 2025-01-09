
# PDF XSS Payload Injection Tool

This tool automates the process of modifying a PDF to inject a custom JavaScript payload for testing purposes. It is designed to assist penetration testers in crafting proof-of-concept exploits for scenarios involving XSS payloads embedded in PDF files.

---

## Features

- Downloads a sample PDF from a specified URL.
- Decodes the PDF to make its structure editable.
- Replaces existing JavaScript within the PDF with a user-provided payload.
- Rebuilds the modified PDF into a valid format.
- Provides an efficient workflow for crafting custom payloads.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Sic4rio/pdf-payload-injection-tool
   cd pdf-payload-injection-tool
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure `qpdf` is installed on your system:
   ```bash
   sudo apt install qpdf
   ```

---

## Usage

1. Run the tool:
   ```bash
   python3 xss.py
   ```

2. Enter your custom JavaScript payload when prompted:
   ```plaintext
   Enter your JavaScript payload (e.g., alert('XSS')): alert('Test Payload');
   ```

3. Upon success, the modified PDF will be saved in the current directory:
   ```plaintext
   Success! Your modified PDF is saved as: final-xss.pdf
   ```

---

## Requirements

- Python 3.x
- `qpdf` (command-line tool)
- Python libraries:
  - `requests`
  - `termcolor`

Install missing libraries using:
```bash
pip install requests termcolor
```

---

## Disclaimer

This tool is intended for educational and authorized penetration testing purposes only. The creator assumes no responsibility for any misuse or damage caused by this tool.

---

## Contributing

Feel free to fork this repository and submit pull requests for improvements or additional features.

---

## License

All rights preserved for my dog. 

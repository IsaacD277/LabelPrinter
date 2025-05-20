# Equipment Sheet Label Printing App

A modern Python application for printing equipment sheet labels using ConnectWise ticket data. The app features a user-friendly GUI built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), supports printer and API key configuration, and prints labels directly to a specified Windows printer.

## Features

- **Modern UI:** Clean, full-screen capable interface with easy navigation.
- **Ticket Lookup:** Fetches ticket and client info from ConnectWise using the API.
- **Device Type Selection:** Supports "Normal" and "Laptop" label templates.
- **Printer Integration:** Sends filled labels directly to a Windows printer.
- **Settings Panel:** Change printer name and API keys (with password protection for sensitive changes).
- **Input History:** Navigate previous ticket numbers with arrow keys.

## Requirements

- ConnectWise
- Python 3.8+
- Windows OS (uses `win32api` for printing)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [python-docx](https://python-docx.readthedocs.io/)
- [Pillow](https://python-pillow.org/)
- [requests](https://docs.python-requests.org/)
- [pywin32](https://github.com/mhammond/pywin32)

## Setup

1. **Clone the repository** and navigate to the project folder.

2. **Install dependencies:**
   ```sh
   pip install customtkinter python-docx pillow requests pywin32
   ```

3. **Configure API Keys:**
   - Rename `config.example.py` to `config.py` and replace the placeholder values with your ConnectWise API credentials and printer name.
   - For help obtaining keys, see comments inside `config.example.py`.

4. **Add Label Templates:**
   - Place your Word templates in the project directory:
     - `ETS EQUIPMENT SHEET TEMPLATE - Normal.docx`
     - `ETS EQUIPMENT SHEET TEMPLATE - Laptop.docx`

## Usage

Run the application:

```sh
python LabelPrinting - Frontend.py
```

- Enter a 7-digit ticket number and select the device type.
- Click **Submit** to print the label.
- Use the **Settings** button to change the printer or API keys.
- Use **Escape** to exit fullscreen.

### Console-Only Version

A console-only version is also available for use without a GUI:

```sh
python "LabelPrinting - Console Version.py"
```

Follow the prompts in the terminal to print labels. Use a capital "L" to specify a laptop label instead of the default label layout. Type "end" to close the program.

## Security

- Changing API keys requires entering the admin password (`etsAdmin` by default; change in code for production).
- Sensitive settings are stored in `config.py` (add this file to `.gitignore`).

## File Structure

- `LabelPrinting - Frontend.py` — Main GUI application.
- `LabelPrinting - Backend.py` — Handles API calls and label generation/printing.
- `config.py` — Stores API credentials and printer name.
- `.gitignore` — Ignores sensitive files like `config.py`.

## Troubleshooting

- **Printing issues:** Ensure the printer name in `config.py` matches your Windows printer.
- **API errors:** Double-check API keys and ConnectWise permissions.
- **Template not found:** Ensure the correct template files are present in the project directory.

## License

This project is for internal use. Contact the project maintainers for licensing information.

---

*For support, contact Isaac D2.*

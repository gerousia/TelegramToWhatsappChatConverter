# Convert Telegram HTML to WhatsApp Chat Format

## Overview

This script converts **Telegram**'s *old* HTML chat exports into **WhatsApp** chat text file format. It processes exported Telegram HTML files to generate a text file that can be imported into WhatsApp.

## Prerequisites

Before running the script, make sure you have the following installed:

1. **Python 3.x**

    Download and install Python from [python.org](https://www.python.org/).

2. **BeautifulSoup4**

    This script uses the `BeautifulSoup` library to parse HTML. Install it using `pip`:
   
    ```bash
    pip install beautifulsoup4
    ```

3. **Exported Telegram HTML files**

    Export your Telegram chat using the desktop application. Make sure you have the HTML files ready.

## Usage

Follow these steps to convert your Telegram HTML chat export into a WhatsApp chat file.

- #### Step 1: Clone the Repository

    Clone this repository local machine:

    ```bash
    git clone https://github.com/gerousia/TelegramToWhatsappChatConverter.git
    cd <repository-directory>
    ```

- #### Step 2: Prepare the HTML Files

    Ensure you have the exported Telegram file(s) located within the repository. These should be named according to the format used by Telegram exports (e.g., messages.html).

- #### Step 3: Run the Script

    Run the script by executing the following command:

    ```bash
    python telegram_chat_converter.py
    ```

#### Command-Line Options

The script accepts several options:

```bash
    -h, --help               
        Show this help message and exit.
    -p <str>, --prefix <str>  
        Specify the Telegram HTML filename prefix. Default is 'messages'.
    -o <str>, --output <str>  
        Specify the output WhatsApp TXT filename. Default is '_chat'.
    -s <int>, --start <int>   
        Specify the starting message index (non-negative integer). Default is 1.
    -e <int>, --end <int>     
        Specify the ending message index (positive integer). Default is MAX (process all messages).
```

#### Example Usage

```bash
python telegram_chat_converter.py -s 1 -e 500
```

- This will convert the Telegram messages from the `messages.html` file (starting from `message.html` to `message500.html`) into a WhatsApp-compatible chat file named `_chat.txt`.

```bash
python telegram_chat_converter.py
```

- This will convert the all the Telegram messages within the directory into a WhatsApp-compatible chat file named `_chat.txt`.

## Disclaimer

I haven't fully tested this.

## Acknowledgements

This project is based on [Transform HTML to WhatsApp Chat Format](https://github.com/Suberbia/html_to_txt) by [Suberbia](https://github.com/Suberbia), which provides the foundational work for converting Telegram HTML chat exports.

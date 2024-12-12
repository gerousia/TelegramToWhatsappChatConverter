# Author: Gerousia
# Date: 2024-12-13
# Description: This script converts Telegram's old exported format HTML messages 
#              into a WhatsApp-compatible text format for import into Telegram.

import argparse
import os
from bs4 import BeautifulSoup

# Define functions
def transform_html_to_whatsapp(html_file, output_file):
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract chat messages
    messages = soup.find_all('div', class_='message')

    # Transform messages to WhatsApp format
    whatsapp_chat = ''
    for message in messages:

        # Determine 'Sender'
        sender_element = message.find('div', class_='from_name')
        if sender_element is not None:
            sender = sender_element.text.strip()
        
        # Determine Date and Time
        timestamp_div = message.find('div', class_="pull_right date details")
        if timestamp_div:
            timestamp = timestamp_div['title']
            date_str = timestamp[:10]
            time_str = timestamp[11:19]
        else:
            date_str, time_str = None, None

        text = ""

        # For Replies
        reply_element = message.find('div', class_='reply_to details')
        reply_message = None

        if reply_element is not None:
            for anchor in reply_element.find_all('a'):
                reply_message = anchor.get('href')
                
                # Cleanup
                # Remove text ('go_to_message') before number of replied message
                _i = reply_message.index("#go_to_message")
                reply_message_id = int(reply_message[_i+14:])
                replied_message_id = int(message.get('id')[7:])

                if reply_message is not None:
                    text += f"In reply to message {reply_message_id - replied_message_id}\n"
                

        # For Text Messages
        text_element = message.find('div', class_='text')
        if text_element is not None:
            text = text_element.text.strip()

        # For Media Messages
        media_element = message.find('div', class_='media_wrap clearfix')
        
        if media_element is not None:
            for anchor in media_element.find_all('a'):
                media_message = anchor.get('href')
                
                if media_message is not None:
                    if 'media_voice_message' in anchor['class']:
                        text = f"[Voice: {media_message}]"
                    elif 'photo_wrap' in anchor['class']:
                        text = f"[Image: {media_message}]"

            # For Stickers
            media_title_element = media_element.find('div', class_='title bold')
            media_description_element = media_element.find('div', class_='description')
            media_status_element = media_element.find('div', class_='status details')

            if media_title_element and media_description_element and media_status_element:
                media_title = media_title_element.text.strip()
                media_description = media_description_element.text.strip()
                media_status = media_status_element.text.strip()
                text = f"Media: {media_title} - {media_description} ({media_status})"
    
        # Format message in WhatsApp format
        if time_str:
            whatsapp_message = f"[{date_str}, {time_str}] {sender}: {text}\n"
            whatsapp_chat += whatsapp_message

    # Append the transformed chat to the output file (_chat.txt)
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(whatsapp_chat)

def process_multiple_html_files(filename, output_file, args):
    i = args.start
    while True:
        if hasattr(args, 'end') and args.end is not None and i > args.end:
            break
        
        html_file = f"{filename}.html" if i == 1 else f"{filename}{i}.html"

        if not os.path.exists(html_file):
            print("Stopping...")
            break  # Stop when the next file doesn't exist

        print(f"Processing {html_file}...")
        transform_html_to_whatsapp(html_file, output_file)
        i += 1

    print(f'Transformation complete. The WhatsApp chat export is saved as {output_file}')

# Usage example
if __name__ == "__main__":
    # Define argument parser
    parser = argparse.ArgumentParser(
                        prog='TelegramHTMLtoWhatsappTXT',
                        description='Converts Telegram\'s exported old-format HTML messages into a WhatsApp-compatible text format for easy import into Telegram.'
                        )

    parser.add_argument('-p', '--prefix', type=str, metavar='<str>', default='messages', help='Specify the Telegram HTML filename prefix. Default \'messages\'.')
    parser.add_argument('-o', '--output', type=str, metavar='<str>',default='_chat', help='Specify the Whatsapp TXT filename output. Default \'_chat\'.')
    parser.add_argument('-s', '--start', type=int, metavar='<int>', default=1, help='Specify the starting count of messages to process (must be a non-negative integer). Default 1.')
    parser.add_argument('-e', '--end', type=int, metavar='<int>', help='Specify the ending count of messages to process (must be a positive integer). Default MAX')

    args = parser.parse_args()

    output_file = f"{args.output}.txt"

    # Remove existing output file to avoid duplication
    if os.path.exists(output_file):
        os.remove(output_file)

    process_multiple_html_files(args.prefix, output_file, args)

    input('Press Enter to Exit')
import re
import pypff
import argparse


def main(directory, arg_year ):
    """
    The main function opens a PST and calls functions to parse and report data from the PST
    :param pst_file: A string representing the path to the PST file to analyze
    :param report_name: Name of the report title (if supplied by the user)
    :return: None
    """
    global emails
    global email_regex
    global year

    year = arg_year
    opst = pypff.open(directory)
    root = opst.get_root_folder()
    emails = set()
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    
    folderTraverse(root)


def folderTraverse(base):
    """
    The folderTraverse function walks through the base of the folder and scans for sub-folders and messages
    :param base: Base folder to scan for new items within the folder.
    :return: None
    """
    for folder in base.sub_folders:
        if folder.number_of_sub_folders:
            folderTraverse(folder) # Call new folder to traverse:
        checkForMessages(folder)


def checkForMessages(folder):
    """
    The checkForMessages function reads folder messages if present and passes them to the report function
    :param folder: pypff.Folder object
    :return: None
    """
    for message in folder.sub_messages:
        if message.creation_time.year >= year:
            processMessage(message)

def processMessage(message):
    """
    The processMessage function processes multi-field messages to simplify collection of information
    :param message: pypff.Message object
    :return: A dictionary with message fields (values) and their data (keys)
    """
    email_props = {
        "subject": "subject",
        "sender":  "sender_name",
        "header":  "transport_headers",
        "body":  "plain_text_body",
        "html_body": "get_html_body"
    }

    item = {}
    for key, val in email_props.items():
        try:
            call = getattr(message, val)
            item[key] = str(call()) if callable(call) else str(call)
        except Exception as e:
            print(f"Skipping {key} due to error: {e}")

    valid_emails = []
    for key in item.keys():
        if item[key] is None:
            continue
        if(key == 'body' and '\\x' in item[key]):
            item[key] = item[key].encode('latin1').decode('unicode_escape').encode('latin1').decode('utf8')
        if item[key] is not None:
            valid_emails += re.findall(email_regex, item[key])

    for email in valid_emails:
        if email not in emails:
            emails.add(email)
    
    return

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Python Exetutable script that loads .OST file and extracts email addresses")

    parser.add_argument("-f", "--file", required=True, help="Path pointing to the .OST file for parsing.")
    parser.add_argument("--year", type=int, required=True, help="Low bound year for emails. Emails before the year defined will be ignored.")

    args = parser.parse_args()

    main(args.file, args.year)
    with open("email_addresses.csv", 'w') as f:
        for email in emails:
            f.write(f"{str(email)};\n")
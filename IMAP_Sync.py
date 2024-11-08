import imapclient
import email
import json
import os
import logging
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.console import Console
from rich.prompt import Confirm
from rich.live import Live
from rich.panel import Panel

# Log configuration
LOG_FILE = 'sync.log'
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Console setup for interactive output
console = Console()

# Load configuration from JSON
def load_config():
    """
    Load the configuration for IMAP sync from 'config.json'.
    
    Returns:
        dict: Configuration data containing 'source' and 'destination' keys with IMAP credentials.
        None: Returns None if there's an error reading the file.
    """
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error reading config file: {e}")
        console.print("[red]Error reading config file.[/red]")
        return None

# Connect to an IMAP server
def connect_to_imap(host, user, password):
    """
    Establish a connection to an IMAP server with the given credentials.
    
    Returns:
        IMAPClient: A connected IMAPClient instance if successful.
        None: Returns None if there's an error during connection or login.
    """
    try:
        server = imapclient.IMAPClient(host, ssl=True)
        server.login(user, password)
        logging.info(f"Connected to {host}")
        return server
    except Exception as e:
        logging.error(f"Error connecting to {host}: {e}")
        console.print(f"[red]Error connecting to {host}[/red]: {e}")
        return None

# List all folders in the mailbox
def list_folders(server):
    """
    Retrieve a list of all folders in the connected IMAP mailbox.
    
    Returns:
        list: A list of folder information tuples.
    """
    try:
        return server.list_folders()
    except Exception as e:
        logging.error(f"Error listing folders: {e}")
        return []

# Get folder statistics (email count and size)
def get_folder_stats(server, folder_name):
    """
    Retrieve statistics for a specified folder, including the email count and total size.
    
    Returns:
        tuple: A tuple containing the total email count and total size in bytes.
    """
    try:
        server.select_folder(folder_name, readonly=True)
        uids = server.search()
        total_emails = len(uids)
        size = sum(len(server.fetch(uid, ['RFC822'])[uid][b'RFC822']) for uid in uids)
        return total_emails, size
    except Exception as e:
        logging.error(f"Error getting stats for folder {folder_name}: {e}")
        return 0, 0

# Display mailbox statistics
def display_mailbox_stats(server, title):
    """
    Display statistics for all folders in a mailbox.
    
    Returns:
        tuple: A tuple containing the total email count and size.
    """
    console.print(f"[cyan]{title}[/cyan]")
    folders = list_folders(server)
    total_emails = 0
    total_size = 0

    if not folders:
        console.print("[red]No folders found.[/red]")
        return 0, 0

    for folder_info in folders:
        folder_name = folder_info[2]
        emails, size = get_folder_stats(server, folder_name)
        total_emails += emails
        total_size += size
        console.print(f"  [green]{folder_name}[/green]: {emails} emails, {size / 1024:.2f} KB")

    console.print(f"\n[bold]Total:[/bold] {total_emails} emails, {total_size / (1024 * 1024):.2f} MB\n")
    return total_emails, total_size

# Create a folder on the destination server if it does not exist
def create_folder_if_not_exists(dest_server, folder_name):
    """
    Ensure that a specified folder exists on the destination server.
    """
    try:
        existing_folders = [folder[2] for folder in dest_server.list_folders()]
        if folder_name not in existing_folders:
            dest_server.create_folder(folder_name)
            logging.info(f"Created folder: {folder_name}")
    except Exception as e:
        logging.error(f"Error creating folder {folder_name}: {e}")

# Sync all emails from one folder to another
def sync_folder(source_server, dest_server, folder_name, progress, task, logs):
    """
    Sync all emails from a source folder to a destination folder.
    """
    try:
        source_server.select_folder(folder_name, readonly=True)
        create_folder_if_not_exists(dest_server, folder_name)
        dest_server.select_folder(folder_name)

        uids = source_server.search()
        total_emails = len(uids)
        logging.info(f"Syncing folder: {folder_name} with {total_emails} emails")
        logs.append(f"Syncing folder: {folder_name} with {total_emails} emails")
        progress.update(task, total=total_emails)

        if total_emails == 0:
            return

        for uid in uids:
            try:
                raw_email = source_server.fetch(uid, ['RFC822'])
                message = raw_email[uid][b'RFC822']
                dest_server.append(folder_name, message)
                progress.advance(task)
                logs.append(f"Synced email UID {uid} in {folder_name}")
            except Exception as e:
                logging.error(f"Failed to sync email UID {uid} in {folder_name}: {e}")
                logs.append(f"[red]Failed to sync email UID {uid}[/red]: {e}")

    except Exception as e:
        logging.error(f"Error syncing folder {folder_name}: {e}")
        logs.append(f"[red]Error syncing folder {folder_name}[/red]: {e}")

# Main function to orchestrate the IMAP synchronization process
def main():
    """
    Main function to execute the IMAP synchronization process.
    """
    console.print(f"[bold magenta]121 Digital IMAP Sync by 121 Digital Services Limited[/bold magenta]\n")

    config = load_config()
    if not config:
        return

    # Connect to source and destination servers
    source_server = connect_to_imap(
        config['source']['host'], config['source']['user'], config['source']['password']
    )
    dest_server = connect_to_imap(
        config['destination']['host'], config['destination']['user'], config['destination']['password']
    )

    if not source_server or not dest_server:
        return

    # Display mailbox statistics and confirm sync
    display_mailbox_stats(source_server, "Source Mailbox Statistics")
    display_mailbox_stats(dest_server, "Destination Mailbox Statistics")
    if not Confirm.ask("Do you want to proceed with syncing?"):
        console.print("[yellow]Sync cancelled.[/yellow]")
        return

    # Start synchronization
    folders = list_folders(source_server)
    logs = []
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        for folder_info in folders:
            folder_name = folder_info[2]
            task = progress.add_task(f"Syncing {folder_name}", start=False)
            sync_folder(source_server, dest_server, folder_name, progress, task, logs)

    console.print("[green]Sync process completed successfully![/green]")

    # Display logs
    if logs:
        console.print(Panel("\n".join(logs), title="Verbose Log"))

    # Cleanup
    source_server.logout()
    dest_server.logout()

if __name__ == "__main__":
    main()

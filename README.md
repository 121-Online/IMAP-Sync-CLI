# 121 Digital IMAP Sync

**121 Digital IMAP Sync** is a tool developed by [121 Digital Services Limited](https://www.121digital.co.uk) to synchronize emails and folders between two IMAP servers. It includes an interactive progress bar, verbose logging, folder creation, and the ability to confirm the sync process before it begins.

## Features

- Syncs emails and folders between source and destination IMAP servers.
- Creates folders on the destination server if they do not exist.
- Provides an interactive progress bar to track the sync process.
- Displays verbose logs to help with troubleshooting and monitoring.
- Asks for confirmation before initiating the sync.
- Handles large mailboxes efficiently.

## Installation

To use **121 Digital IMAP Sync**, ensure that you have Python 3.7+ installed along with the required dependencies. You can install the necessary packages using `pip`:

```bash
pip install imapclient rich
```

## Configuration File

You will need to create a configuration file that contains the IMAP details that are
needed for the sync job. Below is an example config for config.json

```json
{
  "source": {
    "host": "source_imap_host",
    "user": "source_user",
    "password": "source_password"
  },
  "destination": {
    "host": "destination_imap_host",
    "user": "destination_user",
    "password": "destination_password"
  }
}

```

## Example Usage

Execute the script using python:
```bash
python imap_sync.py
```

Example output
```terminal
Starting 121 Digital IMAP Sync...

Loading source mailbox details...
  Source: user@example.com (imap.gmail.com)

Loading destination mailbox details...
  Destination: user@example.com (imap.example.com)

Fetching folder list from source mailbox...
  - Inbox: 1000 emails (2.5MB)
  - Sent: 500 emails (1.2MB)
  - Drafts: 10 emails (50KB)

Fetching folder list from destination mailbox...
  - Inbox: 0 emails (0MB)
  - Sent: 0 emails (0MB)
  - Drafts: 0 emails (0MB)

Confirming sync process:
  Source mailbox: 1500 emails across 3 folders
  Destination mailbox: 0 emails across 3 folders
  Total size: 3.8MB (source) vs. 0MB (destination)

Proceed with sync? (y/n): y

Starting sync...

[====================] 100% - Syncing Inbox (1000 emails)
[====================] 100% - Syncing Sent (500 emails)
[====================] 100% - Syncing Drafts (10 emails)

Sync completed successfully!

Log written to sync.log

```

## Authors

This project was created and maintained by:

- **James Gibbons**  
  Founder & Developer at [121 Digital Services Limited](https://www.121digital.co.uk)  
  Email: [jgibbons@121digital.co.uk](mailto:jgibbons@121digital.co.uk)  
  Twitter: [@jamesgibbons](https://twitter.com/jamesgibbons)

If you have any questions or need further assistance, feel free to reach out to James via email or through the contact information on the [121 Digital website](https://www.121digital.co.uk).

### Contributions

We welcome contributions from the open-source community. If you'd like to contribute to this project, please follow the guidelines provided in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

For any bug reports, feature requests, or other inquiries, please open an issue or contact us directly.


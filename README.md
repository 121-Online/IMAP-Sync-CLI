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

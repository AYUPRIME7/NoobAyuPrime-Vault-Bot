# Telegram File Locker Bot

## Features

- **Private archive imports:** paste a Telegram message link from a linked or explicitly allowed source. The bot checks a bounded sequence of message IDs, forwards media into a separate private archive channel, and catalogs it there. File media is not sent to the owner’s DM; the DM only shows the progress bar and results.
- **Safe pacing:** imports use a one-request-at-a-time queue, a configurable delay, and Telegram `RetryAfter` waits. Bulk delivery groups media where possible and displays progress. Telegram limits still apply; the bot waits for them rather than trying to bypass them.
- **Telegram history limitation:** the Bot API cannot list old channel history. A user must provide a known message link, the bot must have access to the authorized source, and protected or deleted messages may not be importable.
- **Incoming-file queue:** files arrive through one bounded FIFO worker with progress, duplicate/error counts, and resource-aware pacing. Telegram file IDs and metadata are stored in MongoDB rather than file bytes.
- **Section sharing:** existing custom-section sharing remains available, with viewer and editor roles.
- **Videos and Archives sharing:** Premium owners can share their own default Videos and Archives folders with viewer access. A recipient sees shared files in the matching folder, can download them, and cannot edit them. Access ends when the owner's Premium subscription expires or is revoked.
- **Premium payments:** `/premium` sells a recurring 30-day subscription in Telegram Stars. `/terms` shows the service terms and `/paysupport` sends a billing question to the owner. The default price is 100 Stars and can be changed with `PREMIUM_MONTHLY_PRICE_STARS`.

## Required setup

1. Set `BOT_TOKEN` and `MONGO_URI` in Replit Secrets. Do not put credentials in source files or `.env.example`. Rotate any credentials that were previously included in source.
2. Set `OWNER_ID` to the owner’s Telegram numeric user ID.
3. Create a **private Telegram channel** for imported media, add the bot as an administrator with permission to post, and set `IMPORT_ARCHIVE_CHAT_ID` to that channel’s numeric ID.
4. Optionally set `ALLOWED_CHAT_IDS` to a comma-separated list of additional authorized group/channel IDs. Sources linked through `/backup` are also accepted.
5. Set `PREMIUM_MONTHLY_PRICE_STARS` before launch if 100 Stars is not the intended price.

The bot starts without an archive channel, but historical-link imports remain disabled until `IMPORT_ARCHIVE_CHAT_ID` points to a private channel the bot can post to.

## Run

From this directory, install the dependencies and run:

```bash
python -m pip install -r requirements.txt
python main.py
```

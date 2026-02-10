# 🎮 Epic Games Store Free Games Bot
A fully asynchronous Telegram bot that monitors the **Epic Games Store** for free game giveaways 24/7.  
It automatically fetches new offers and broadcasts notifications to subscribed users with game details, images, and promotion dates.

## ✨ Key Features
- 🔄 **Automated Background Parsing**  
  Runs a background service that checks the Epic Games API every hour for new **100% discounted** games.
- 📢 **Instant Notifications**  
  Automatically broadcasts a message to all active subscribers as soon as a new game is found in the database.
- 👤 **Subscription System**  
  Users can subscribe/unsubscribe via inline buttons.  
  The bot remembers users using an SQLite database.
- 🖼️ **Rich Media Messages**  
  Sends beautifully formatted cards with the game cover, description, and **"Free Until"** dates using HTML parsing.
- 🛡️ **Duplicate Prevention**  
  Stores game history in the database to ensure users never receive the same notification twice.
- ⚡ **Asynchronous Architecture**  
  Built with `asyncio` and **aiogram 3**, allowing the bot to handle user interactions and parsing simultaneously without blocking.
  
## 📂 Project Structure
The project follows a modular architecture for better maintainability:

```

epic_games_notifications/
├── app/
│   ├── bot/
│   │   ├── bot_handlers.py    # Telegram command & callback handlers
│   │   └── bot_utils.py       # Helper functions (message formatting)
│   ├── database.py            # SQLite wrapper class
│   ├── loader.py              # Bot, Dispatcher, and DB initialization
│   ├── parser.py              # Logic for fetching & filtering EGS data
│   └── parser_service.py      # Background loop service
├── main.py                    # Entry point
├── games.db                   # SQLite database (auto-generated)
├── .env                       # Environment variables
└── requirements.txt           # Python dependencies

````
## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/merdone/epic-games-bot.git
cd epic-games-bot
````


### 2. Set up a Virtual Environment

Using a virtual environment is recommended.

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```


### 3. Install Dependencies

```bash
pip install -r requirements.txt
```


### 4. Configuration

Create a `.env` file in the project root and add your Telegram Bot Token (get it from **@BotFather**):

```env
BOT_TOKEN=your_telegram_bot_token_here
DB_NAME=games  # Optional, defaults to 'games'
```


### 5. Run the Bot

```bash
python main.py
```

Expected logs:

```
INFO:root:Bot starting...
INFO:root:Parser service started...
```


## ⚙️ How It Works

### Initialization

* `main.py` initializes the **Bot**, **Dispatcher**, and **Database**
* Schedules the `parser_loop` as an asyncio background task

### User Interaction

* `/start`
  Checks if the user exists in the database
  If not — shows a **Subscribe** button

* **Subscribe**

  * Adds the user ID to the `users` table
  * Immediately sends currently active free games

### Parsing Logic

* `parser_service` calls `get_discount_games()`
* Filters Epic Games data by:

  * `discountPercentage == 0`
* Checks the `games` table:

  * If a game is new → saves it
  * Broadcasts the game card to all active users
 

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Bot Framework:** aiogram 3.x
* **Database:** SQLite3
* **HTTP Client:** requests / aiohttp
* **Scheduling:** asyncio

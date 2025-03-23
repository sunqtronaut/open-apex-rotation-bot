# Apex Legends Map Rotation Bot

A Telegram bot that provides the current map rotation schedule for Apex Legends. The bot fetches data from [Apex Legends Status](https://apexlegendsstatus.com) and displays the schedule for both PUBS and RANKED modes.

## Features

- Supports PUBS and RANKED modes.
- Provides a simple `/get <mapname>` command to retrieve schedules.
- Includes a web service for health checks and redirection to the source website.

## How to Use

1. Start the bot in Telegram: [@openapexrotation_bot](https://t.me/openapexrotation_bot).
2. Use the `/start` command to see instructions.
3. Use the `/get <mapname>` command to get the schedule for a specific map  (e.g `/get Kings Canyon`).

## Deployment

This bot is designed to run on [Render.com](https://render.com) or any other platform that supports Python and Flask. It includes a web service for health checks and listens on the required `PORT` environment variable.

### Environment Variables

The following environment variables must be set:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
- `BASE_URL` (optional): The base URL for fetching map rotation data. Default: `https://apexlegendsstatus.com/current-map/battle_royale`.
<!-- - `MAP_NAME` (optional): The default map name. Default: `Kings Canyon`. -->
- `PORT`: The port for the Flask web service (required by Render).

### Running Locally

1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/open-apexrotation.git
  cd open-apexrotation

2. Install dependencies:
  ```bash
  pip install -r requirements.txt

3. Set environment variables:
  ```bash
  export TELEGRAM_BOT_TOKEN=your_telegram_bot_token:xxxxx
  export PORT=5000

4. Run the bot:
  ```bash
  python main-tg.py

### Deploying to Render

1. Create a new **Web Service** on Render:
   - Go to [Render.com](https://render.com).
   - Select "New +" > "Web Service".
   - Connect your GitHub repository.

2. Set the environment variables in the Render dashboard:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
   - `BASE_URL` (optional): The base URL for fetching map rotation data. Default: `https://apexlegendsstatus.com/current-map/battle_royale`.
   - `MAP_NAME` (optional): The default map name. Default: `Kings Canyon`.
   - `PORT`: The port for the Flask web service (Render requires this).

3. Deploy the service:
   - Click "Deploy" and wait for the service to build and start.

## Requirements

The project requires the following Python libraries:

- `Flask`: For the web service.
- `requests`: For fetching map rotation data.
- `beautifulsoup4`: For parsing HTML.
- `python-telegram-bot`: For interacting with the Telegram Bot API.

Install all dependencies using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## File Structure

```
open-apexrotation/
├── main-tg.py          # Main script for the bot and web service
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

Enjoy using the Apex Legends Map Rotation Bot! 🎮

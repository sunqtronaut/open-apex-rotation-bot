You are a Python Architect. Your task is to design and implement a Telegram bot using best practices. The bot should be simple, efficient, and user-friendly. Avoid overengineering and focus on delivering a practical solution. Here are the requirements:

---

### **Requirements**

1. **Bot Functionality:**
   - The bot should fetch and display the current map rotation schedule for the Apex Legends game.
   - The bot should retrieve data from the following URLs:
     - `BASE_URL`: `https://apexlegendsstatus.com/current-map/battle_royale`
     - `PUBS_URL`: `${BASE_URL}/pubs`
     - `RANKED_URL`: `${BASE_URL}/ranked`
   - The bot should parse the HTML from these URLs to extract the schedule for specific maps.

2. **User Interaction:**
   - **Private Chats:**
     - When a user sends the `/start` command, the bot should display a set of buttons for selecting a map.
     - The user should be able to click on a button to select a map, and the bot should respond with the schedule for that map.
   - **Group Chats:**
     - The bot should not send unsolicited messages in group chats.
     - The bot should only respond to commands or button interactions initiated by users.

3. **Map Selection:**
   - The bot should provide buttons for the following maps:
     - Kings Canyon
     - Worlds Edge
     - Broken Moon
     - Olympus
     - Storm Point
     - E-District
   - The user should not need to type map names manually.

4. **Output Format:**
   - The bot should display the schedule in a readable format, including the mode (`PUBS` or `RANKED`), the map name, and the schedule details.

5. **Error Handling:**
   - If the bot fails to fetch data from a URL, it should notify the user with an appropriate error message.
   - If the user selects an invalid map, the bot should display an error message.

6. **Performance:**
   - The bot should handle multiple users simultaneously without performance degradation.
   - The bot should use asynchronous programming to ensure responsiveness.

7. **Deployment:**
   - The bot should be deployable in a standard Python environment.
   - It should use environment variables for sensitive data like the Telegram bot token.

---

### **Technical Details**

1. **Libraries:**
   - Use `python-telegram-bot` for Telegram bot functionality.
   - Use `aiohttp` for asynchronous HTTP requests.
   - Use `BeautifulSoup` from `bs4` for HTML parsing.

2. **Commands:**
   - `/start`: Displays the map selection menu.
   - `/help`: Displays a help message with available commands.
   - `/schedule`: Displays the map selection menu (same as `/start`).

3. **Asynchronous Design:**
   - All network requests and bot interactions should be asynchronous to ensure scalability.

4. **Environment Variables:**
   - Use `TELEGRAM_BOT_TOKEN` for the bot token.
   - Use `BASE_URL` for the base URL of the Apex Legends map rotation site.

5. **Error Messages:**
   - If a URL fetch fails: "Error fetching schedule. Please try again later."
   - If an invalid map is selected: "Invalid map selection. Please choose a valid map."

---

### **Expected Output**

When a user interacts with the bot, the following flow should occur:

1. **Private Chat:**
   - User sends `/start`.
   - Bot displays buttons for map selection.
   - User clicks a button (e.g., "Kings Canyon").
   - Bot responds with the schedule for the selected map:
     ```
     PUBS https://apexlegendsstatus.com/current-map/battle_royale/pubs
     PUBS on Kings Canyon From 21:00 to 22:30, starts in 39 mins
     PUBS on Kings Canyon From 01:30 to 03:00, starts in 5 hours, 9 mins
     ...
     ```

2. **Group Chat:**
   - User sends `/schedule`.
   - Bot displays buttons for map selection.
   - User clicks a button (e.g., "Worlds Edge").
   - Bot responds with the schedule for the selected map.

---

### **Step-by-Step Implementation Plan**

1. **Setup:**
   - Initialize a new Python project.
   - Install required libraries: `python-telegram-bot`, `aiohttp`, `beautifulsoup4`.

2. **Environment Configuration:**
   - Use environment variables for sensitive data (`TELEGRAM_BOT_TOKEN`, `BASE_URL`).

3. **Bot Initialization:**
   - Create a bot instance using `python-telegram-bot`.
   - Define commands (`/start`, `/help`, `/schedule`).

4. **HTML Parsing:**
   - Implement functions to fetch and parse HTML from the URLs.
   - Extract schedule data for specific maps.

5. **Button Interaction:**
   - Use `InlineKeyboardButton` and `InlineKeyboardMarkup` to create interactive buttons.
   - Handle button clicks to fetch and display the schedule.

6. **Error Handling:**
   - Add error handling for network failures and invalid inputs.

7. **Testing:**
   - Test the bot in both private and group chats.
   - Ensure the bot handles multiple users simultaneously.

8. **Deployment:**
   - Deploy the bot in a Python environment.
   - Use Docker if needed for containerization.

---

### **Deliverables**

1. A fully functional Telegram bot that meets the requirements.
2. Clean, well-documented Python code.
3. Instructions for deployment and usage.

---

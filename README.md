---

# Telegram Video Verification Bot

This is a Telegram bot designed for video verification and management. It allows owners to upload, delete, and manage videos while users can verify their membership by sending screenshots.

## Features

- Owner commands for managing verification links and videos.
- User commands for confirming membership and accessing videos.
- Screenshot verification process.
- Video upload and deletion functionality.

## Requirements

- Python 3.7+
- MongoDB
- Telegram Bot Token

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root of the project and add the following variables:
   ```plaintext
   MONGO_URI=<your_mongodb_uri>
   TELEGRAM_TOKEN=<your_telegram_bot_token>
   OWNER_ID=<your_telegram_id>
   VERIFICATION_LINK=<your_verification_link>
   ```

   - `MONGO_URI`: The connection string for your MongoDB database.
   - `TELEGRAM_TOKEN`: The token you received from BotFather.
   - `OWNER_ID`: Your Telegram user ID (you can find it using a bot like @userinfobot).
   - `VERIFICATION_LINK`: The link to the group that users must join for verification.

## Running the Bot

1. **Start the bot**:
   ```bash
   python your_bot_file.py
   ```

2. The bot will run and log its status to the console.

## Usage

### Owner Commands

- **Set Verification Link**: 
  ```
  /set_verification_link <new_link>
  ```

- **Help Command**: 
  ```
  /help
  ```

- **Upload Video**: 
  Use the button provided in the bot.

- **Delete Video**: 
  Use the button provided in the bot.

### User Commands

- **Start Interaction**: 
  ```
  /start
  ```

- **Confirm Membership**: 
  Click the "Konfirmasi Bergabung" button.

- **Send Screenshot**: 
  After confirming membership, send a screenshot of your group membership.

- **List Videos**: 
  Click the "Lihat Video" button to view available videos.

## Deploying the Bot

You can deploy the bot on any server that supports Python. Here's a simple guide using a cloud server like DigitalOcean or AWS.

### Steps to Deploy

1. **Create a Server**: Set up a new cloud server with Ubuntu.

2. **SSH into Your Server**:
   ```bash
   ssh your_user@your_server_ip
   ```

3. **Install Python and Pip** (if not installed):
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

4. **Install MongoDB**:
   Follow the instructions on the [MongoDB installation guide](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/).

5. **Clone the Repository**:
   Follow the same steps as in the installation section.

6. **Set Up Environment Variables**:
   Create a `.env` file as described earlier.

7. **Run the Bot**:
   Start your bot as shown in the running section. You may want to use a tool like `screen` or `tmux` to keep the bot running after you log out:
   ```bash
   sudo apt install screen
   screen
   python your_bot_file.py
   ```

8. **Detaching from Screen**: Press `Ctrl+A`, then `D` to detach.

## Troubleshooting

- **Logs**: Check the console output for any errors.
- **MongoDB Connection**: Ensure your MongoDB URI is correct and accessible from your server.
- **Telegram Bot Issues**: Verify that your bot token is correct and that you are using the bot commands properly.

## License

This project is licensed under the MIT License.

---

Feel free to adjust the instructions and add any additional information you think might be necessary!

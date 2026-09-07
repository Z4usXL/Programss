import requests
import json
import telebot
from telebot import types
import re

# Telegram bot token
BOT_TOKEN = "bot token"

bot = telebot.TeleBot(BOT_TOKEN)

# Instagram API information
IG_AUTHORIZATION = "Instsgram session id "
IG_USER_AGENT = "Instagram 400.0.0.49.68 Android (31/12; 352dpi; 1080x2274; Xiaomi/POCO; M2102J20SG; vayu; qcom; tr_TR; 799297099)"

# Track user states
user_states = {}

def escape_markdown(text):
    """Escape markdown special characters"""
    if not text:
        return ""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', str(text))

def estimate_registration_date(user_id):
    """Estimate registration date based on user ID"""
    if user_id:
        try:
            user_id_int = int(user_id)
            if 1 < user_id_int <= 1278889:
                return "2010"
            elif 1279000 <= user_id_int <= 17750000:
                return "2011"
            elif 17750001 <= user_id_int <= 279760000:
                return "2012"
            elif 279760001 <= user_id_int <= 900990000:
                return "2013"
            elif 900990001 <= user_id_int <= 1629010000:
                return "2014"
            elif 1629010001 <= user_id_int <= 2369359761:
                return "2015"
            elif 2369359762 <= user_id_int <= 4239516754:
                return "2016"
            elif 4239516755 <= user_id_int <= 6345108209:
                return "2017"
            elif 6345108210 <= user_id_int <= 10016232395:
                return "2018"
            elif 10016232396 <= user_id_int <= 27238602159:
                return "2019"
            elif 27238602160 <= user_id_int <= 43464475395:
                return "2020"
            elif 43464475396 <= user_id_int <= 50289297647:
                return "2021"
            elif 50289297648 <= user_id_int <= 57464707082:
                return "2022"
            elif 57464707083 <= user_id_int <= 63313426938:
                return "2023"
            else:
                return "2024 or 2025"
        except:
            return "Unknown"
    return "Unknown"

def get_instagram_user_info(username):
    """Fetch user information from Instagram"""
    try:
        # Search URL
        search_url = "https://graph.instagram.com/api/v1/fbsearch/typeahead_stream/"
        
        # Search parameters
        params = {
            'search_surface': "typeahead_search_page",
            'search_session_id': "aac1fe61-75aa-4826-88ed-66f2d502a9df",
            'count': "30",
            'query': username,
        }
        
        # Request headers
        headers = {
            'Host': "i.instagram.com",
            'User-Agent': IG_USER_AGENT,
            'authorization': IG_AUTHORIZATION,
        }
        
        # Send search request
        response = requests.get(search_url, params=params, headers=headers)
        text = response.text.replace("for (;;);", "")
        data = json.loads(text.split("\n")[0])
        
        # Get user ID from username
        if not data.get("users"):
            return None
            
        user_id = data["users"][0]["pk"]
        
        # Create info_stream URL with ID
        info_url = f"https://i.instagram.com/api/v1/users/{user_id}/info_stream/"
        
        # Send info request as POST
        info_headers = {
            'User-Agent': IG_USER_AGENT,
            'authorization': IG_AUTHORIZATION,
        }
        
        info_response = requests.post(info_url, headers=info_headers)
        
        best_user = None
        
        # Parse each line as JSON and select the most comprehensive user data
        for line in info_response.text.splitlines():
            try:
                data = json.loads(line)
                user = data.get("user")
                if user:
                    if best_user is None or len(user.keys()) > len(best_user.keys()):
                        best_user = user
            except:
                pass
        
        return best_user
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def format_user_info(user):
    """Format user information"""
    if not user:
        return "❌ User not found!"
    
    # Secure values
    username = escape_markdown(user.get("username", "Unknown"))
    full_name = escape_markdown(user.get("full_name", "Unknown"))
    user_id = escape_markdown(user.get("id", "Unknown"))
    biography = escape_markdown(user.get("biography", "No biography"))
    
    # Check private account
    is_private = "🔒 Yes" if user.get("is_private") else "🔓 No"
    is_verified = "✅ Yes" if user.get("is_verified") else "❌ No"
    is_business = "💼 Yes" if user.get("is_business") else "❌ No"
    
    # Estimate registration date
    reg_date = estimate_registration_date(user.get("id"))
    
    # Format information (using HTML)
    message = f"""
📱 <b>Instagram User Information</b>

👤 <b>Username:</b> @{username}
📝 <b>Name:</b> {full_name}
🆔 <b>ID:</b> {user_id}
📅 <b>Date:</b> {reg_date}

📊 <b>Statistics:</b>
👥 <b>Followers:</b> {user.get("follower_count", 0):,}
👣 <b>Following:</b> {user.get("following_count", 0):,}
📸 <b>Posts:</b> {user.get("media_count", 0):,}

🔍 <b>Account Information:</b>
🔒 <b>Private Account:</b> {is_private}
✅ <b>Verified:</b> {is_verified}
💼 <b>Business Account:</b> {is_business}

📄 <b>Biography:</b>
{biography}
"""
    
    return message

def create_copy_keyboard_for_info(user_info):
    """Create keyboard for user information"""
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # Copy button
    copy_button = types.InlineKeyboardButton(
        "📋 Copy", 
        callback_data="copy_info"
    )
    
    # Profile link button
    profile_url = f"https://instagram.com/{user_info.get('username', '')}"
    profile_button = types.InlineKeyboardButton(
        "🔗 Profile", 
        url=profile_url
    )
    
    # Refresh button
    refresh_button = types.InlineKeyboardButton(
        "🔄 Refresh", 
        callback_data=f"refresh_{user_info.get('username', '')}"
    )
    
    keyboard.add(copy_button)
    keyboard.add(profile_button, refresh_button)
    
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Welcome message and ask for username"""
    user_states[message.chat.id] = "waiting_for_username"
    
    welcome_text = """
👋 <b>Welcome to Instagram User Info Bot!</b>

Please enter the Instagram username you want to query.

📝 <b>Example:</b> <code>instagram</code> or <code>@instagram</code>
"""
    
    bot.reply_to(message, welcome_text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """Handle callback queries"""
    
    if call.data == "copy_info":
        # Create copyable text
        try:
            # Get last message text
            message_text = call.message.caption if call.message.caption else call.message.text
            if message_text:
                # Clean HTML tags
                clean_text = re.sub(r'<[^>]+>', '', message_text)
                
                # Send copyable format message
                bot.send_message(
                    call.message.chat.id,
                    f"<code>{clean_text}</code>",
                    parse_mode='HTML'
                )
                bot.answer_callback_query(call.id, "📋 Copyable format sent!")
        except Exception as e:
            bot.answer_callback_query(call.id, "❌ Copy error!")
    
    elif call.data.startswith("refresh_"):
        username = call.data.replace("refresh_", "")
        bot.answer_callback_query(call.id, "🔄 Refreshing...")
        
        # Fetch user information again
        user_info = get_instagram_user_info(username)
        
        if user_info:
            formatted_info = format_user_info(user_info)
            keyboard = create_copy_keyboard_for_info(user_info)
            
            # Update with profile picture if available
            profile_pic = user_info.get("profile_pic_url")
            if profile_pic:
                try:
                    bot.edit_message_media(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        media=types.InputMediaPhoto(profile_pic, caption=formatted_info, parse_mode='HTML'),
                        reply_markup=keyboard
                    )
                except:
                    bot.edit_message_text(
                        formatted_info,
                        call.message.chat.id,
                        call.message.message_id,
                        parse_mode='HTML',
                        reply_markup=keyboard
                    )
            else:
                bot.edit_message_text(
                    formatted_info,
                    call.message.chat.id,
                    call.message.message_id,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )

@bot.message_handler(func=lambda message: True)
def handle_username(message):
    """Handle username query"""
    # Clean username
    username = message.text.strip()
    
    # Remove @ symbol
    if username.startswith('@'):
        username = username[1:]
    
    # Check if empty
    if not username:
        bot.reply_to(message, "❌ Please enter a username!", parse_mode='HTML')
        return
    
    # Processing message
    processing_msg = bot.reply_to(message, f"🔍 Searching for @{username}...", parse_mode='HTML')
    
    # Fetch user information
    user_info = get_instagram_user_info(username)
    
    if user_info:
        # Format and send information
        formatted_info = format_user_info(user_info)
        keyboard = create_copy_keyboard_for_info(user_info)
        
        # Send with profile picture if available
        profile_pic = user_info.get("profile_pic_url")
        if profile_pic:
            try:
                bot.send_photo(
                    message.chat.id,
                    profile_pic,
                    caption=formatted_info,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Photo sending error: {e}")
                # Send only text if photo fails
                bot.reply_to(
                    message, 
                    formatted_info, 
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
        else:
            bot.reply_to(
                message, 
                formatted_info, 
                parse_mode='HTML',
                reply_markup=keyboard
            )
        
        # Delete processing message
        try:
            bot.delete_message(message.chat.id, processing_msg.message_id)
        except:
            pass
    else:
        # Error message with keyboard
        keyboard = types.InlineKeyboardMarkup()
        retry_button = types.InlineKeyboardButton("🔄 Try Again", callback_data=f"refresh_{username}")
        keyboard.add(retry_button)
        
        try:
            bot.edit_message_text(
                "❌ User not found or an error occurred!",
                message.chat.id,
                processing_msg.message_id,
                reply_markup=keyboard
            )
        except:
            bot.reply_to(message, "❌ User not found or an error occurred!")

# Start bot
if __name__ == "__main__":
    print("🤖 Bot starting...")
    print("Bot is active! Send /start on Telegram.")
    bot.polling(none_stop=True)
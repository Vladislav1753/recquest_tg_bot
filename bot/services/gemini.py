import google.generativeai as genai
import logging
from bot.data.constants import GEMINI_API_KEY


gemini_chat = None

async def setup_gemini():
    """Initialize and configure the model when the bot starts."""
    global gemini_chat
    genai.configure(api_key=GEMINI_API_KEY)


    model = genai.GenerativeModel("gemini-2.0-flash")

    # Start a chat session with predefined instructions
    gemini_chat = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "You are an assistant that recommends movies, TV shows, games, books, and anime. "
                    "You should always provide up to 5 recommendations and avoid using markdown. "
                    "Your responses should be relatively brief. "
                    "Format: "
                    "1. Recommendation Title - short review and some reasons it's similar to what the user sent. "
                    "2. Recommendation Title - short review and some reasons it's similar to what the user sent. "
                    "... and so on."
                ]
            }
        ]
    )
    print("Gemini initialized!")


async def get_gemini_recommendations(category, query, previous_recommendations=None):
    """Fetch recommendations from the pre-configured model, avoiding previous recommendations."""
    try:
        if gemini_chat is None:
            await setup_gemini()  # Initialize if not already set up

        # Create prompt with instruction to avoid previous recommendations
        prompt = f"{category}: {query}"
        if previous_recommendations and len(previous_recommendations) > 0:
            avoid_list = ", ".join(previous_recommendations)
            prompt += f"\nPlease provide 5 new recommendations that are NOT in this list: {avoid_list}"

        response = gemini_chat.send_message(prompt)

        if not response or not hasattr(response, "text") or not response.text.strip():
            return ["No recommendations found."]

        recommendations = [rec.strip() for rec in response.text.split("\n") if rec.strip()]
        return recommendations[:5] if recommendations else ["No recommendations found."]

    except Exception as e:
        logging.error(f"Error getting recommendations: {e}")
        return ["Sorry, I couldn't generate recommendations at the moment."]
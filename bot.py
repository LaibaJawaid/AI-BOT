# bot.py (Updated with Message Splitting Logic)

import discord
from discord.ext import commands
import asyncio 

from config import DISCORD_TOKEN
from retrieval import perform_rag_retrieval

# --- Discord Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Prints a message when the bot successfully connects to Discord."""
    print(f'Bot connected as {bot.user} (ID: {bot.user.id})')

@bot.command(name='azwaj')
async def azwaj_query(ctx, *, users_query: str):
    """Handles the RAG query for Ummul Momineen (Azwaj)."""
    
    async with ctx.typing():
        try:
            # Run RAG process in executor
            final_response = await bot.loop.run_in_executor(
                None, 
                perform_rag_retrieval, 
                users_query
            )
        except Exception as e:
            print(f"An unexpected error occurred during RAG process: {e}")
            final_response = "An internal error occurred while trying to process your request."
        
        # === START OF NEW LOGIC TO HANDLE 2000 CHARACTER LIMIT ===
        MAX_CHARS = 2000
        response_text = final_response

        if len(response_text) > MAX_CHARS:
            # Split the long response into chunks of max 2000 characters
            # We use a simple method here, but for perfect paragraph/line breaks, 
            # more complex logic (like discord.utils.fill_in_chunks) is needed.
            chunks = [response_text[i:i + MAX_CHARS] for i in range(0, len(response_text), MAX_CHARS)]
            
            # Send each chunk separately
            for i, chunk in enumerate(chunks):
                if i == 0:
                    # Add a header to the first chunk
                    await ctx.send(f"**[Detailed Response - Part 1/{len(chunks)}]**\n{chunk}")
                else:
                    await ctx.send(f"**[Part {i+1}/{len(chunks)}]**\n{chunk}")
        else:
            # Send the response normally
            await ctx.send(response_text)
        # === END OF NEW LOGIC ===

if __name__ == "__main__":
    if DISCORD_TOKEN:
        print("Starting bot...")
        bot.run(DISCORD_TOKEN)
    else:
        print("Error: DISCORD_TOKEN not found in .env file. Please check config.py and .env.")

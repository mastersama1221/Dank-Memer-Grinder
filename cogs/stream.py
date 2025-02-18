import asyncio
import re

from discord.ext import commands

Games = {
    "apex legends": 0,
    "call of duty": 1,
    "csgo": 2,
    "dead by daylight": 3,
    "destiny 2": 4,
    "dota 2": 5,
    "elden ring": 6,
    "escape from tarkov": 7,
    "fifa 22": 8,
    "fortnite": 9,
    "grand theft auto v": 10,
    "hearthstone": 11,
    "just chatting": 12,
    "league of legends": 13,
    "lost ark": 14,
    "minecraft": 15,
    "music": 16,
    "pubg": 17,
    "rainbow six siege": 18,
    "rocket league": 19,
    "rust": 20,
    "teamfight Tactics": 21,
    "valorant": 22,
    "world of tanks": 23,
    "world of warcraft": 24,
}


class Stream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.channel.id != self.bot.channel_id
            or self.bot.config_dict[self.bot.account_id]["state"] is False
            or self.bot.config_dict[self.bot.account_id]["commands"]["stream"] is False
        ):
            return

        for embed in message.embeds:
            # Get trending game
            try:
                if embed.to_dict()["title"] == "Trending Game":
                    global game
                    game = Games[
                        (
                            re.search(
                                "\*\*(.*?)\*\*", embed.to_dict()["description"]
                            ).group(1)
                        )
                        .title()
                        .lower()
                    ]
            except KeyError:
                pass

            # Go live
            try:
                if embed.to_dict()["fields"][1]["name"] == "Last Live":
                    await self.bot.click(message, 0, 0)

                    # Get trending game
                    async for cmd in self.bot.channel.slash_commands(
                        command_ids=[967369106301026344]
                    ):
                        await cmd()
                        break
                    await asyncio.sleep(4)

                    # Select trending game
                    await self.bot.select(message, 0, 0, game)
                    await asyncio.sleep(0.7)
                    await self.bot.click(message, 1, 0)
                    await asyncio.sleep(0.7)
                    await self.bot.click(message, 0, 1)
            except (KeyError, IndexError):
                pass

            # Read chat
            try:
                if embed.to_dict()["fields"][1]["name"] == "Live Since":
                    await self.bot.click(message, 0, 1)
            except (KeyError, IndexError):
                pass


async def setup(bot):
    await bot.add_cog(Stream(bot))

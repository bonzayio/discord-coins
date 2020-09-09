import os
import discord
import json


class Helper:
    def __init__(self):
        if not os.path.isfile('configuration/config.json'):
            print('[ERROR] Couldn\'t locate the aws.json file. Exitting.')
            exit()
        with open('configuration/config.json', 'r') as json_file:
            data = json.load(json_file)

        self.command_channel_id = data["command_channel_id"]

        self.success_channel_id = data["success_channel_id"]

        self.verified_role_id = data["verified_role_id"]

        self.twitter_mention = data["twitter_mention"]

        self.salute_emoji_name = data["salute_emoji_name"]

        self.coins_for_tweet = int(data["coins_for_tweet"])
        self.coins_for_picture = int(data["coins_for_picture"])


        embed_settings = data["embed_settings"]
        self.color = embed_settings["color"]
        self.footer = embed_settings["footer"]
        self.icon = embed_settings["icon"]

    def get_success_channel_id(self) -> int:
        return self.success_channel_id

    def get_commands_channel_id(self) -> int:
        return self.command_channel_id

    def get_verified_role_id(self) -> int:
        return self.verified_role_id

    def get_twitter_mention(self) -> str:
        return self.twitter_mention

    def get_salute_emoji_name(self) -> str:
        return self.salute_emoji_name

    def get_coins_for_tweet(self) -> str:
        return self.coins_for_tweet
        
    def get_coins_for_picture(self) -> str:
        return self.coins_for_picture

    def initialize_embed(self, title: str = None) -> discord.Embed:
        """Initializes an embed with the config specified in `config.json` file.

        Args:
            title (str, optional): Title of the embed. Defaults to None.

        Returns:
            discord.Embed: The embed object.
        """

        embed = discord.Embed(
            title=title,
            color=self.color,
        )
        embed.set_footer(text=self.footer, icon_url=self.icon)

        return embed

import io
import logging
from pathlib import Path

import discord.ext.commands as commands
import discord
from adultnea.client import AdultClient, Context
from PIL import Image, ImageSequence, ImagePalette


@commands.command(aliases=['pat'])
async def patpat(ctx: Context, user: discord.User, speed: int = 100):
    patpat = Image.open((Path(__file__).parent / 'patpatempty.gif'))
    avatar_bytes = await user.avatar.read()
    with io.BytesIO(avatar_bytes) as avatar_fp:
        avatar = Image.open(avatar_fp)

        frame_avatar_positions = [
            (32, 102, 73, 65),
            (32, 112, 73, 47),
        ]

        frames = []
        for frame_idx in range(patpat.n_frames):
            frame = Image.new('RGBA', patpat.size)
            frames.append(frame)
            patpat.seek(frame_idx)
            x, y, w, h = frame_avatar_positions[frame_idx]
            fitted_avatar = avatar.copy().resize((w, h), Image.Resampling.BICUBIC)
            frame.paste(fitted_avatar, (x, y, x + w, y + h))
            patpat_frame = patpat.convert('RGBA')
            frame.paste(patpat_frame, (0, 0), patpat_frame)

        with io.BytesIO() as output_file:
            frames[0].save(output_file, 'WEBP', duration=speed,
                           loop=0, optimize=False,
                           save_all=True,
                           append_images=frames[1:]
                           )
            output_file.seek(0)
            await ctx.followup(f'Patting {user.name}',
                               attachments=[discord.File(output_file, "hardcorepattingaction.webp")])


async def setup(bot: AdultClient):
    bot.add_command(patpat)

# -*- coding: utf-8 -*-
import os
import asyncio
import discord
from discord.ext import commands
import tools.codm_parsers

LANG = 'ru' #ru - for russian, en - for english, use that for global language settings
lang_list = ['ru', 'ру', 'en', 'eng'] #список для проверки языка / list for language checks
PREFIX = '*' # задаем префикс / set prefix

#TOKEN = os.getenv("DISCORD_TOKEN") #строка для запуска на Heroku / string for Heroku launch
#TOKEN = "DISCORD_TOKEN" #строка для запуска где-то, кроме Heroku / string for launch not on the Heroku
TOKEN = "ODI2MTc4ODcyNTc0NzM4NDUy.YGItCA.NB2Js5Ar5vtVcmvRfJ0Ohtz0AwY" 

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents) #задаем префикс бота и разрешения для работы / setting prefix and intents
version = 'v0.1'
#bot.remove_command("help") #удаляем дефолтный help от библиотеки discord.py

@bot.event #запуск бота / bot launching
async def on_ready():
    if LANG == 'ru':
        print('Вошёл как')
    elif LANG == 'en':
        print('Login as')
    print(bot.user.name)
    print(bot.user.id)
    print(version)
    print('------')
    await bot.change_presence(activity=discord.Game(name=PREFIX + "help"))

@bot.command(pass_context=True, aliases=["Info", "инфо", "Инфо"])
async def info(ctx, *, weapon: str = None):

    if weapon is None:
        if LANG == 'ru':
            await ctx.send(embed = discord.Embed(description = "Введите название оружия!", color = 0x00ff00))
            return
        elif LANG == 'en':
            await ctx.send(embed = discord.Embed(description = "Enter the weapon name!", color = 0x00ff00))
            return
  
    result = await tools.codm_parsers.weapon_parser(weapon.lower(), LANG)

    if result is None:
        if LANG == 'ru':
            await ctx.send(embed = discord.Embed(description = "Не получилось найти оружие! Попробуйте убрать пробел или кавычки в названии оружия.", color = 0x00ff00))
            return
        elif LANG == 'en':
            await ctx.send(embed = discord.Embed(description = "I can't found weapon! Remove spaces and quotes in weapon name.", color = 0x00ff00))
            return

    if LANG == 'ru':
        embed = discord.Embed(title = "Информация о " + result[0], color = 0x00ff00)
        embed.set_image(url=result[10])
        embed.add_field(name="Тип:", value=result[1], inline=False)
        embed.add_field(name="Описание:", value=result[2], inline=False)
        embed.add_field(name="Характеристики:", value=f'Урон: {str(result[4])}\nТочность: {str(result[5])}\nДистанция: {str(result[6])}\nТемп стрельбы: {str(result[7])}\nПодвижность: {str(result[8])}\nКонтроль: {str(result[9])}', inline=False)
        embed.set_footer(text=f'Изменения: {result[3]}')
        await ctx.send(embed=embed)
        print('Обработал info о', weapon, 'для пользователя', ctx.author.name)
    elif LANG == 'en':
        embed = discord.Embed(title = "Information about " + result[0], color = 0x00ff00)
        embed.set_image(url=result[10])
        embed.add_field(name="Type:", value=result[1], inline=False)
        embed.add_field(name="Description:", value=result[2], inline=False)
        embed.add_field(name="Stats:", value=f'Damage: {str(result[4])}\nAccuracy: {str(result[5])}\nRange: {str(result[6])}\nFire Rate: {str(result[7])}\nMobility: {str(result[8])}\nControl: {str(result[9])}', inline=False)
        embed.set_footer(text=f'Changes: {result[3]}')
        await ctx.send(embed=embed)
        print('Give info for', weapon, 'for user', ctx.author.name)

@bot.command(pass_context=True, aliases=["Compare", "сравни", "Сравни"])
async def compare(ctx, weapon1: str = None, weapon2: str = None):

    if weapon1 is None or weapon2 is None:
        if LANG == 'ru':
            await ctx.send(embed = discord.Embed(description = "Введите название оружия!", color = 0x00ff00))
            return
        elif LANG == 'en':
            await ctx.send(embed = discord.Embed(description = "Enter the weapon name!", color = 0x00ff00))
            return
  
    result1 = await tools.codm_parsers.weapon_parser(weapon1.lower(), LANG)
    result2 = await tools.codm_parsers.weapon_parser(weapon2.lower(), LANG)

    if result1 is None or result2 is None:
        if LANG == 'ru':
            await ctx.send(embed = discord.Embed(description = "Не получилось найти оружие! Попробуйте убрать пробел или кавычки в названии оружия.", color = 0x00ff00))
            return
        elif LANG == 'en':
            await ctx.send(embed = discord.Embed(description = "I can't found weapon! Remove spaces and quotes in weapon name.", color = 0x00ff00))
            return

    if LANG == 'ru':
        embed = discord.Embed(title = f"Сравнение {result1[0]} и {result2[0]}", color = 0x00ff00)
        embed.set_image(url=result1[10])
        embed.set_thumbnail(url=result2[10])
        embed.add_field(name="Тип:", value=f"{result1[1]} / {result2[1]}", inline=False)
        embed.add_field(name="Описание:", value=f"{result1[2]} / {result2[2]}", inline=False)
        embed.add_field(name="Характеристики:", value=f'Урон: {str(result1[4])} / {str(result2[4])}\nТочность: {str(result1[5])} / {str(result2[5])}\nДистанция: {str(result1[6])} / {str(result2[6])}\nТемп стрельбы: {str(result1[7])} / {str(result2[7])}\nПодвижность: {str(result1[8])} / {str(result2[8])}\nКонтроль: {str(result1[9])} / {str(result2[9])}', inline=False)
        embed.set_footer(text=f'Изменения: {result1[3]} / {result2[3]}')
        await ctx.send(embed=embed)
        print('Обработал сравнение о', weapon1, 'и', weapon2, 'для пользователя', ctx.author.name)
    elif LANG == 'en':
        embed = discord.Embed(title = f"Compare {result1[0]} and {result2[0]}", color = 0x00ff00)
        embed.set_image(url=result1[10])
        embed.set_thumbnail(url=result2[10])
        embed.add_field(name="Type:", value=f"{result1[1]} / {result2[1]}", inline=False)
        embed.add_field(name="Description:", value=f"{result1[2]} / {result2[2]}", inline=False)
        embed.add_field(name="Stats:", value=f'Damage: {str(result1[4])} / {str(result2[4])}\nAccuracy: {str(result1[5])} / {str(result2[5])}\nRange: {str(result1[6])} / {str(result2[6])}\nFire Rate: {str(result1[7])} / {str(result2[7])}\nMobility: {str(result1[8])} / {str(result2[8])}\nControl: {str(result1[9])} / {str(result2[9])}', inline=False)
        embed.set_footer(text=f'Changes: {result1[3]} / {result2[3]}')
        await ctx.send(embed=embed)
        print('Give compare for', weapon1, 'and', weapon2, 'for user', ctx.author.name)

@bot.command(aliases=["мета", "Meta", "Мета"])
async def meta(ctx):
  
    result = await tools.codm_parsers.meta_parser()

    if LANG == 'ru':
        embed = discord.Embed(title = 'Мета-отчёт', color = 0x00ff00)
        embed.add_field(name=f"Тир {result[2]}:", value=result[3], inline=False)
        embed.add_field(name=f"Тир {result[4]}:", value=result[5], inline=False)
        embed.add_field(name=f"Тир {result[6]}:", value=result[7], inline=False)
        embed.add_field(name=f"Тир {result[8]}:", value=result[9], inline=False)
        await ctx.send(embed=embed)
        print('Обработал meta для пользователя', ctx.author.name)
    elif LANG == 'en':
        embed = discord.Embed(title = 'Meta-report:', color = 0x00ff00)
        embed.add_field(name=f"Tier {result[2]}:", value=result[3], inline=False)
        embed.add_field(name=f"Tier {result[4]}:", value=result[5], inline=False)
        embed.add_field(name=f"Tier {result[6]}:", value=result[7], inline=False)
        embed.add_field(name=f"Tier {result[8]}:", value=result[9], inline=False)
        await ctx.send(embed=embed)
        print('Give meta for user', ctx.author.name)

bot.run(TOKEN)
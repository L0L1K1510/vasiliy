import discord
from discord.ext import commands

from random import randint

import json
import asyncio

class Levels(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.bot.loop.create_task(self.save_users())

		with open(r'/home/maxlol98765/git/vasiliy/cogs/users.json', 'r') as f:
			self.users = json.load(f)

	@commands.Cog.listener()
	async def save_users(self):
		await self.bot.wait_until_ready()
		while not self.bot.is_closed():
			with open(r'/home/maxlol98765/git/vasiliy/cogs/users.json', 'w') as f:
				json.dump(self.users, f, indent=4)

			await asyncio.sleep(5)




	def lvl_up(self, author_id):
		cur_xp = self.users[author_id]['exp']
		cur_lvl = self.users[author_id]['level']

		if cur_xp >= round(4*(cur_lvl**3)/5):
			self.users[author_id]['level'] += 1
			self.users[author_id]['money'] += self.users[author_id]['level']*5
			return True

		else:
			return False



	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user:
			return

		author_id = str(message.author.id)

		if not author_id in self.users:
			self.users[author_id] = {}
			self.users[author_id]['level'] = 1
			self.users[author_id]['exp'] = 0
			self.users[author_id]['money'] = 0

		self.users[author_id]['exp'] += 1

		if self.lvl_up(author_id):
			await message.channel.send(f"{message.author.mention} получил {self.users[author_id]['level']} уровень и {self.users[author_id]['level']*5} пивных крышек!")

	@commands.command()
	async def level(self, ctx, member: discord.Member = None):
		member = ctx.author if not member else member
		member_id = str(member.id)

		if not member_id in self.users:
			await ctx.send('Пользователь не имеет никакого уровня.')
		else:
			embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

			embed.set_author(name=f'Уровень - {member}', icon_url=self.bot.user.avatar_url)

			embed.add_field(name='Уровень', value=self.users[member_id]['level'])
			embed.add_field(name='Опыт', value=self.users[member_id]['exp'])
			embed.add_field(name='Пивные крышки', value=self.users[member_id]['money'])

			await ctx.send(embed=embed)

	@commands.command()
	async def giverole(self, ctx, member: discord.Member = None):
		member = ctx.author if not member else member
		member_id = str(member.id)

		if not member_id in self.users:
			await ctx.send('***Пользователь не имеет никакого уровня.***')
		else:
			if self.users[member_id]['level'] == 30:
				role = discord.utils.get(member.guild.roles, name='Bro')
				await member.add_roles(role)
				await ctx.send(f'{member}, достигший 30 уровня, получает роль Bro!')
			elif self.users[member_id]['level'] == 20:
				role = discord.utils.get(member.guild.roles, name='Mating on Sundays')
				await member.add_roles(role)
				await ctx.send(f'{member}, достигший 20 уровня, получает роль Mating on Sundays!')
			elif self.users[member_id]['level'] == 10:
				role = discord.utils.get(member.guild.roles, name='Do not Pussy')
				r_role = discord.utils.get(member.guild.roles, name='Pussy')
				await member.add_roles(role)
				await member.remove_roles(r_role)
				await ctx.send(f'{member}, достигший 10 уровня, получает роль Do not Pussy!')
			elif self.users[member_id]['level'] < 10:
				await ctx.send('***Повышайте уровень, чтобы получать роли!***')

	@commands.command()
	async def diceup(self, message, amount: int):
		N = int(amount)
		author_id = str(message.author.id)
		roll = randint(0, 100)

		if roll > 50:
			self.users[author_id]['money'] += N
			await message.channel.send(f"❖{roll}❖ {message.author.mention} выиграл в Dice {N*2} пивные(-ых) крышки(-ек)! ☉{self.users[author_id]['money']}☉")
		elif roll == 50:
			self.users[author_id]['money'] += N*9
			await message.channel.send(f"❖{roll}❖ {message.author.mention} получил особый приз в {N*10} пивные(-ых) крышки(-ек)! ☉{self.users[author_id]['money']}☉")
		elif roll < 50:
			self.users[author_id]['money'] -= N
			await message.channel.send(f"❖{roll}❖ {message.author.mention} проиграл в Dice {N} пивные(-ых) крышки(-ек)! ☉{self.users[author_id]['money']}☉")

	@commands.command()
	async def dicedown(self, message, amount: int):
		N = int(amount)
		author_id = str(message.author.id)
		roll = randint(0, 100)

		if roll < 50:
			self.users[author_id]['money'] += N
			await message.channel.send(f"❖{roll}❖ {message.author.mention} выиграл в Dice {N*2} пивные(-ых) крышки(-ек)! ☉{self.users[author_id]['money']}☉")
		elif roll == 50:
			self.users[author_id]['money'] += N*9
			await message.channel.send(f"❖{roll}❖ {message.author.mention} получил особый приз в {N*10} пивные(-ых) крышки(-ек)! ☉{self.users[author_id]['money']}☉")
		elif roll > 50:
			self.users[author_id]['money'] -= N
			await message.channel.send(f"❖{roll}❖ {message.author.mention} проиграл в Dice {N} пивные(-ых) крышки(-ек)! ☉{self.users[author_id]['money']}☉")

	#@commands.command()
	#async def buy1(self, ctx, member):
		#member_id = str(member.id)
		#if self.users[member_id]['money'] >= 250:
			#role = discord.utils.get(member.guild.roles, name='Майнкрафт моя жызнь')
			#await member.add_roles(role)
		#else:
			#await ctx.send('Недостаточно крышек для покупки!')


	@commands.Cog.listener()
	@diceup.error
	async def diceup_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Неверно введена команда (!diceup N)!***')
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Неверно введена команда (!diceup N)!***')
		if isinstance(error,commands.BadFrgument):
			await ctx.send('***Неверно введена команда (!diceup N)!***')

	@commands.Cog.listener()
	@dicedown.error
	async def dicedown_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Неверно введена команда (!dicedown N)!***')
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Неверно введена команда (!dicedown N)!***')
		if isinstance(error,commands.BadFrgument):
			await ctx.send('***Неверно введена команда (!dicedown N)!***')

	#@commands.Cog.listener()
	#@buy.error
	#async def buy_error(self, ctx, error):
		#if isinstance(error, commands.CheckFailure):
			#await ctx.send('***Неверно введена команда (!buy index)!***')
		#if isinstance(error, commands.MissingRequiredArgument):
			#await ctx.send('***Неверно введена команда (!buy index)!***')
		#if isinstance(error,commands.BadFrgument):
			#await ctx.send('***Неверно введена команда (!buy index)!***')
			





def setup(bot):
	bot.add_cog(Levels(bot))
		
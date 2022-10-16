import discord
from discord import errors, File, Message, Embed, TextChannel
from discord.ext.tasks import loop
from discord.ext import commands
import os
import json
from keep_alive import keep_alive
from PIL import Image, ImageDraw, ImageFont
import io
from twitch import get_notifications, get_app_acess_token
import random
import requests 
from datetime import datetime, date

client = commands.Bot(command_prefix='!')
client.remove_command("help")

with open("config.json") as config_file:
  config=json.load(config_file)

with open("strimers.json") as strimers_file:
  strimers=json.load(strimers_file)

with open("chulos.json") as chulos_file:
  chulos=json.load(chulos_file)  

@client.event
async def on_ready():
  print('Chismestrum sta en linea')
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="sus caritas preciosas"))


@loop(seconds=100)
async def check_twitch_online_streamers():
  chnl = client.get_channel(892472599228084315)
  notifi=[]
  if not chnl:
    return
  

  with open("config.json") as config_file:
    config=json.load(config_file)


  notifications = get_notifications()
  with open("strimers.json") as strimers_file:
    strimers=json.load(strimers_file)

  for notification in notifications:
    embed=discord.Embed(url="https://www.twitch.tv/{}".format(notification["user_login"]),title=notification["title"],description="{} sta enbibo en Tuich".format(notification["user_login"]), color=discord.Colour.from_rgb(204, 152, 197))
    imgstrim=notification["thumbnail_url"]
    img_strim=imgstrim.replace("{width}","400")
    imagenstrim=img_strim.replace("{height}","225")
    embed.set_image(url=imagenstrim)
    embed.add_field(name="Playing",value=notification["game_name"], inline=True)
    embed.set_thumbnail(url=notification["foto_juego"])
    embed.set_footer(icon_url="https://www.iconheaven.com/download/63/png/twitch_logo_png512.png", text="El Tuich")
    embed.set_author(icon_url=notification["foto_perfil"],name=notification["user_login"])
    
    if notification["user_login"] in strimers:
      cuantos=len(strimers[notification["user_login"]])
      if cuantos == 0:
        pass
      else:
        rango=range(0,cuantos)
        for i in rango:
          b=strimers[notification["user_login"]][i]
          ba=str(b)
          a="<@!"+ba+">"
          notifi.append(a)
        final=" ".join(notifi)
        await chnl.send(final+" - {} inicio strim :  https://www.twitch.tv/{}".format(notification["user_login"],notification["user_login"]),embed=embed)
      
    else:   
      await chnl.send("@everyone - {} inicio strim :  https://www.twitch.tv/{}".format(notification["user_login"],notification["user_login"]),embed=embed)
      
if __name__ == "__main__":
  check_twitch_online_streamers.start()
  

@client.command()
async def kiss(ctx,member: discord.Member):
  apikey = "LIVDSRZULELA"  # test value
  lmt = 250

  # our test search
  search_term = "anime kiss gif"
  pos = '0'
  pos2 = '50'
  pos3 = '100'

  # get the top 8 GIFs for the search term
  r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s&pos=%s" % (search_term, apikey, lmt, pos))
  r2 = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s&pos=%s" % (search_term, apikey, lmt, pos2))
  r3 = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s&pos=%s" % (search_term, apikey, lmt, pos3))

  if r.status_code == 200:
    # load the GIFs using the urls for the smaller GIF sizes
    busqueda = json.loads(r.text)
    busqueda2 = json.loads(r2.text)
    busqueda3 = json.loads(r3.text)
    ds = [busqueda, busqueda2, busqueda3]
    d = {}
    for k in busqueda.keys():
      d[k] = tuple(d[k] for d in ds)
    indice=random.randint(0, 2)
    numero=random.randint(0, 49)
    gif=d['results'][indice][numero]['media'][0]['gif']['url']

  else:
    busqueda = None
  
  embed=discord.Embed(description=ctx.author.mention + " le ha dado besito a "+ member.mention, color=discord.Colour.from_rgb(204, 152, 197))
  embed.set_image(url=gif)
  await ctx.send(embed=embed)

@client.command()
async def hug(ctx,member: discord.Member):
  apikey = "LIVDSRZULELA"  # test value
  lmt = 250

  # our test search
  search_term = "anime hug gif"
  pos = '0'
  pos2 = '50'
  pos3 = '100'

  # get the top 8 GIFs for the search term
  r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s&pos=%s" % (search_term, apikey, lmt, pos))
  r2 = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s&pos=%s" % (search_term, apikey, lmt, pos2))
  r3 = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s&pos=%s" % (search_term, apikey, lmt, pos3))

  if r.status_code == 200:
    # load the GIFs using the urls for the smaller GIF sizes
    busqueda = json.loads(r.text)
    busqueda2 = json.loads(r2.text)
    busqueda3 = json.loads(r3.text)
    ds = [busqueda, busqueda2, busqueda3]
    d = {}
    for k in busqueda.keys():
      d[k] = tuple(d[k] for d in ds)
    indice=random.randint(0, 2)
    numero=random.randint(0, 49)
    gif=d['results'][indice][numero]['media'][0]['gif']['url']

  else:
    busqueda = None
  
  embed=discord.Embed(description=ctx.author.mention + " le ha dado abracito a "+ member.mention, color=discord.Colour.from_rgb(204, 152, 197))
  embed.set_image(url=gif)
  await ctx.send(embed=embed)

@client.command()
async def cat(ctx):
  r = requests.get("https://api.thecatapi.com/v1/images/search")

  if r.status_code == 200:
    busqueda = json.loads(r.content)
    gif=busqueda[0]['url']
  else:
    busqueda = None

  embed=discord.Embed(color=discord.Colour.from_rgb(204, 152, 197))
  embed.set_image(url=gif)
  await ctx.send(embed=embed)
  
@client.command()
async def dog(ctx):
  r = requests.get("https://api.thedogapi.com/v1/images/search")

  if r.status_code == 200:
    busqueda = json.loads(r.content)
    gif=busqueda[0]['url']
  else:
    busqueda = None

  embed=discord.Embed(color=discord.Colour.from_rgb(204, 152, 197))
  embed.set_image(url=gif)
  await ctx.send(embed=embed)

@client.command()
async def sub(ctx):
  add = ctx.message.content
  split=add.split()
  words=len(split)
  if words == 2:
    
   texto=split[1]
   if texto == 'add':
    uid = ctx.author.id
    uuid=str(uid)
    if uuid == "727384087714857050":
      await ctx.send("Naambre " + ctx.author.mention + " tu no te puedes regalar subs")
    else:
      now = datetime.now()
      timestamp =datetime.timestamp(now)
      chulos[uuid][1]=timestamp
      await ctx.send(ctx.author.mention + " agregaste una sub regalada por <@!727384087714857050> ")
  elif words == 1:
    uid = ctx.author.id
    uuid=str(uid)
    if uuid == "727384087714857050":
      await ctx.send("Naambre " + ctx.author.mention + " tu no te puedes regalar subs")
    else:
      fechag=chulos[uuid][1]
      if fechag == "":
        await ctx.send(ctx.author.mention + " <@!727384087714857050> no te ha regalado ninguna sub")
      else:
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        fechaok = int(fechag)
        min = fechaok           #removing milli seconds
        max = timestamp
        min = datetime.fromtimestamp(min)
        max = datetime.fromtimestamp(max)
        diferencia=str((max-min).days)
        await ctx.send(ctx.author.mention + " han pasado " +diferencia+" días sin que <@!727384087714857050> te regale una sub")

@client.command()
async def strimer(ctx):
  with open("config.json") as config_file:
    config=json.load(config_file)

  with open("strimers.json") as strimers_file:
    strimers=json.load(strimers_file)
    
  add=ctx.message.content
  split=add.split()
  func=split[1]
  try:
      strimer=split[2].lower()
  except IndexError:
      strimer=""    

  userid=ctx.author.id
  test = config['watchlist']
  if (strimer == 'hpavel82') or (strimer == 'sicaac') or (strimer == 'marf0n') or (strimer == 'tiranodiego') or (strimer == 'deividaam'):
    await ctx.send(ctx.author.mention + "el papucho que intentas agregar ya esta en la lista general")
  else:
    if func == 'add':
      if strimer in strimers:
        if userid in strimers[strimer]:
          await ctx.send(ctx.author.mention + " ya habias registrao a este usario en tus notificaciones")
        else:
          strimers[strimer].append(userid)
          nstrimer=strimers
          with open("strimers.json", "w") as strimers_file:
            json.dump(nstrimer, strimers_file)
          await ctx.send(ctx.author.mention + " searegistrao a "+strimer+ " en tus notificaciones")
      else:
        strimers[strimer]=[userid]
        nstrimer=strimers
        with open("strimers.json", "w") as strimers_file:
          json.dump(nstrimer, strimers_file)

        await ctx.send(ctx.author.mention + " searegistrao a  "+strimer+ " en tus notificaciones")
      
    elif func == 'del':
      if strimer in strimers:
        if userid in strimers[strimer]:
          strimers[strimer].remove(userid)
          with open("strimers.json", "w") as strimers_file:
            json.dump(strimers, strimers_file)

          await ctx.send(ctx.author.mention + " eliminaste a "+strimer+ " de tus notificaciones")

        else:
          await ctx.send(ctx.author.mention + strimer + " no esta registrao en tus notificaciones")
      else:
        await ctx.send(ctx.author.mention + " este strimer no esta registrao en la lista de notificaciones")
    elif func == 'list':
      embed=discord.Embed(title="Strimers registrados",description=ctx.author.mention + ' acá esta tu lista: ',color=discord.Colour.from_rgb(204, 152, 197))
      key_list = list(strimers.keys())
      val_list = list(strimers.values())
      list_strimers=[]
      for i in range(0,len(key_list)):
        valor = val_list[i]
        if userid in valor:
          strimer = key_list[i]
          list_strimers.append(strimer)
      cantstrimers=len(list_strimers)
      if cantstrimers == 0:
        await ctx.author.send('No tienes strimers registrados')
      else:
        lista_final = ' | '.join(list_strimers)
        embed.add_field(name = chr(173), value=lista_final, inline=False)
        await ctx.author.send(embed=embed)

  if strimer in test:
    pass
  else:
    if strimer == "":
      pass
    else:
      test.append(strimer)
      nuevo={'watchlist':test}
      with open("config.json", "w") as config_file:
        json.dump(nuevo, config_file)




@client.command()
async def help(ctx):
  embed=discord.Embed(title="Comandos de Chismestrum",description="aca sta la lista",color=discord.Colour.from_rgb(204, 152, 197))
  embed.add_field(name="Rocket League", value="Comandos de rokelij",inline=False)
  embed.add_field(name="!rank",value="Muestra tus rangos en listas competitvas de rokelij, si quieren ver el rango de otro usuario escriban: __**!rank plataforma usuario**__ , ejemplo de comando: __**!rank epic chismestrum**__", inline=False)
  
  embed.add_field(name="Twitch", value="Comandos de tuich",inline=False)
  embed.add_field(name="!strimer add usuario",value="Agrega al usuario de tuich a tus notificaciones, ejemplo de comando: __**!strimer add chismestrum**__", inline=True)
  embed.add_field(name="!strimer del usuario",value="Elimina al usuario de tuich de tus notificaciones, ejemplo de comando: __**!strimer del chismestrum**__", inline=True)
  embed.add_field(name="!strimer list",value="Para ver la lista de strimers que has puesto en tus notificaciones", inline=True)

  embed.add_field(name="Amorts", value="Comandos de besitos, abracitos, gatitos y perritos ",inline=False)
  embed.add_field(name="!kiss",value="Manda un gif random de besito a la persona que quieras, ejemplo de comando: __**!kiss @chismestrum**__", inline=True)
  embed.add_field(name="!hug",value="Manda un gif random de abracito a la persona que quieras, ejemplo de comando: __**!hug @chismestrum**__", inline=True)
  embed.add_field(name="!dog o !cat",value="Muestra una imagen random de perrito o de gatito", inline=True)

  embed.add_field(name="!sub", value="Comando para saber cuantos días han pasado desde que sicaac te ha regalado una sub, para agregar la fecha en la que sicaac te regale una sub utiliza el comando __**!sub add**__",inline=False)

  await ctx.author.send(embed=embed)

client.run(os.environ['TOKEN'])

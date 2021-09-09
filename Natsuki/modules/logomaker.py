from Natsuki.events import register
from Natsuki import OWNER_ID
from Natsuki import telethn as tbot
import os 
from PIL import Image, ImageDraw, ImageFont
import shutil 
import random, re
import glob
import time
from telethon.tl.types import InputMessagesFilterPhotos


FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

#Add telegraph media links of profile pics that are to be used
TELEGRAPH_MEDIA_LINKS = ["https://telegra.ph/file/e354ce72d5cc6a1d27c4d.jpg", 
                         "https://telegra.ph/file/8f9ff3d743e6707a61489.jpg", 
                         "https://telegra.ph/file/bfc97f4abc4bec6fe860d.jpg", 
                         "https://telegra.ph/file/5ef0f060023600ec08c19.jpg",
                         "https://telegra.ph/file/a448465a3a8a251170f76.jpg",
                         "https://telegra.ph/file/eb0ac1557668a98a38cb6.jpg", 
                         "https://telegra.ph/file/fdb3691a17a2c91fbe76c.jpg", 
                         "https://telegra.ph/file/ccdf69ebf6cb85c52a25b.jpg",
                         "https://telegra.ph/file/2adffc55ac0c9733ecc7f.jpg", 
                         "https://telegra.ph/file/faca3b435da33f2f156f1.jpg", 
                         "https://telegra.ph/file/93d0a48c31e16f036f0e8.jpg", 
                         "https://telegra.ph/file/9ed89dc742b172a779312.jpg",
                         "https://telegra.ph/file/0b4c19a19fb834d922d66.jpg", 
                         "https://telegra.ph/file/a95a0deb86f642129b067.jpg", 
                         "https://telegra.ph/file/c4c3d8b5cfc3cc5040833.jpg", 
                         "https://telegra.ph/file/1e1a1b52b9a313e066a04.jpg",
                         "https://telegra.ph/file/a582950a8a259efdcbbc0.jpg",
                         "https://telegra.ph/file/9c3a784d45790b193ca36.jpg", 
                         "https://telegra.ph/file/6aa74b17ae4e7dc46116f.jpg", 
                         "https://telegra.ph/file/e63cf624d1b68a5c819b6.jpg",
                         "https://telegra.ph/file/7e420ad5995952ba1c262.jpg",
                         "https://telegra.ph/file/c7a4dc3d2a9a422c19723.jpg", 
                         "https://telegra.ph/file/163c7eba56fd2e8c266e4.jpg", 
                         "https://telegra.ph/file/5c87b63ae326b5c3cd713.jpg",
                         "https://telegra.ph/file/344ca22b35868c0a7661d.jpg", 
                         "https://telegra.ph/file/a0ef3e56f558f04a876aa.jpg", 
                         "https://telegra.ph/file/217b997ad9b5af8b269d0.jpg", 
                         "https://telegra.ph/file/b3595f99b221c56a5679b.jpg",
                         "https://telegra.ph/file/aba7f4b4485c5aae53c52.jpg", 
                         "https://telegra.ph/file/209ca51dba6c0f1fba85f.jpg", 
                         "https://telegra.ph/file/2a0505ee2630bd6d7acca.jpg", 
                         "https://telegra.ph/file/d193d4191012f4aafd4d2.jpg",
                         "https://telegra.ph/file/47e2d151984bd54a5d947.jpg",
                         "https://telegra.ph/file/2a6c735b47db947b44599.jpg", 
                         "https://telegra.ph/file/7567774412fb76ceba95c.jpg", 
                         "https://telegra.ph/file/6dd8b0edec92b24985e13.jpg",
                         "https://telegra.ph/file/dcf5e16cc344f1c030469.jpg",
                         "https://telegra.ph/file/0718be0bd52a2eb7e36aa.jpg", 
                         "https://telegra.ph/file/0d7fcb82603b5db683890.jpg", 
                         "https://telegra.ph/file/44595caa95717f4db4788.jpg",
                         "https://telegra.ph/file/f3a063d884d0dcde437e3.jpg", 
                         "https://telegra.ph/file/733425275da19cbed0822.jpg", 
                         "https://telegra.ph/file/aff5223e1aa29f212a46a.jpg", 
                         "https://telegra.ph/file/45ccfa3ef878bea9cfc02.jpg",
                         "https://telegra.ph/file/a38aa50d009835177ac16.jpg", 
                         "https://telegra.ph/file/53e25b1b06f411ec051f0.jpg", 
                         "https://telegra.ph/file/96e801400487d0a120715.jpg", 
                         "https://telegra.ph/file/6ae8e799f2acc837e27eb.jpg",
                         "https://telegra.ph/file/265ff1cebbb7042bfb5a7.jpg",
                         "https://telegra.ph/file/4c8c9cd0751eab99600c9.jpg", 
                         "https://telegra.ph/file/1c6a5cd6d82f92c646c0f.jpg", 
                         "https://telegra.ph/file/2c1056c91c8f37fea838a.jpg",
                         "https://telegra.ph/file/f140c121d03dfcaf4e951.jpg", 
                         "https://telegra.ph/file/39f7b5d1d7a3487f6ba69.jpg"
                         ]

@register(pattern="^/logo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo...wait!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./Natsuki/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "gold"
    shadowcolor = "blue"
    font = ImageFont.truetype("./Natsuki/resources/Chopsic.otf", 330)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="yellow")
    fname2 = "NatsukiLogo.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Made By @TheNatsukiBot ⚡️")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Go to Help From  @NatsukiSupport_Official, {e}')

@register(pattern="^/biglogo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo...wait!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./Natsuki/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "gold"
    shadowcolor = "blue"
    font = ImageFont.truetype("./Natsuki/resources/Chopsic.otf", 950)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="yellow")
    fname2 = "NatsukiLogo.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Made By @TheNatsukiBot ⚡️")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Go to Help From  @NatsukiSupport_Official, {e}')


@register(pattern="^/wlogo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo...wait!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./Natsuki/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "blue"
    font = ImageFont.truetype("./Natsuki/resources/Maghrib.ttf", 1000)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="white", stroke_width=0, stroke_fill="white")
    fname2 = "NatsukiLogo.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Made By @TheNatsukiBot")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Go to Help From  @NatsukiSupport_Official, {e}')

@register(pattern="^/daalogo ?(.*)")
async def logo_gen(event):
    xx = await eor(event, get_string("com_1"))
    name = event.pattern_match.group(1)
    if not name:
        await eod(xx, "`Give a name too!`")
    bg_, font_ = "", ""
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            if hasattr(temp.media, "document"):
                if "font" in temp.file.mime_type:
                    font_ = await temp.download_media()
                elif (".ttf" in temp.file.name) or (".otf" in temp.file.name):
                    font_ = await temp.download_media()
            elif "pic" in mediainfo(temp.media):
                bg_ = await temp.download_media()
    else:
        pics = []
        async for i in event.client.iter_messages(
            "@UltroidLogos", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download_media()
        fpath_ = glob.glob("Natsuki/resources/*")
        font_ = random.choice(fpath_)
    if not bg_:
        pics = []
        async for i in event.client.iter_messages(
            "@UltroidLogos", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download_media()
    if not font_:
        fpath_ = glob.glob("Natsuki/resources/*")
        font_ = random.choice(fpath_)
    if len(name) <= 8:
        fnt_size = 150
        strke = 10
    elif len(name) >= 9:
        fnt_size = 50
        strke = 5
    else:
        fnt_size = 130
        strke = 20
    img = Image.open(bg_)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_, fnt_size)
    w, h = draw.textsize(name, font=font)
    h += int(h * 0.21)
    image_width, image_height = img.size
    draw.text(
        ((image_width - w) / 2, (image_height - h) / 2),
        name,
        font=font,
        fill=(255, 255, 255),
    )
    x = (image_width - w) / 2
    y = (image_height - h) / 2
    draw.text(
        (x, y), name, font=font, fill="white", stroke_width=strke, stroke_fill="black"
    )
    flnme = f"ultd.png"
    img.save(flnme, "png")
    await xx.edit("`Done!`")
    if os.path.exists(flnme):
        await event.client.send_file(
            event.chat_id,
            file=flnme,
            caption=f"Logo by Natsuki",
            force_document=True,
        )
        os.remove(flnme)
        await xx.delete()
    if os.path.exists(bg_):
        os.remove(bg_)
    if os.path.exists(font_):
        if not font_.startswith("Natsuki/resources/"):
            os.remove(font_)    
 

@register(pattern="^/redlogo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo...wait!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./Natsuki/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "gold"
    shadowcolor = "blue"
    font = ImageFont.truetype("./Natsuki/resources/Chopsic.otf", 330)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="red")
    fname2 = "NatsukiLogo.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Made By @TheNatsukiBot ⚡️")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Go to Help From  @NatsukiSupport_Official, {e}')
  

@register(pattern="^/pandalogo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo...wait!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./Natsuki/resources/pandabg.png')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 25
    fillcolor = "gold"
    shadowcolor = "blue"
    font = ImageFont.truetype("./Natsuki/resources/font.otf", 170)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="yellow")
    fname2 = "NatsukirLogo.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Made By @TheNatsukiBot ⚡️")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Go to Help From  @NatsukiSupport_Official, {e}')
  

@register(pattern="^/spiderlogo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo...wait!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./Natsuki/resources/spiderbg.png')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 25
    fillcolor = "gold"
    shadowcolor = "blue"
    font = ImageFont.truetype("./Natsuki/resources/font.otf", 170)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="yellow")
    fname2 = "NatsukiLogo.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Made By @TheNatsukiBot ⚡️")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Go to Help From  @NatsukiSupport_Official, {e}')  
  
  
  
@register(pattern="^/spidermanlogo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo...wait!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./Natsuki/resources/spiderbg (2).png')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 25
    fillcolor = "gold"
    shadowcolor = "blue"
    font = ImageFont.truetype("./Natsuki/resources/font.otf", 170)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="yellow")
    fname2 = "NatsukiLogo.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Made By @TheNatsukiBot ⚡️")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Go to Help From  @NatsukiSupport_Official, {e}')  
  
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")


__help__ = """
 ❍ /logo text :  Create your logo with your name
 ❍ /biglogo text :  Create your logo Bigger Than `logo`
 ❍ /wlogo text : Create your logo with your name
 ❍ /redlogo text : Create your logo with your name
 ❍ /pandalogo text : Create your logo with your name
 ❍ /spiderlogo text : Create your logo with your name
 ❍ /spidermanlogo text : Create your logo with your name
 """
__mod_name__ = "Logo Maker"

""" MIUI Updates messages generator """
from telethon import Button

from uranus_bot.providers.miui_updates_tracker.miui_updates_tracker import get_miui
from uranus_bot.utils.miui import get_region, get_type, get_branch
from uranus_bot.telegram_bot.tg_bot import LOCALIZE
from uranus_bot import XFU_WEBSITE


async def miui_message(device, updates, codenames_names, locale):
    """ Generate telegram message of recovery/fasboot command """
    data = await get_miui(device, updates)
    rom_type = LOCALIZE.get_text(locale, await get_type(str(data)))
    message = "**" + LOCALIZE.get_text(locale, "miui_message").replace(
        "{codenames_names[device]}", codenames_names[device]).replace(
        "{device}", device).replace(
        "{rom_type}", rom_type) + "**"
    buttons = []
    for i in data:
        version = i['version']
        android = i['android']
        download = i['download']
        region = LOCALIZE.get_text(locale, await get_region(
            download.split('/')[-1], i['codename'], version))
        buttons.append([Button.url(f"{region} {version} | {android}", url=download)])
    buttons.append([Button.url(LOCALIZE.get_text(locale, "roms_archive"),
                               url=f"{XFU_WEBSITE}/archive/miui/{device}/"),
                    Button.url(LOCALIZE.get_text(locale, "MIUIUpdatesTracker"),
                               url="https://t.me/MIUIUpdatesTracker")])
    return message, buttons


async def miui_inline(event, device, updates, codenames_names, locale):
    """ Generate telegram result of recovery/fasboot inline query """
    builder = event.builder
    message, buttons = await miui_message(device, updates, codenames_names, locale)
    result = builder.article(
        LOCALIZE.get_text(locale, "miui_inline").replace(
            "{codenames_names[device]}", codenames_names[device]
        ).replace("{device}", device),
        text=message, buttons=buttons,
        link_preview=False
    )
    return result


async def archive_message(device, codenames_names, locale):
    """ Generate telegram message of archive command """
    message = LOCALIZE.get_text(locale, "miui_archive").replace(
        "{codenames_names[device]}", codenames_names[device]).replace("{device}", device)
    buttons = [
        [Button.url(LOCALIZE.get_text(locale, "roms_archive"),
                    url=f"{XFU_WEBSITE}/archive/miui/{device}/"),
         Button.url(LOCALIZE.get_text(locale, "MIUIUpdatesTracker"),
                    url="https://t.me/MIUIUpdatesTracker")]
    ]
    return message, buttons


async def archive_inline(event, device, codenames_names, locale):
    """ Generate telegram result of archive inline query """
    builder = event.builder
    message, buttons = await archive_message(device, codenames_names, locale)
    result = builder.article(
        LOCALIZE.get_text(locale, "archive_inline").replace(
            "{codenames_names[device]}", codenames_names[device]
        ).replace("{device}", device),
        text=message,
        buttons=buttons, link_preview=False
    )
    return result


async def latest_miui_message(device, updates, codenames_names, locale):
    """ Generate telegram message for latest command """
    data = await get_miui(device, updates)
    message = LOCALIZE.get_text(locale, "latest_message").replace(
        "{codenames_names[device]}", codenames_names[device]).replace(
        "{device}", device) + ":\n"
    for i in data:
        version = i['version']
        download = i['download']
        filename = download.split('/')[-1]
        branch = LOCALIZE.get_text(locale, await get_branch(version))
        region = LOCALIZE.get_text(locale, await get_region(filename, i['codename'], version))
        message += f"{region} {branch}: `{version}`\n"
    return message


async def latest_miui_inline(event, device, updates, codenames_names, locale):
    """ Generate telegram result of latest inline query """
    builder = event.builder
    message = await latest_miui_message(device, updates, codenames_names, locale)
    result = builder.article(
        LOCALIZE.get_text(locale, "latest_inline").replace(
            "{codenames_names[device]}", codenames_names[device]).replace(
            "{device}", device), text=message)
    return result


async def miui_update_message(data, codenames_names, locale):
    """ Generate telegram message of miui update """
    rom_type = LOCALIZE.get_text(locale, await get_type(str(data)))
    device = data['codename']
    region = LOCALIZE.get_text(locale,
                               await get_region(data['filename'], device, data['version']))
    message = LOCALIZE.get_text(locale, "miui_update").replace(
        "{device}", device).replace(
        "{codenames_names[device]}", codenames_names[device]).replace(
        "{rom_type}", rom_type) + f"**{LOCALIZE.get_text(locale, 'Region')}:** {region} \n" \
                                  f"**{LOCALIZE.get_text(locale, 'Size')}**: {data['size']}"
    buttons = [Button.url(f"{data['version']} | {data['android']}", url=data['download'])]
    return message, buttons


async def wrong_codename_message(locale):
    """ Generate wrong codename message"""
    return "**" + LOCALIZE.get_text(locale, "wrong_codename") + "**"


async def subscribed_message(sub_type, device, locale):
    """ Generate subscribed message"""
    return "**" + LOCALIZE.get_text(locale, "subscribed").replace(
        "{device}", device).replace("{sub_type}", sub_type) + "**"


async def already_subscribed_message(sub_type, device, locale):
    """ Generate already subscribed message"""
    return "**" + LOCALIZE.get_text(locale, "already_subscribed").replace(
        "{device}", device).replace("{sub_type}", sub_type) + "**"


async def unsubscribed_message(sub_type, device, locale):
    """ Generate unsubscribed message"""
    return "**" + LOCALIZE.get_text(locale, "unsubscribed").replace(
        "{device}", device).replace("{sub_type}", sub_type) + "**"


async def subscriptions_message(subscriptions, locale):
    """ Generate subscriptions message"""
    message = f"**" + LOCALIZE.get_text(locale, "your_subscriptions") + ":**\n"
    if subscriptions:
        for subscription in subscriptions:
            message += f"{subscription[1]} ({subscription[0]})"
    else:
        message = f"**{LOCALIZE.get_text(locale, 'no_subscriptions')}**"
    return message

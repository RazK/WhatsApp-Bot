# WhatsApp-Bot

An experimental WhatsApp bot for the sake of humanity and for humor.

## Demo

<img src="docs/whatsapp-bot-demo.gif" alt="WhatsApp Bot Preview"/>

## Usage

The bot is currently live and available on
<a href="tel:12513091793">+1 (251) 309-1793</a>. <br>
Send him a WhatsApp message!

### Features

You can type any message with the following words, and the bot will respond accordingly.<br>
Check [app.py](app.py) for a full list of supported words.

* <b>Horse</b> - The bot will fetch a horse image from https://generatorfun.com and send it back.
* <b>Cat</b> - The bot will fetch a cat image from https://cataas.com/cat and send it back.
* <b>Quote</b> - The bot will fetch a quote from https://api.quotable.io/random and send it back.

## System Overview

This bot has multiple components that are working together:

* <b>Phone Number</b> - a [phone number](tel:12513091793) approved by WhatsApp for sending and recieving messages.
  I bought an American phone number for roughly $4 through Twillio, and had to fill an approval request form in order
  for WhatsApp to enable it on their apps. <br>
  This took a couple of days to process.
* <b>WhatsApp Sender</b> - a [Twillio](https://www.twilio.com/messaging/whatsapp) account for routing messages incoming
  on my phone number to a [webhook](https://stingray-app-vrsol.ondigitalocean.app/bot) I configured.
  That webhook forwards WhatsApp messages to my Flask server.
* <b>Flask Server</b> -
  a [DigitalOcean](https://cloud.digitalocean.com/apps/eb865ebf-ebfd-46e3-9ad2-b1590569b0bf/overview) server
  running [app.py](app.py) on a public facing URL. This server gets updated whenever a new commit is pushed to the main branch. 

## Resources

* Building a WhatsApp bot with Python and Twillio - https://www.geeksforgeeks.org/building-whatsapp-bot-on-python/
* MP4 to GIF - https://ezgif.com/video-to-gif/
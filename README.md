# Discord Suggestion / Proposal System Bot

## About the Bot:
**With this Bot you can add a Proposal / Suggestion System to your Discord Server.**

For that you need to create **3** Channels in your Discord Server.


### Discord Textchannels:

| Channels  | Description |
| ------------- | ------------- |
| 1. Suggestion/Proposal Channel  | **Visible**: All Users <br> The users can write their suggestion/proposals in here.|
| 2. Queue Channel  | **Visible**: Staff Member <br> All written messages from the 1st Channel will get in here <br> The staff can `Accept` or `Decline` the suggestions / proposals |
| 3. Accepted Suggestions Channel | **Visible**: -- <br> You can set this channel according to your needs, depending on what this system is used for.|

### How does it look like:

| Example  | Picture |
| :---: | :---: |
| Accepted  | ![image](https://user-images.githubusercontent.com/5453796/167943569-efaec8c5-1546-432d-9446-7707807772e4.png)  |
| Accepted <br> (3rd Channel) | ![image](https://user-images.githubusercontent.com/5453796/167943973-0b3e0170-e395-4dcd-b083-60b19aca174d.png) |
| Declined  | ![image](https://user-images.githubusercontent.com/5453796/167943134-0a0a23c1-2330-44c7-a678-078b0ec64b5b.png) |
| Reactivated | ![image](https://user-images.githubusercontent.com/5453796/167943513-a6e646de-951b-424e-8a24-9a99d911aeb1.png) |





## How to install:
> Install the required package: 
```
python3 -m pip install -U novus
```
<br>

> Edit Line 10 / 11 in bot.py 

https://github.com/Braandn/Discord-Suggestion-System-Bot/blob/32fa6ed96c0938343bb65311e3bf14dba0d71ae9/bot.py#L11-L12

<br>

> Then start the Bot
```
python3 Bot.py
```

This is made with Discord Novus to use SlashCommands

## Usage:
```
/proposal channel type
```

Channel: Pick the `channel` out of the given list.

Type: Select the `type` of the `channel`

> The data will be stored in `proposal.json`

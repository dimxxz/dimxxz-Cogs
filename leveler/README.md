Original cog written by stevy/Maybe-Useful-Cogs https://github.com/AznStevy/Maybe-Useful-Cogs

All credits go to stevy for this cog.
If you need support for this cog, please visit stevy's github page.

- This is a new design of the leveler cog. It is still WIP according to stevy!
- Please keep that in mind when using this newer version!

----------------------------------------------------------------------------------------------
Modified and improved by me, dimxxz


----------------------------------------------------------------------------------------------
Major update 04.04.2018:

removed commands:
- backgrounds, addprofilebg, delprofilebg, addrankbg, delrankbg, addlevelbg, dellevelbg

added commands:
+ lvlshop, lvlshop list, lvlshop buy, lvlshop add, lvlshop del, lvlshop inv, lvlshop give, lvlshop fix


----------------------------------------------------------------------------------------------
IMPORTANT!:
Previous background settings won't work with this update.
backgrounds.json file will be created by default but not used by leveler at all!
Completely disposed the usage of backgrounds.json!
You will need to set up all backgrounds again since lvlshop is ported to mongodb completely.
Use the default backgrounds from the backgrounds.json in data/leveler if needed.

lvlshop allows you to set the price for each background.
Purchased backgrounds will be applied to the buyer's account.
Background switching still functions with the profileset, rankset and levelupset commands.

----------------------------------------------------------------------------------------------


Old but still included features:
1. Rank Roles assignment issue fixed
2. Rank Roles can now be assigned with Level-up Message turned off
3. Bot's own commands give 0 exp
4. Added Ignore Channel Feature: listed Channel IDs won't process EXP/ Credits
5. Auto reset Background feature (in case a custom bg is removed or link not working)
6. Slight changes to the design/font
7. Removed Badge border color
8. Bot owner can give global badges to users
9. Badge priority on profile fixed
10. Rank Role assignment notification added


Installation:

Replace `[p]` with your bot's prefix.
```
[p]cog repo add dimxxz-Cogs https://github.com/dimxxz/dimxxz-Cogs
```
```
[p]cog install dimxxz-Cogs leveler
```

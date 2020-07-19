# Building

Will be built with Slacks [EventAPI](https://api.slack.com/events-api) and will need:

- message.channels - to listen for messages
- chat.postMessage - to post into the channel
- member_joined_channel - to print usage instructions when a new user joins the channel

## Features for the future

It may also be useful to have options to click a user in the report to automatically mention them in a message in the current channel. For example you might be in the `#team` channel, request the report, click a name and it automatically adds them as a mention in a draft message for the current `#team` channel so communication continues in the open.

Another use case would be to have the headers for the report be clickable. This would allow for something similar to the feature described above but could add all users in that column as mentions. This way you could easily notify everyone marked as "available" without bothering people away at lunch

---
group name: available

when a user does something like `/teamstatus online` it adds them to the "@available" custom group

| @available | unavailable | lunch | break | offline |
+-----------------------------------------------------
| user 1     | user 2      |       | user 3|         |

this way, if you want to quickly alert all people available for task assignment you can click the '@available` column header

---

this should be in line but private, like a giphy preview
I don't want any pop-ups, all interaction should be in line and only exposed publically when needed

---

maybe a way to configure regular, unprompted, reports. Like maybe every hour?
this is to help if someone forgets to update themselves back to available
would need to have a way to enable/disable cause it could be annoying

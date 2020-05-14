# Team Status - WIP
**NOTE: this is a work in progress and is currently not hosted or installable**

Slack App to keep track of who's online, at lunch, or on a break


## Example usage

This tool consists of two components. The first is for setting and changing a users Slack status, the other is for getting a quick report on the status of the team as a whole.

### Setting Status

From the Slack client you can use the following commands to set your status:
```
/teamstatus online
/teamstatus lunch
/teamstatus break
/teamstatus back
/teamstatus eod
```

The reason for having our own method of setting and updating user status is to provide the consistency needed for accurate reporting. There is already some logic in place to take things like `/teamstatus walk` or `/teamstatus brb` and convert it to the `break` status. This way teams can keep using the verbage they are accustomed to but managers and team leaders can have accurate up-to-the-minute reports for things like seeing who is immediately available for task assignment.

Another reason for this is that we keep a copy of the users status, and when it was set, in a DB as Slack does not seem to provide a way of how long a users status has been set that way. This comes into play for requesting a report. That way not only can you see who is at lunch or on break, but how long they have been in that status. 

### Reporting on Status
If you want to get a breakdown of the team status run the following:
```
/teamstatus report
```

The report will look something like this:
| Available     | Break | Lunch | Offline |
| --- | --- | --- | --- |
| user 1 | user 3 (for 45 mins) | user 5 (for 5 mins) | user 7 |
| user 2 | user 4 (for 10 mins) | user 6 (for 8 mins) | user 8 | 

The report will have the users names appear as slack links so you can click within the provided report to go directly into a private conversation with the user.

#### Features for the future
It may also be useful to have options to click a user in the report to automatically mention them in a message in the current channel. For example you might be in the `#team` channel, request the report, click a name and it automatically adds them as a mention in a draft message for the current `#team` channel so communication continues in the open. 

Another use case would be to have the headers for the report be clickable. This would allow for something similar to the feature described above but could add all users in that column as mentions. This way you could easily notify everyone marked as "available" without bothering people away at lunch
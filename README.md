# BWT_Co-players
Lightweight AI engine for detecting zero-day phishing attacks in emails and SMS before user interaction.
*Trust Nothing in Your Inbox*

-Problem-
Phishing attacks are getting smarter every day. Attackers create fake emails and SMS messages that look almost real and trick users into clicking malicious links. Most traditional systems rely on blacklists, which only work if the link has already been reported.
The real problem is zero-day phishing — newly generated links and messages that are not yet in any database. By the time they are reported, the damage is already done.

-Our Idea-
We are building a lightweight AI-based system that analyzes incoming email or SMS content and detects phishing attempts before the user interacts with them.
Instead of checking only blacklists, our system looks at:
#URL structure
#Suspicious keywords
#Message tone (urgent / threatening)
#Link patterns
#Sender anomalies
The system generates a risk score and flags the message if it looks dangerous — even if the link has never been seen before.

-Architecture Overview-
1.User receives Email / SMS
2.System extracts text and URLs
3.Feature Extraction Module analyzes patterns
4.Machine Learning Model predicts phishing probability
5.Risk Scoring Engine assigns score (0–100%)
6.System alerts user before action is taken

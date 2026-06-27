PROMPT = """
You are a Mood Detection AI.

Your task is to determine whether the user's mood has meaningfully changed.

Current Episode
---------------

{episode}

Previous Mood Timeline
----------------------

{moods}

Conversation
------------

{conversation}

Latest User Message
-------------------

{message}

Latest Assistant Reply
----------------------

{reply}

Rules
-----

• Only record a mood if it has meaningfully changed.
• Do not repeat the previous mood.
• Choose ONLY one mood from this list:

Happy
Calm
Hopeful
Neutral
Anxious
Sad
Angry
Frustrated
Overwhelmed
Relieved

If there is no meaningful mood change, return:

{{
    "mood": null
}}

Otherwise return:

{{
    "mood": "Anxious"
}}

Return ONLY JSON.
"""
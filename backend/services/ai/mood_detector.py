from services.llm_provider import generate_response

from services.ai.json_parser import JSONParser
from services.ai.prompts.mood_prompt import PROMPT

from models import EpisodeMood

class MoodDetector:

    def __init__(self):

        self.json_parser = JSONParser()

    def update(

        self,

        db,

        episode,

        conversation,

        latest_message,

        reply

    ):

        ##################################################
        # Increment Counter
        ##################################################

        episode.messages_since_last_mood += 1

        db.commit()

        db.refresh(episode)

        ##################################################
        # Wait until enough messages
        ##################################################

        if episode.messages_since_last_mood < 3:

            return

        ##################################################
        # Reset Counter
        ##################################################

        episode.messages_since_last_mood = 0

        db.commit()

        db.refresh(episode)

        ##################################################
        # Load Previous Moods
        ##################################################

        previous_moods = db.query(EpisodeMood).filter(

            EpisodeMood.episode_id == episode.episode_id

        ).order_by(

            EpisodeMood.created_at

        ).all()

        ##################################################
        # Build Prompt
        ##################################################

        prompt = self.build_prompt(

            episode,

            previous_moods,

            conversation,

            latest_message,

            reply

        )

        ##################################################
        # Gemini
        ##################################################

        response = generate_response(

            prompt

        )

        print("\n===== Mood Detector =====")
        print(prompt)
        print("-------------------------")
        print(response)
        
        ##################################################
        # Parse JSON
        ##################################################

        decision = self.json_parser.parse(

            response

        )

        print(decision)
        print("=========================\n")

        ##################################################
        # No Mood
        ##################################################

        if decision["mood"] is None:

            return

        ##################################################
        # Duplicate Mood
        ##################################################

        if len(previous_moods) > 0:

            latest_mood = previous_moods[-1].mood

            if latest_mood == decision["mood"]:

                return

        ##################################################
        # Save Mood
        ##################################################

        self.save(

            db,

            episode,

            decision["mood"]

        )

        pass

    def build_prompt(

        self,

        episode,

        previous_moods,

        conversation,

        latest_message,

        reply

    ):

        ##################################################
        # Episode
        ##################################################

        episode_text = f"""
    Episode ID: {episode.episode_id}

    Title: {episode.title}

    Status: {episode.status}

    Summary:
    {episode.summary if episode.summary else "None"}
    """

        ##################################################
        # Previous Mood Timeline
        ##################################################

        if len(previous_moods) == 0:

            moods_text = "None"

        else:

            moods_text = ""

            for mood in previous_moods:

                moods_text += f"{mood.created_at} - {mood.mood}\n"

        ##################################################
        # Conversation
        ##################################################

        conversation_text = ""

        for message in conversation:

            role = message["role"].capitalize()

            conversation_text += f"{role}: {message['content']}\n"

        ##################################################
        # Final Prompt
        ##################################################

        return PROMPT.format(

            episode=episode_text,

            moods=moods_text,

            conversation=conversation_text,

            message=latest_message,

            reply=reply

        )

        pass

    def save(

        self,

        db,

        episode,

        mood

    ):

        new_mood = EpisodeMood(

            episode_id=episode.episode_id,

            mood=mood

        )

        db.add(

            new_mood

        )

        db.commit()

        db.refresh(

            new_mood

        )

        print("\n===== Mood Saved =====")

        print(

            new_mood.mood

        )

        print(

            new_mood.created_at

        )

        print("======================\n")
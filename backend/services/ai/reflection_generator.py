from services.llm_provider import generate_response

from services.ai.json_parser import JSONParser
from services.ai.prompts.reflection_prompt import PROMPT

from models import EpisodeReflection


class ReflectionGenerator:

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

        episode.messages_since_last_reflection += 1

        db.commit()

        db.refresh(episode)

        ##################################################
        # Wait until enough messages
        ##################################################

        if episode.messages_since_last_reflection < 5:

            return

        ##################################################
        # Reset Counter
        ##################################################

        episode.messages_since_last_reflection = 0

        db.commit()

        db.refresh(episode)

        ##################################################
        # Load Previous Reflections
        ##################################################

        previous_reflections = db.query(EpisodeReflection).filter(

            EpisodeReflection.episode_id == episode.episode_id

        ).order_by(

            EpisodeReflection.created_at

        ).all()

        ##################################################
        # Build Prompt
        ##################################################

        prompt = self.build_prompt(

            episode,

            previous_reflections,

            conversation,

            latest_message,

            reply

        )

        ##################################################
        # LLM
        ##################################################

        response = generate_response(

            prompt

        )

        print("\n===== Reflection Generator =====")
        print(prompt)
        print("-------------------------------")
        print(response)

        ##################################################
        # Parse JSON
        ##################################################

        decision = self.json_parser.parse(

            response

        )

        print(decision)
        print("===============================\n")

        ##################################################
        # No Reflection
        ##################################################

        if decision["reflection"] is None:

            return

        ##################################################
        # Duplicate Reflection
        ##################################################

        if len(previous_reflections) > 0:

            latest_reflection = previous_reflections[-1].reflection

            if latest_reflection.strip().lower() == decision["reflection"].strip().lower():

                return

        ##################################################
        # Save Reflection
        ##################################################

        self.save(

            db,

            episode,

            decision["reflection"]

        )

    def build_prompt(

        self,

        episode,

        previous_reflections,

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
        # Previous Reflections
        ##################################################

        if len(previous_reflections) == 0:

            reflections_text = "None"

        else:

            reflections_text = ""

            for reflection in previous_reflections:

                reflections_text += (
                    f"{reflection.created_at} - "
                    f"{reflection.reflection}\n"
                )

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

            reflections=reflections_text,

            conversation=conversation_text,

            message=latest_message,

            reply=reply

        )

    def save(

        self,

        db,

        episode,

        reflection

    ):

        new_reflection = EpisodeReflection(

            episode_id=episode.episode_id,

            reflection=reflection

        )

        db.add(

            new_reflection

        )

        db.commit()

        db.refresh(

            new_reflection

        )

        print("\n===== Reflection Saved =====")

        print(

            new_reflection.reflection

        )

        print(

            new_reflection.created_at

        )

        print("============================\n")
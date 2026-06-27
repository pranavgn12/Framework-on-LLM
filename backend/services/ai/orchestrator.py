from services.llm import chat
from services.title_generator import generate_title

from services.ai.episode_manager import EpisodeManager
from services.ai.episode_detector import EpisodeDetector

from services.ai.short_term_memory import ShortTermMemory
from services.ai.long_term_memory import LongTermMemory
from services.ai.memory_rag import MemoryRAG
from services.ai.knowledge_rag import KnowledgeRAG
from services.ai.profile import Profile

from services.ai.pattern_detector import PatternDetector
from services.ai.memory_consolidator import MemoryConsolidator

from services.ai.mood_detector import MoodDetector
from services.ai.reflection_generator import ReflectionGenerator

from services.ai.episode_summarizer import EpisodeSummarizer

from models import EpisodeReflection

class AIOrchestrator:

    def __init__(self):

        self.episode_manager = EpisodeManager()
        self.episode_detector = EpisodeDetector()

        self.mood_detector = MoodDetector()
        self.reflection_generator = ReflectionGenerator()

        self.episode_summarizer = EpisodeSummarizer()

        self.short_term_memory = ShortTermMemory()
        self.long_term_memory = LongTermMemory()
        self.memory_rag = MemoryRAG()
        self.knowledge_rag = KnowledgeRAG()
        self.profile = Profile()

        self.pattern_detector = PatternDetector()
        self.memory_consolidator = MemoryConsolidator()

    def chat(

        self,

        db,

        user_id,

        conversation,

        latest_message,

        current_title

    ):

        ##################################################
        # 1. Generate Conversation Title
        ##################################################

        title = None

        if current_title == "New Conversation":

            title = generate_title(

                latest_message

            )

        ##################################################
        # 2. Episode Lifecycle
        ##################################################

        episode = self.episode_manager.get_active_episode(

            db,

            user_id

        )

        decision = self.episode_detector.detect(

            episode,

            latest_message

        )

        if decision["action"] == "CREATE":

            episode = self.episode_manager.create_episode(

                db,

                user_id,

                decision["title"]

            )

        elif decision["action"] == "CLOSE":

            if episode is not None:

                ##################################################
                # Generate Episode Summary
                ##################################################

                summary = self.episode_summarizer.summarize(

                    conversation

                )

                ##################################################
                # Save Episode Summary
                ##################################################

                self.episode_summarizer.save(

                    db,

                    episode,

                    summary

                )

                ##################################################
                # Load Previous Memory
                ##################################################

                previous_memory = self.memory_consolidator.load(

                    db,

                    user_id

                )

                ##################################################
                # Load Episode Reflections
                ##################################################

                reflections = db.query(

                    EpisodeReflection

                ).filter(

                    EpisodeReflection.episode_id == episode.episode_id

                ).order_by(

                    EpisodeReflection.created_at

                ).all()

                ##################################################
                # Build Updated Memory
                ##################################################

                memory = self.memory_consolidator.consolidate(

                    previous_memory,

                    summary,

                    reflections

                )

                ##################################################
                # Save Long-Term Memory
                ##################################################

                self.memory_consolidator.save(

                    db,

                    user_id,

                    memory

                )

                ##################################################
                # Close Episode
                ##################################################

                self.episode_manager.close_episode(

                    db,

                    episode

                )

            episode = None

        elif decision["action"] == "CONTINUE":

            pass

        elif decision["action"] == "NONE":

            pass

        ##################################################
        # 3. Retrieve Profile
        ##################################################

        profile = None

        ##################################################
        # 4. Retrieve Long-Term Memory
        ##################################################

        long_term_memory = self.memory_consolidator.load(

            db,

            user_id

        )

        ##################################################
        # 5. Retrieve Memory RAG
        ##################################################



        ##################################################
        # 6. Retrieve Knowledge RAG
        ##################################################

        knowledge = self.knowledge_rag.retrieve(

            latest_message

        )

        ##################################################
        # 7. Chat with LLM
        ##################################################

        reply = chat(

            conversation=conversation,

            profile=profile,

            memory=long_term_memory,

            knowledge=knowledge,

            episode=episode,

            reflection=None,

            mood=None

        )

        ##################################################
        # 8. Mood Detection
        ##################################################

        if episode is not None:

            self.mood_detector.update(

                db,

                episode,

                conversation,

                latest_message,

                reply

            )

        ##################################################
        # 9. Reflection Generation
        ##################################################

        if episode is not None:

            self.reflection_generator.update(

                db,

                episode,

                conversation,

                latest_message,

                reply

            )

        ##################################################
        # 10. Future Background Tasks
        ##################################################

        # self.pattern_detector.detect(...)
        # self.memory_consolidator.consolidate(...)

        ##################################################
        # 11. Response
        ##################################################

        return {

            "reply": reply,

            "title": title,

            "episode": episode

        }
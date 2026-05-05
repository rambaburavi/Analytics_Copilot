from core.sql_pipeline import SQLAgentPipeline

# Singleton instance (loads only once)
shared_pipeline = None


def get_pipeline():
    global shared_pipeline

    if shared_pipeline is None:
        print("Initializing SQLAgentPipeline (lazy load)...")
        shared_pipeline = SQLAgentPipeline()

    return shared_pipeline